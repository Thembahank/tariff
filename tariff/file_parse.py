from collections import defaultdict
from datetime import datetime

import pandas as pd
from io import BytesIO

from tariff.constants import HIGH_DEMAND, LOW_DEMAND
from tariff.tariff_maps import coe_tariff_e_2020_2021

OFF_PEAK = "off_peak"


def add_demand_slots(df):
    """
    Adds 'month', 'season', and 'rate' columns to the DataFrame based on its 'Date' (date-time) column.

    Parameters:
        df (pd.DataFrame): The DataFrame containing energy data.

    Returns:
        pd.DataFrame: The updated DataFrame with new columns.
    """
    # Extract month from the 'Date' column
    df['month'] = df['Date'].dt.month
    
    # Determine the season (high_demand or low_demand) based on the month
    df['season'] = df['month'].apply(
        lambda x: HIGH_DEMAND if x in coe_tariff_e_2020_2021["high_demand_months"] else LOW_DEMAND)
    
    # Holidays and their treatment
    default_holidays = [datetime.strptime(f"{datetime.now().year}-06-16", "%Y-%m-%d").date(),
                        datetime.strptime(f"{datetime.now().year}-08-09", "%Y-%m-%d").date()]
    
    # Determine the rate (off_peak, peak, or standard) based on the season and hour
    def get_rate(row):
        date_time = row['Date']
        if date_time.date() in default_holidays or date_time.weekday() == 6:
            return OFF_PEAK
        
        hour = date_time.hour
        season = row['season']
        return coe_tariff_e_2020_2021[season][hour][0]
    
    df['rate'] = df.apply(get_rate, axis=1)
    
    return df


def aggregate_highest_kva(file_obj=None, sheet_range=(0, 6), multiplier=200000):
    """
    Aggregates the highest total kVA across all meters for each sheet.

    Parameters:
        file_obj (file object): The file object of the Excel file.
        sheet_range (tuple): The range of sheet numbers to consider.
        multiplier (int): The multiplier for kVA.

    Returns:
        pd.DataFrame: The aggregated DataFrame.
    """
    master_df = pd.DataFrame()

    for i in range(sheet_range[0], sheet_range[1] + 1):
        df = read_and_parse_excel(file_obj, sheet_name=i, multiplier=multiplier)
        df['Meter'] = f'Mtr{i+1}'
        master_df = pd.concat([master_df, df], ignore_index=True)

    # Ensure each combination of Date and Meter is unique by summing KVA values
    master_df = master_df.groupby(['Date', 'Meter'])['KVA'].sum().reset_index()

    # Group by Date and sum the kVA values
    total_kva = master_df.groupby('Date')['KVA'].sum().reset_index()

    # Find the Date with the highest total kVA
    highest_kva_date = total_kva.loc[total_kva['KVA'].idxmax(), 'Date']

    # Filter the master DataFrame to only include rows with the highest total kVA Date
    highest_kva_df = master_df[master_df['Date'] == highest_kva_date]

    # Pivot to make Meters as columns
    final_df = highest_kva_df.pivot(index='Date', columns='Meter', values='KVA').reset_index()
    final_df['Total kVA'] = final_df.iloc[:, 1:].sum(axis=1)
    final_df['kVA x 200000'] = final_df['Total kVA'] * multiplier

    return final_df



def read_and_parse_excel(file_obj=None, sheet_name=0, multiplier=200000):
    """
    Reads an Excel file from a file object and parses the table data into a DataFrame.

    Parameters:
        file_obj (file object): The file object of the Excel file.
        sheet_name (str or int): The name or index of the sheet to read. Default is 0 (first sheet).

    Returns:
        pd.DataFrame: The parsed DataFrame.
    """
    
    if file_obj is None:
        with open('./ncp-data.xlsx', 'rb') as f:
            file_obj = f
    # Read the Excel file into a DataFrame, using the first column as the index
            df = pd.read_excel(BytesIO(file_obj.read()), sheet_name=sheet_name, index_col=0, engine='openpyxl')
    else:
        df = pd.read_excel(BytesIO(file_obj.read()), sheet_name=sheet_name, index_col=0, engine='openpyxl')
    
    # Replace commas with dots in the numeric columns to ensure they are read as floats
    numeric_columns = ['KW', 'KVAR', 'KVA']
    for col in numeric_columns:
        df[col] = df[col].apply(lambda x: float(str(x).replace(',', '.'))  if pd.notnull(x) else x)
        df[col] = df[col] * multiplier
    
    # Convert the 'HEX' column to datetime format (the name seems to be 'HEX' based on your sample data)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %H:%M')
    df = add_demand_slots(df)
    
    return df
