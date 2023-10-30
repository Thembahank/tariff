import datetime
import decimal
import math

from core.utils.app_logging import log_error
from energy_manager.constants import (
    OFF_PEAK,
    LOW_DEMAND,
    HIGH_DEMAND,
    STANDARD,
    PEAK,
)
from energy_manager.utils.file_parser import kw_to_kwh


def get_tariff_type(date_time: datetime.datetime, tariff_intervals):
    # print(f"tariff check {date_time}, for tar {tariff_intervals}")

    holidays = [datetime.datetime.now().date]
    # date - check if it is a holiday

    if date_time.date in holidays or date_time.weekday() == 6:
        return OFF_PEAK

    month = date_time.month
    if month in tariff_intervals["high_demand_months"]:
        tariff_period = tariff_intervals[LOW_DEMAND]
    else:
        tariff_period = tariff_intervals[HIGH_DEMAND]

    # return half hourly tariff type
    tariff = tariff_period.get(str(date_time.hour))

    tariff_type = tariff["0"] if date_time.minute == 0 else tariff["1"]
    return tariff_type


def get_max_kva(df_consumption, month=None):
    """Get the max kva value from dataframe, filter on month if provided"""
    # https://towardsdatascience.com/filtering-data-frames-in-pandas-b570b1f834b9

    try:
        print(df_consumption.head(), "max_kva")
        df_max_kva = df_consumption[df_consumption["period"].isin([PEAK, STANDARD])]

        # filter for only a month if provide
        if month is not None:
            df_max_kva = df_max_kva[df_max_kva["month"] == month]

        max_value = df_max_kva["kva"].max()
        return max_value
    except Exception as e:
        log_error(e, get_max_kva.__name__)


def get_peak_charge(period, kwh, season, charge_voltage_type, rates_dic):
    """Returns the rate for a kwh"""
    total = float(kwh) * rates_dic[season][charge_voltage_type][period]
    return total


def get_season_type(high_demand_mnths, month):
    return HIGH_DEMAND if month in high_demand_mnths else LOW_DEMAND


def apply_energy_charge(charge_voltage_type, tariff_charge, dataframe):
    """add the energy charge"""

    dataframe["kwh"] = dataframe["kw"].apply(lambda x: kw_to_kwh(x))
    rates_dic = tariff_charge["types"]
    # https://towardsdatascience.com/apply-and-lambda-usage-in-pandas-b13a1ea037f7
    try:
        dataframe["price_per_kwh"] = dataframe.apply(
            lambda x: get_peak_charge(
                x["period"], x["kwh"], x["season"], charge_voltage_type, rates_dic
            ),
            axis=1,
        )
    except Exception as e:
        raise Exception(f"error {e} cannot add energy")

    return dataframe


def get_clean_label(data):
    return data.replace("_", " ")


