import streamlit as st
import pandas as pd
import plotly.express as px
import webbrowser as wb
import openpyxl
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from natsort import natsort_keygen
from datetime import datetime
from io import BytesIO

today_date = datetime.now().strftime('%Y-%m-%d')

st.set_page_config(page_title="Stock Check", page_icon="🚚", layout="wide")

st.title("🚚 Genuine Inside (M) Sdn. Bhd. - Stock Tick📝")
st.markdown("##")


#st.header("Sequencer")
#seq_file = st.file_uploader("wms file",type=['xlsx'])

#if seq_file is not None:
    #df_seq = pd.read_excel(seq_file,sheet_name="Sheet2")
    #st.write("Before:")
    #df_seq
    #df_seq  = df_seq .sort_values(by='Location Code', key=natsort_keygen())
    #st.write("After:")
    #df_seq

    # Function to write DataFrames to an Excel file in memory
#def dfs_to_excel(df_list, sheet_list):
    #output = BytesIO()
    #with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        #for dataframe, sheet in zip(df_list, sheet_list):
            #dataframe.to_excel(writer, sheet_name=sheet, index=False)
    #output.seek(0)
    #return output

#df_list = [df_seq]
#sheet_list = ['Sheet1']

# Convert DataFrames to Excel in memory
#excel_file = dfs_to_excel(df_list, sheet_list)

# Streamlit download button
#st.download_button(
    #label="Download Excel file",
   # data=excel_file,
    #file_name=f"WMS_Sequenced_{today_date}.xlsx",
   # mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#)

st.write("______________________________________________________________________________________")
st.header("WMS File Upload")
data_file = st.file_uploader("WMS file",type=['xlsx'])
df1 = pd.read_excel(data_file)
st.write("UPLOAD SUCESS")

product_wms = st.selectbox('WMS PRODUCT column:', df1.columns.tolist())
quantity_wms = st.selectbox('WMS QUANTITY column:', df1.columns.tolist())

st.markdown("#")
st.header("ERP File Upload")
data_file2 = st.file_uploader("ERP file",type=['xlsx'])
df3 = pd.read_excel(data_file2)
#df3.rename(columns={'ProductCode': 'Product', 'ProductDescription': 'Product Name'}, inplace=True)
st.write("UPLOAD SUCESS")

product_erp = st.selectbox('ERP PRODUCT column:', df3.columns.tolist())
quantity_erp = st.selectbox('ERP QUANTITY column:', df3.columns.tolist())

#df1
#df3

df1_filtered = df1[product_wms].unique()
df1_filtered = pd.DataFrame(df1_filtered, columns=[product_wms])
#df1_filtered = df1_filtered.sort_values(by=product_wms, ascending=True)
df1_filtered.reset_index(inplace=True)
df1_filtered = df1_filtered.drop('index', axis=1)
df1_filtered


df3_filtered = df3[product_erp].unique()
df3_filtered = pd.DataFrame(df3_filtered, columns=[product_erp])
#df3_filtered = df3_filtered.sort_values(by='Product', ascending=True)
df3_filtered.reset_index(inplace=True)
df3_filtered = df3_filtered.drop('index', axis=1)
df3_filtered

concatenated_df = pd.concat([df1_filtered, df3_filtered], axis=1, ignore_index=True)
#concatenated_df

df1_filtered.columns = ['ProductCode']
df3_filtered.columns = ['ProductCode']

# Concatenate the two DataFrames into one column
df_unique = pd.concat([df1_filtered, df3_filtered], ignore_index=True)
df_unique = df_unique.drop_duplicates()
df_unique  = df_unique.dropna()
df_unique.reset_index(inplace=True)
df_unique = df_unique.drop('index', axis=1)
df_unique

st.markdown("#")
num_rows = len(df_unique.index)

df1s={}
df2s={}
df3s={}
dfs={}

for i in range(num_rows):
    cell_value = df_unique.iat[i, 0]
    df1s[i] = df1[df1[product_wms] == cell_value]
    df3s[i] = df3[df3[product_erp] == cell_value]
    dfs[i]= pd.concat([df1s[i], df3s[i]], axis=0,ignore_index=True)
    dfs[i] =  dfs[i][[product_wms,quantity_wms,quantity_erp]]
    dfs[i]= dfs[i].groupby([product_wms],as_index=False).sum()
    #dfs[i].rename(columns={ 'Total': 'WMS', 'CurrentQty': 'ERP'}, inplace=True)

df_final = pd.concat(dfs)
#df_final = df_final[['Product', 'Product Name', 'WMS','ERP']].copy()
df_final["var."] = df_final[quantity_wms] - df_final[quantity_erp]
#df_final = df_final[df_final['var.'] != 0]
df_final = df_final.sort_values(by='var.', ascending=True)
df_final.reset_index(inplace=True)
df_final = df_final.drop(['level_0','level_1'], axis=1)
df_final

# Function to write DataFrames to an Excel file in memory
def dfs_to_excel(df_list, sheet_list):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for dataframe, sheet in zip(df_list, sheet_list):
            dataframe.to_excel(writer, sheet_name=sheet, index=False)
    output.seek(0)
    return output

df_list = [df_final]
sheet_list = ['Sheet1']

# Convert DataFrames to Excel in memory
excel_file = dfs_to_excel(df_list, sheet_list)

# Streamlit download button
st.download_button(
    label="Download Excel file",
    data=excel_file,
    file_name=f"Stock_Tick_{today_date}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
