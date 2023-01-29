import pandas as pd 
import re
import os 
import numpy as np
import itertools
import threading
import time
import sys

def v2toData(files,folder,word="(UNITS: CM/SEC/SEC)",word2="(UNITS: CM/SEC)"):
    

    word = word
    word2 = word2

    fs = float()  
    f_index = int() 
    velo_index = int() 
    data_df = pd.Series(dtype=float)
    data_df2 = pd.DataFrame()
    datas = pd.DataFrame(dtype=float)
    
    
    files = [c for c in files if c[-3::] == ".V2"]

    for file in files:
        index = 0
        v_index = 0
        b = []
        f = open(folder+'/'+file,"r")
        lines = f.readlines()
        
        for line in lines:
            
            index += 1
            if word in line:
                f_index = index
                
        
        for line in lines:
            v_index += 1
            if word2 in line:
                velo_index = v_index - 1
        
        
        for i in range(f_index,velo_index):
        
            line = lines[i]
            b.append(re.findall(r"[-+]?\d*\.\d+|\d+", line))
            
    
        
        datas = pd.DataFrame(b,dtype=float)
        values = datas.values
        sort_val = values.flatten()
        
        data = pd.DataFrame(sort_val)
        data = data.dropna()
        
        value = data.values
        value = value.flatten()
        
        data_df[file] = value
        
        
        f.close()
    try:
        
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

    except IndexError:
        
        word = "cm/sec2."
        word2 = "cm/sec."
        
        return v2toData(files,folder,word="cm/sec2.",word2="cm/sec.")
        
        



# files = ['CHAN001.V2', 'CHAN001.V3', 'CHAN002.V2', 'CHAN002.V3', 'CHAN003.V2', 'CHAN003.V3', 'CHAN004.V2', 'CHAN004.V3', 'CHAN005.V2', 'CHAN005.V3', 'CHAN006.V2', 'CHAN006.V3', 'CHAN007.V2', 'CHAN007.V3', 'CHAN009.V2', 'CHAN009.V3', 'CHAN010.V2', 'CHAN010.V3', 'CHAN011.V2', 'CHAN011.V3', 'CHAN012.V2', 'CHAN012.V3', 'CHAN014.V2', 'CHAN014.V3', 'CHAN015.V2', 'CHAN015.V3', 'CHAN016.V2', 'CHAN016.V3']
# folder = "C:/Users/PC/Desktop/SMC AFU PY/CE24386/AFUPY/Data/chinohills_ci14383980"

# v2toData(files,folder)