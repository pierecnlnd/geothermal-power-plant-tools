import pandas as pd
import numpy as np

def antoine_eq(df_,t):
    df = pd.read_excel('./backbone/antoine_coeff.xlsx')
    id_ = df_['ID'].to_list()
    df = df[df['ID'].isin(id_)]
    a = df['A'].values 
    b = df['B'].values
    c = df['C'].values
    psat = 10**(a-(b/(t+c)))
    return psat

def raults_law(psat,p):
    ki = psat*0.00133322/p
    return ki

def flash_calc_gs(df_,f,p,t):
    result = {}
    err_li = []
    psat = antoine_eq(df_,t)
    ki = raults_law(psat,p)
    zi = df_['Zi'].values
    ziFi = zi*100
    v_arr = np.linspace(0.0,100,10000)
    for v in v_arr:
        l = 100-v
        yi = ziFi/(v+(l/ki))
        xi = yi/ki
        err = abs(np.sum(yi)-1)
        # print(v/100*f, err)
        df_result = df_
        df_result['psat'] = psat*0.00133322
        df_result['Ki'] = ki
        df_result['Xi'] = xi
        df_result['Yi'] = yi
        result[err] = {
            'V':v/100*f,
            'L':f-v/100*f,
            'df':df_result,
            'err':err
        }
        err_li.append(err)
    # print(np.min(err))
    return result[np.min(err)]
    