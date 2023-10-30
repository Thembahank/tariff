import io

import pandas as pd
import streamlit as st
from tariff.file_parse import read_and_parse_excel, aggregate_highest_kva, concate_all_sheets, max_kva


def multi_excel(dfs):
    # Specify the Excel writer and the file name
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Loop through the list of DataFrames and write each one to a different sheet
        for index, df in enumerate(dfs):
            df.to_excel(writer, sheet_name=f'Sheet_{index + 1}', index=False)
    output.seek(0)
    return output.read()


def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    output.seek(0)
    return output.read()

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
    
    all_dfs = []
    for i in range(0, 6):
        all_dfs.append(read_and_parse_excel(sheet_name=i, multiplier=multiplier))
    
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
    
    st.divider()
    
    st.write('Chart')
    chart_data = edited_df[['Date', 'KVA', 'KW', 'KVAR']]
    chart_data = chart_data.set_index('Date')
    st.line_chart(chart_data)
    
    
    
    st.write('Download sheet data')
    excel_data_edited = to_excel(edited_df)
    st.download_button(
        label="Download table to  Excel",
        data=excel_data_edited,
        file_name='all_sheets.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    
    # write them all to excel
    # button to download excel
    button = st.toggle('Download all sheets as Excel')
    if button:
        st.write("Preparing to download all sheets as Excel")
        excel_data = multi_excel(all_dfs)
        st.write("Done preparing to download all sheets as Excel")
        st.download_button(
            label="Download All Sheets",
            data=excel_data,
            file_name='all_sheets.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
    
    st.divider()
    
    st.subheader('KVA per meter')
    merged = concate_all_sheets()
    st.write(merged)
    
    excel_data = to_excel(merged)
    st.download_button(
        label="Download KVA per meter",
        data=excel_data,
        file_name='merged_kva.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    
    st.divider()
    
    df_max = max_kva(merged)
    st.subheader('Highest KVA')
    st.write(df_max)
    
    excel_data = to_excel(df_max)
    st.download_button(
        label="Download Max KVA as Excel",
        data=excel_data,
        file_name='max_kva.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )


load_files()
