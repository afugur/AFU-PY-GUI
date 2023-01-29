# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 23:52:30 2022

@author: afugur
"""

import pandas as pd
import re 
import numpy as np
def versionV2(file):
    
    f = open(file,"r")

    lines = f.readlines()
    f.close()
    
    word="(UNITS: CM/SEC/SEC)"
    word2="(UNITS: CM/SEC)"
    index = 0
    v_index = 0
    data_df = pd.Series(dtype=float)
    data_df2 = pd.DataFrame()
    f_index = int()
    
    l_aindex = []
    
    v_aindex = []
    
    for line in lines:
        
        index += 1
        if word in line:
            f_index = index
            l_aindex.append(f_index)
    
    for line in lines:
        v_index += 1
        if word2 in line:
            velo_index = v_index - 1
            v_aindex.append(velo_index)
    for i in range(len(v_aindex)):
            
        b = []
        for a in range(l_aindex[i],v_aindex[i]):
            
        
            b.append((re.findall(r"[-+]?\d*\.\d+|\d+", lines[a])))
        
        datas = pd.DataFrame(b,dtype=float)
        values = datas.values
        sort_val = values.flatten()
        
        data = pd.DataFrame(sort_val)
        data = data.dropna()
        
        value = data.values
        value = value.flatten()
            
        data_df["ch {}".format(i+1)] = value 
        
    fs = re.findall("\.\d+", lines[f_index-1])      
    fs = float(fs[0])
    
    time = np.arange(0,len(data_df[0]) * float(fs),float(fs))
    
    indexes = data_df.index.values
    
    length_data = data_df.values
    
    min_list = []
    
    for i in range(len(data_df)):
        
        min_list.append(len(length_data[i]))
    
    min_value = min(min_list)
    for i in range(len(data_df)):
        
        data_df2[indexes[i]] = length_data[i][0:min_value]
    
    return data_df2,fs,time
