import streamlit as st
import pandas as pd
import plotly.express as px
import webbrowser as wb
import openpyxl
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
#from natsort import natsorted

st.set_page_config(page_title="Stock Check", page_icon="🚚", layout="wide")

st.title("🚚 Genuine Inside (M) Sdn. Bhd. - Stock Check📝")
st.markdown("##")

st.header("WMS File Upload")
data_file = st.file_uploader("WMS file",type=['xlsx'])
df1 = pd.read_excel(data_file,sheet_name="Sheet1")
df2 = pd.read_excel(data_file,sheet_name="Sheet2")
st.write("UPLOAD SUCESS")

st.markdown("#")
st.header("ERP File Upload")
data_file2 = st.file_uploader("ERP file",type=['xlsx'])
df3 = pd.read_excel(data_file2)
df3.rename(columns={'ProductCode': 'Product', 'ProductDescription': 'Product Name'}, inplace=True)
st.write("UPLOAD SUCESS")

#df1
#df2
#df3

df1_filtered = df1["Product"].unique()
df1_filtered = pd.DataFrame(df1_filtered, columns=['Product'])
df1_filtered = df1_filtered.sort_values(by='Product', ascending=True)
df1_filtered.reset_index(inplace=True)
df1_filtered = df1_filtered.drop('index', axis=1)
#df1_filtered

df2_filtered = df2["Product"].unique()
df2_filtered = pd.DataFrame(df2_filtered, columns=['Product'])
df2_filtered = df2_filtered.sort_values(by='Product', ascending=True)
df2_filtered.reset_index(inplace=True)
df2_filtered = df2_filtered.drop('index', axis=1)
#df2_filtered

df3_filtered = df3["Product"].unique()
df3_filtered = pd.DataFrame(df3_filtered, columns=['Product'])
df3_filtered = df3_filtered.sort_values(by='Product', ascending=True)
df3_filtered.reset_index(inplace=True)
df3_filtered = df3_filtered.drop('index', axis=1)
#df3_filtered

concatenated_df = pd.concat([df1_filtered, df2_filtered, df3_filtered], axis=1, ignore_index=True)
#concatenated_df

df_unique= pd.concat([df1_filtered, df2_filtered, df3_filtered])
df_unique = df_unique.drop_duplicates()
df_unique  = df_unique.dropna()
df_unique.reset_index(inplace=True)
df_unique = df_unique.drop('index', axis=1)
#df_unique

st.write("______________________________________________________________________________________")
num_rows = len(df_unique.index)

df1s={}
df2s={}
df3s={}
dfs={}

for i in range(num_rows):
    cell_value = df_unique.iat[i, 0]
    df1s[i] = df1[df1['Product'] == cell_value]
    df2s[i] = df2[df2['Product'] == cell_value]
    df3s[i] = df3[df3['Product'] == cell_value]
    dfs[i]= pd.concat([df1s[i], df2s[i], df3s[i]], axis=0,ignore_index=True)
    dfs[i] =  dfs[i][['Product','Product Name','Unnamed: 5','Quantity','BalanceQty']]
    dfs[i]= dfs[i].groupby(['Product'],as_index=False).max()
    dfs[i].rename(columns={'Unnamed: 5': 'Warehouse', 'Quantity': 'WMS', 'BalanceQty': 'ERP'}, inplace=True)
    #dfs[i]

df_final = pd.concat(dfs)
df_final["EQUAL"] = (df_final['Warehouse'] == df_final['WMS']) & (df_final['Warehouse'] == df_final['ERP'])
df_final

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df_final)

st.download_button(
    label="Download",
    data=csv,
    file_name='Stock_Check.csv',
    mime='text/csv',
)
