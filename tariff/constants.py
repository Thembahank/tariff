DATE_FORMAT_CHOICES = (
    (
        "day first",
        "day first",
    ),
    (
        "month first",
        "month first",
    ),
    (
        "year first",
        "year first",
    ),
)

CSV = "csv"
XLSX = "xlsx"
XLS = "xls"

FILE_TYPE_CHOICES = (
    (
        CSV,
        CSV,
    ),
    (
        XLSX,
        XLSX,
    ),
    (
        XLS,
        XLS,
    ),
)


class FileStatus:
    PROCESSED = "processed"
    ERROR = "errors"
    PENDING = "pending"


FILE_STATUS_CHOICES = (
    (
        FileStatus.PENDING,
        FileStatus.PENDING,
    ),
    (FileStatus.PROCESSED, FileStatus.PROCESSED),
    (FileStatus.ERROR, FileStatus.ERROR),
)

SEMICOLON = ";"
COMMA = ","
CSV_SEPARATOR_CHOICES = ((SEMICOLON, "SEMICOLON (;)"), (COMMA, "COMMA (,)"))

LANDIS_GYR = "LGZ"
ELSTER = "ELS"
ALS = "ALS"
METER_CHOICES = [
    (LANDIS_GYR, "Landis gyr"),
    (ELSTER, "Elster"),
    (ALS, "ALS"),
]

# file, and function attr ChildProcessError
LGZ_F = "lgz"
ALS_F = "als"
ELS_F = "els"

# dateformats
DAYFIRST = "dayfirst"
YEARFIRST = "yearfirst"

# header identifier for file formats
LGZ_HEADERS_SET = {
    "0-0:1.0.0",
    "0-0:96.240.12[hex]",
    "1-1:1.5.0[kw]",
    "1-1:5.5.0[kvar]",
}
ALS_HEADERS_SET = {
    "rdate",
    "rtime",
    "kwh+",
    "kvarh+",
    "kwh-",
    "kvarh-",
    "kva",
    "pf",
    "status",
}
ELS_HEADERS_SET = {
    "date, starttime, endtime, 1: import kw, 2: off, 3: q1 inductive import, 4: off, 5: off, 6: q4 capacitive export, flags"
}

ELS_2_HEADERS_SET = {
    "date",
    "starttime",
    "endtime",
    "1:importkw",
    "2:off",
    "3:q1inductiveimport",
    "4:off",
    "5:off",
    "6:q4capacitiveexport",
    "flags",
}


# energy values
KVA = "kva"
KW = "kw"
KWH = "kwh"
KVAR = "kvar"
KVARH = "kvarh"
KVARH_M = "kvarh-"
KVARH_P = "kvarh+"

# Tariffs
PEAK = "peak"
OFF_PEAK = "off_peak"
STANDARD = "standard"


class TariffCategory:
    PEAK = PEAK
    OFF_PEAK = OFF_PEAK
    STANDARD = STANDARD


class RateBillingType:
    PER_MONTH = "per_month"
    PER_YEAR = "per_year"
    PER_MAX_KVA_PER_MONTH = "per_max_kva_per_month"
    PER_MAX_KVA_PER_YEAR = "per_max_kva_per_year"  # peak and standard only
    PER_KWH = "per_kwh"
    PER_KVA = "per_kva"


MIN_CAPACITY_1MVA = "MIN_CAPACITY_1MVA"
MIN_NAC_1MVA = "MIN_NAC_1MVA"
SINGLE_PHASE_230_V = "SINGLE_PHASE_230_V"
MULTI_PHASE_400_OR_230_V = "MULTI_PHASE_400_OR_230_V"


class ConnectionTypes:
    SINGLE_PHASE_230_V = SINGLE_PHASE_230_V
    MULTI_PHASE_400_OR_230_V = MULTI_PHASE_400_OR_230_V
    MIN_CAPACITY_1MVA = MIN_CAPACITY_1MVA
    MIN_NAC_1MVA = MIN_CAPACITY_1MVA


# Device types refine later
ANY_230_400_V = "ANY_230_400_V"
LESS_11KV_230_400_V = "LESS_11KV_230_400_V"
CAPACITY_EXCEED_11KV = "CAPACITY_EXCEED_11KV"
DIRECT_FROM_SUBSTATIION_230_400_V = "DIRECT_FROM_SUBSTATIION_230_400_V"
PREPAID_METERING = "PREPAID_METERING"
POST_PAID_METERING = "POSTPAID_METERING"


class ChargeVoltageType:
    ANY_230_400_V = ANY_230_400_V
    LESS_11KV_230_400_V = LESS_11KV_230_400_V
    CAPACITY_EXCEED_11KV = CAPACITY_EXCEED_11KV
    PREPAID_METERING = PREPAID_METERING
    POST_PAID_METERING = POST_PAID_METERING
    DIRECT_FROM_SUBSTATIION_230_400_V = DIRECT_FROM_SUBSTATIION_230_400_V


class FixedChargeTypes:
    ANY_230_400_V = ANY_230_400_V
    LESS_11KV_230_400_V = LESS_11KV_230_400_V
    CAPACITY_EXCEED_11KV = CAPACITY_EXCEED_11KV
    PREPAID_METERING = PREPAID_METERING
    POST_PAID_METERING = POST_PAID_METERING


HIGH_DEMAND = "high_demand"
LOW_DEMAND = "low_demand"


class DemandChargeVoltageType:
    ANY_230_400_V = ANY_230_400_V
    LESS_11KV_230_400_V = LESS_11KV_230_400_V
    DIRECT_FROM_SUBSTATIION_230_400_V = DIRECT_FROM_SUBSTATIION_230_400_V
    CAPACITY_EXCEED_11KV = CAPACITY_EXCEED_11KV
