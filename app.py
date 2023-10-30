import io

import pandas as pd
import streamlit as st
from tariff.file_parse import read_and_parse_excel, aggregate_highest_kva, concate_all_sheets, max_kva


def to_excel(df):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output)
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    excel_data = output.getvalue()
    return excel_data

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def add_title():
    st.title("""
    Tariff Calculator
    """)
    
    
def load_files():
    add_title()
    st.sidebar.header('Add your file or skip to use the default file')
    
    st.sidebar.write('File format must be xlsx. Check the date column has a title `Date`')

    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv", "xlsx", "xls"])
    
    st.sidebar.write('Sheet number must be between 0 -6 if you are using the default file')
    sheet_number = st.sidebar.number_input('Sheet number', value=0, min_value=0, max_value=6)
    
    st.sidebar.write('multiplier must be a number')
    multiplier = st.sidebar.number_input('Multiplier', value=200000)
    
    skip_file = st.sidebar.checkbox('Skip file upload, use default', value=True)
    
    df = None
    if uploaded_file is not None:
        df = read_and_parse_excel(uploaded_file, sheet_name=sheet_number, multiplier=multiplier)
        print(df)
        
    if skip_file:
        df = read_and_parse_excel(sheet_name=sheet_number, multiplier=multiplier)
        print(df)
    
    st.subheader('Tariff table')
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        column_config={
            "Date": st.column_config.DatetimeColumn(
                "Date",
                format="D MMM YYYY, h:mm a",
            ),
            "KW": st.column_config.NumberColumn(
                "KW",
                min_value=0,
                max_value=100000000,
                step=1,
             
            ),
            
        },
        
    )
    csv = convert_df(edited_df)
    st.download_button(
        label="Download totals as csv",
        data=csv,
        file_name='tariff.csv',
        mime='text/csv',
    )
    
    st.divider()
    merged = concate_all_sheets()
    st.subheader('KVA per meter')
    st.write(merged)
    
    df_max = max_kva(merged)
    st.subheader('Highest KVA')
    st.write(df_max)
    
    csv = convert_df(df_max)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='max-kva.csv',
        mime='text/csv',
    )


load_files()
