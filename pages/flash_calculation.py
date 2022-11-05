import streamlit as st
import pandas as pd
import numpy as np
from backbone.flash_calc_gs import *
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

st.header('Components')

df = pd.read_excel('./backbone/antoine_coeff.xlsx')
df = df[['Formula', 'Compound Name', 'ID']]

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination(paginationAutoPageSize=True) 
gb.configure_side_bar() 
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gridOptions = gb.build()

grid_response = AgGrid(
    df,
    gridOptions=gridOptions,
    df_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=False,
    enable_enterprise_modules=True,
    height=350, 
    width='100%',
    reload_df=True
)

data = grid_response['data']
selected = grid_response['selected_rows']
df_selected = pd.DataFrame(selected) 

is_assign = False
if len(selected) > 0:
    st.header('Selected')
    AgGrid(
        df_selected[['Formula', 'Compound Name', 'ID']],
        # gridOptions=gridOptions,
        height=350,
        width='100%',
        update_mode='MODEL_CHANGED',
        reload_df=True
    )
    st.header('Assign Parameters')
    with st.form('assign_Zi'):
        n = len(df_selected['Formula'].to_list())
        formula = df_selected['Formula'].to_list()
        compound_name = df_selected['Compound Name'].to_list()
        Zi = ['' for i in range(n)]
        for i in range(n):
            Zi[i] = float(st.text_input(label='Zi for {} ({})'.format(compound_name[i],formula[i]),value=0))
        f = float(st.text_input(label='Total Feed (kmol/hr)',value=1))
        t = float(st.text_input(label='Temperature (C)',value=0))
        p = float(st.text_input(label='Pressure (bar)',value=0))
        col1, col2, col3= st.columns(3)
        submitted = col2.form_submit_button("Submit")
        if submitted:
            df_selected['Zi'] = Zi
            result = flash_calc_gs(df_selected,f,p,t)
            is_assign = True

if is_assign:
    st.header('Result')
    col1, col2, col3= st.columns(3)
    col2.write('V = {} kmol/hr'.format(result['V']))
    col2.write('L = {} kmol/hr'.format(result['L']))
    AgGrid(
        result['df'][['Formula','Compound Name', 'psat', 'Ki', 'Zi', 'Xi', 'Yi']],
        # gridOptions=gridOptions,
        height=350,
        width='100%',
        update_mode='MODEL_CHANGED',
        reload_df=True
    )
    col2.write('Done with error {}'.format(result['err']))

