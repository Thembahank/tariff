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
    Aggregates the highest total kVA across all meters for each sheet and returns the original values.

    Parameters:
        file_obj (file object): The file object of the Excel file.
        sheet_range (tuple): The range of sheet numbers to consider.
        multiplier (int): The multiplier for kVA.

    Returns:
        pd.DataFrame: The aggregated DataFrame containing the row with the highest total kVA.
    """
    dfs = []  # List to hold individual DataFrames

    for i in range(sheet_range[0], sheet_range[1] + 1):
        try:
            df = read_and_parse_excel(file_obj, sheet_name=i, multiplier=1)  # Note the multiplier is set to 1
            df['Meter'] = f'Mtr{i+1}'
            df.rename(columns={'KVA': 'KVA_value'}, inplace=True)
            dfs.append(df)
        except Exception as e:
            print("error", e)

    # Concatenate all DataFrames
    master_df = pd.concat(dfs, ignore_index=True)

    # Pivot table to get 'Meter' as columns and sum of 'KVA_value' as values
    pivot_df = master_df.pivot_table(values='KVA_value', index='Date', columns='Meter', aggfunc='sum', fill_value=0)

    # Reset index for the pivot table
    pivot_df.reset_index(inplace=True)

    # Calculate the total kVA
    pivot_df['Total kVA'] = pivot_df.iloc[:, 1:].sum(axis=1)

    # Find the row with the highest total kVA
    highest_kva_row = pivot_df.loc[pivot_df['Total kVA'].idxmax()]

    # Convert to DataFrame and transpose for better readability
    highest_kva_df = pd.DataFrame(highest_kva_row).transpose()

    # Multiply only the 'Total kVA' by 200,000 for the highest row
    highest_kva_df['kVA x 200000'] = highest_kva_df['Total kVA'] * multiplier

    return highest_kva_df


def concate_all_sheets(file_obj=None, sheet_range=(0, 5), multiplier=200000):
    col_dfs = []  # List to hold individual columns
    
    for i in range(sheet_range[0], sheet_range[1] + 1):
        try:
            df = read_and_parse_excel(file_obj, sheet_name=i, multiplier=1)  # Note the multiplier is set to 1
            meter_name = f'Mtr{i + 1}'
            df.rename(columns={'KVA': 'KVA_value'}, inplace=True)
            
            # Take just the 'Date' and 'KVA_value' columns and rename 'KVA_value' to include the meter name
            col_df = df[['Date', 'KVA_value']].copy()
            col_df.rename(columns={'KVA_value': f'KVA_value_{meter_name}'}, inplace=True)
            col_dfs.append(col_df)
        except Exception as e:
            print("error", e)
    
    # Concatenate all DataFrames by 'Date'
    master_df = pd.concat(col_dfs, ignore_index=True)
    
    # Convert 'Date' to datetime and set as index
    master_df['Date'] = pd.to_datetime(master_df['Date'])
    master_df.set_index('Date', inplace=True)
    
    # Merge all columns based on 'Date'
    master_df = master_df.groupby('Date').first()
    
    # Sum up all KVA_value columns
    kva_cols = [col for col in master_df.columns if 'KVA_value_' in col]
    master_df['Sum_KVA_value'] = master_df[kva_cols].sum(axis=1)
    
    # Multiply the summed up column by 200000
    master_df['Sum_KVA_value_x200000'] = master_df['Sum_KVA_value'] * multiplier
    
    return master_df


def max_kva(df):
    # Find the index of the maximum value in the last column ('Sum_KVA_value_x200000')
    max_idx = df['Sum_KVA_value_x200000'].idxmax()
    # Get the row corresponding to this index
    max_row = df.loc[max_idx]
    
    return max_row


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
        try:
            df[col] = df[col].apply(lambda x: float(str(x).replace(',', '.'))  if pd.notnull(x) else x)
            df[col] = df[col] * multiplier
            # Convert the 'HEX' column to datetime format (the name seems to be 'HEX' based on your sample data)
            df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %H:%M')
            df = add_demand_slots(df)
        except Exception as e:
            print("error", e)
    
    return df