class TariffCalculator:
    """
    :param df Dataframe
    :param tariff
    :param charge_voltage_type


    """

    def __init__(self, charge_voltage_type, tariff, df, current_charges=None):
        self.charge_voltage_type = charge_voltage_type
        self.tariff = tariff
        self.high_demand_months = tariff["high_demand_months"]
        self.months = list(df.month.unique())
        self.num_m_periods = len(self.months)  # months
        self.dataframe = df
        self.current_charges = current_charges

    def calculate_tariff(self):
        """

        :return: Bill from profile data
        """
        print("retrieving bill: charge voltage type")
        current_charges = []
        for charge in self.tariff["charges"]:
            fn = self.__getattribute__(charge["name"])
            print(fn.__name__, charge)
            c = fn(charge)
            current_charges.append(c)
        self.current_charges = current_charges
        return current_charges

    def get_bill_summary(self):

        if self.current_charges is None:
            raise Exception(
                "Make sure you call caculate tariff or"
                " instantiate class with current charge"
            )

        bill_total = 0
        vat_rate = self.tariff["vat_rate"]

        for i in self.current_charges:
            bill_total = bill_total + i["total"]

        vat_amount = bill_total * vat_rate
        bill_total_incl_vat = bill_total + vat_amount

        summary = {
            "total": bill_total,
            "vat_rate": self.tariff["vat_rate"],
            "vat_rate_human": f"{vat_rate * 100} %",
            "vat_amount": vat_amount,
            "total_incl_vat": bill_total_incl_vat,
            "currency": self.tariff["currency"],
            "symb": self.tariff["currency_symbol"],
        }

        return summary

    def fixed_charge(self, tariff_charge):

        # get the device
        rate_billing_type = tariff_charge.get("rate_billing_type", None)  # TODO
        print(tariff_charge["types"])
        rate_amount = tariff_charge["types"].get(self.charge_voltage_type)
        print(rate_amount, "sds", rate_billing_type, self.charge_voltage_type)
        total = rate_amount * self.num_m_periods
        return {
            "name": "Fixed charge",
            "total": total,
            "units": self.num_m_periods,
            "units_type": get_clean_label(rate_billing_type),
            "rate": rate_amount,
            "meta": {},
        }

    def internet_based_consumption_display(self, tariff_charge):

        # get the device
        rate_billing_type = tariff_charge.get("rate_billing_type", None)  # TODO
        rate_amount = tariff_charge["types"].get(self.charge_voltage_type)

        total = rate_amount * self.num_m_periods  # monthly
        return {
            "name": "Internet based consumption display",
            "total": total,
            "units": self.num_m_periods,
            "units_type": get_clean_label(rate_billing_type),
            "rate": rate_amount,
            "meta": {},
        }

    def demand_charge(self, tariff_charge):
        """ Calculate highest kva in month """
        months = self.months
        total = 0
        rate_billing_type = tariff_charge.get("rate_billing_type", None)
        for month in months:
            try:
                max_kva = get_max_kva(self.dataframe, month)
                print(f"{max_kva}, demand_charge")
                if month in self.high_demand_months:
                    rate = tariff_charge["types"][HIGH_DEMAND][self.charge_voltage_type]

                else:
                    rate = tariff_charge["types"][LOW_DEMAND][self.charge_voltage_type]

                total = (rate * float(max_kva)) + total

                return {
                    "name": "Demand charge",
                    "total": total,
                    "units": self.num_m_periods,
                    "units_type": get_clean_label(rate_billing_type),
                    "rate": rate,
                    "meta": {},
                }

            except Exception as e:
                log_error(e, self.demand_charge.__name__)
                raise Exception(f"{e} demand charge")

    def network_access_charge(
        self,
        tariff_charge,
    ):
        """
        Based on rolling 12 month period highest KVA
        Dataframe must be filter to include past 12 months if used
        Other base it off max kva
        """

        try:

            max_kva = get_max_kva(self.dataframe)

            rate = tariff_charge["types"][self.charge_voltage_type]
            total = rate * float(max_kva)
            return {
                "total": total,
                "name": "Network access charge",
                "units": float(max_kva),
                "units_type": get_clean_label(
                    tariff_charge.get("rate_billing_type", "-")
                ),
                "rate": rate,
            }

        except Exception as e:
            log_error(e, self.network_access_charge.__name__)
            raise Exception(f"{e} network charge")

    def energy_charge(self, tariff_charge):
        """Returns the total energy charge for a dataframe"""

        try:
            df = apply_energy_charge(
                self.charge_voltage_type,
                tariff_charge,
                self.dataframe,
            )

            total = df["price_per_kwh"].sum()
            units = df["kwh"].sum()
            rate = total / units

            items = [OFF_PEAK, PEAK, STANDARD]
            meta = {}
            kw = 0
            kwh = 0
            price_kwh = 0
            for i in items:
                filtered = df[df["period"] == i]
                ikw = filtered["kw"].sum()
                ikwh = filtered["kwh"].sum()
                iprice = filtered["price_per_kwh"].sum()

                price_kwh = price_kwh + iprice
                kw = ikw + kw
                kwh = ikwh + kwh
                meta.update({i: {"kw": ikw, "kwh": ikwh, "price_per_kwh": iprice}})
            meta.update({"total": {"kw": kw, "kwh": kwh, "price_per_kwh": price_kwh}})
            return {
                "name": "Energy charge",
                "total": total,
                "units": units,
                "units_type": "per kwh",
                "rate": f"{round(rate, 4)} (avg)",
                "meta": meta,
            }

        except Exception as e:
            log_error(e, self.energy_charge.__name__)
            raise Exception(f"{e} energy charge")


def _roundup(x):
    return int(math.ceil(x / 10.0)) * 10


def _get_pf(kw, kva, time):
    try:
        return float(kw) / float(kva)
    except (decimal.InvalidOperation, ZeroDivisionError) as e:
        return 1


def _get_meta_stats(c_data):
    meta = {"max_y": 55, "step_y": 11, "pf_max": 1, "pf_min": 1, "pf_avg": 1}
    try:
        max_y = (_roundup(max([max(c_data["kva"]), max(c_data["kw"])])),)
        step_y = max_y[0] / 5
        meta.update(
            {
                "max_y": max_y,
                "step_y": step_y,
                "pf_max": round(max(c_data["pf"]), 2),
                "pf_min": round(min(c_data["pf"]), 2),
                "pf_avg": round(sum(c_data["pf"]) / len(c_data["pf"]), 2),
            }
        )

    except Exception as e:
        log_error(e, "get_chartdata values:_get_meta_stats")

    return meta
