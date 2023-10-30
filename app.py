import streamlit as st
from tariff.file_parse import read_and_parse_excel, aggregate_highest_kva


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
    sheet_number = st.sidebar.number_input('Sheet number', value=0)
    
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
    
    st.divider()
    st.subheader('Totals KVA')
    aggregated_df = None
    if uploaded_file is not None:
        aggregated_df = aggregate_highest_kva(file_obj=uploaded_file, sheet_range=(0, sheet_number), multiplier=multiplier)
        print(df)
    
    if skip_file:
        aggregated_df = aggregate_highest_kva(file_obj=None, sheet_range=(0, sheet_number), multiplier=multiplier)
        print(df)
    
    st.data_editor(
        aggregated_df,
        num_rows="dynamic",
    )


load_files()
