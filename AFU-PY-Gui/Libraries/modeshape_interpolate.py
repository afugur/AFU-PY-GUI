# -*- coding: utf-8 -*-
"""
Created on Sat May 28 17:04:13 2022

Reorder ModShape

inputs
=============

    max_modshape : DataFrame
        Mod shape max values in mods
        
        
    min_modshape : DataFrame
        Mod shape min values in mods
        
    x_coordinates : String <List>
        X Coordinates of sensors
    
    y_coordinates : String <List>
        Y Coordinates of sensors
        
    z_coordinates : String <List>
        Z Coordinates of sensors
        
        
    directions: String <List>
        Directions of sensors
        
    height : FLoat
        Height of the structure
        
    z_dim : Float
        Z-Dimension system
    
    
    ch_names: String <List>
        Channels names of the system
    
outputs
============

    
    X_max_modshape: DataFrame
        
        Columns :
                
            Z --> height of the model
        Indexes:
            
            mod {n} -- > mods of system
                
        Values:
            
            Value of every height of the model



@author: PC
"""

import re
import pandas as pd
import numpy as np
def modeshapeInterpolate(max_modshape,min_modshape,coordinate_df2,height,z_dim,ch_names):
    
    coordinate_df = pd.DataFrame()
    coordinate_df = coordinate_df2.copy()
    

    coordinate_df = coordinate_df.reset_index(drop=True)
    coordinate_df = coordinate_df.sort_values(by="Z",ascending=False)

    
    coordinate_df2 = coordinate_df["Z"].drop_duplicates()
    Z_list = coordinate_df2.values
    
    
    
    X_max_df = pd.DataFrame()
    Y_max_df = pd.DataFrame()
    for z in Z_list:
        
        X_max_df[z] = np.nan
        Y_max_df[z] = np.nan
    
    for i in max_modshape:
        
        mod = max_modshape[i]
        X_value_list = []
        Y_value_list = []
        
        for z in Z_list:
            
            
            X_name_df = coordinate_df.loc[(coordinate_df["Z"] == z) & (coordinate_df["directions"] == "X")]
            Y_name_df = coordinate_df.loc[(coordinate_df["Z"] == z) & (coordinate_df["directions"] == "Y")]
            
            X_max = mod.loc[X_name_df["name"].values].max()
            
            X_value_list.append(X_max)
            
            
            Y_max = mod.loc[Y_name_df["name"].values].max()
            
            Y_value_list.append(Y_max)
            
    
        X_max_df.loc[-1] = X_value_list  # adding a row
        X_max_df.index = X_max_df.index + 1  # shifting index
    
        Y_max_df.loc[-1] =Y_value_list  # adding a row
        Y_max_df.index = Y_max_df.index + 1  # shifting index  
            

        
    X_max_df = X_max_df.set_index(max_modshape.columns)
    Y_max_df = Y_max_df.set_index(max_modshape.columns)
    
    
    # Interpolate Mod Shapes
    
    floors = np.linspace(0,height,z_dim+1)
    
    increase = floors[1]

    x = [2, 3]
    y = [17.5, 22.5]
    X_columns = X_max_df.columns
    Y_columns = Y_max_df.columns
    for i in range(len(X_columns)):
        
        try:
            
            difference = float(X_columns[i]) - float(X_columns[i+1])
            
            if difference == increase:
                pass
            
            else:
                
                count = int(difference/increase)
                
                
                diff_floor = np.linspace(float(X_columns[i]),float(X_columns[i+1]),count+1)
                
                nonsensor_floor = diff_floor[1:-1]
                
                for z in nonsensor_floor:
                    
                    value_list = []
                    for value1,value2 in zip(X_max_df[X_columns[i]],X_max_df[X_columns[i+1]]):
                        

                        y[0] = float(X_columns[i+1])
                        y[1] = float(X_columns[i])
                        
                        x[0] = value2
                        x[1] = value1
                        
                        
                        x_new = np.interp(z, y, x)
                            
                        value_list.append(x_new)
                        
                    
                    X_max_df[z] = value_list
                        
                else:
                    pass
         
        except (IndexError,KeyError):
            pass
        
    for i in range(len(Y_columns)):
        
        try:
            
            difference = float(Y_columns[i]) - float(Y_columns[i+1])
            
            if difference == increase:
                pass
            
            else:
                
                count = int(difference/increase)
                
                
                diff_floor = np.linspace(float(Y_columns[i]),float(Y_columns[i+1]),count+1)
                
                nonsensor_floor = diff_floor[1:-1]
                
                for z in nonsensor_floor:
                    
                    value_list = []
                    for value1,value2 in zip(Y_max_df[Y_columns[i]],Y_max_df[Y_columns[i+1]]):
                        

                        y[0] = float(Y_columns[i+1])
                        y[1] = float(Y_columns[i])
                        
                        x[0] = value2
                        x[1] = value1
                        
                        
                        x_new = np.interp(z, y, x)
                            
                        value_list.append(x_new)
                        
                    
                    Y_max_df[z] = value_list
                        
                else:
                    pass
         
        except (IndexError,KeyError):
            pass
    
# Minnn DFFF
    X_min_df = pd.DataFrame()
    Y_min_df = pd.DataFrame()
    for z in Z_list:
        
        X_min_df[z] = np.nan
        Y_min_df[z] = np.nan
    
    for i in min_modshape:
        
        mod = min_modshape[i]
        X_value_list = []
        Y_value_list = []
        
        for z in Z_list:
            
            
            X_name_df = coordinate_df.loc[(coordinate_df["Z"] == z) & (coordinate_df["directions"] == "X")]
            Y_name_df = coordinate_df.loc[(coordinate_df["Z"] == z) & (coordinate_df["directions"] == "Y")]
            
            X_max = mod.loc[X_name_df["name"].values].max()
            
            X_value_list.append(X_max)
            
            
            Y_max = mod.loc[Y_name_df["name"].values].max()
            
            Y_value_list.append(Y_max)
            
    
        X_min_df.loc[-1] = X_value_list  # adding a row
        X_min_df.index = X_min_df.index + 1  # shifting index
    
        Y_min_df.loc[-1] =Y_value_list  # adding a row
        Y_min_df.index = Y_min_df.index + 1  # shifting index  
            

        
    X_min_df = X_min_df.set_index(min_modshape.columns)
    Y_min_df = Y_min_df.set_index(min_modshape.columns)
    
    
    # Interpolate Mod Shapes
    
    floors = np.linspace(0,height,z_dim+1)
    
    increase = floors[1]

    x = [2, 3]
    y = [17.5, 22.5]
    X_columns = X_min_df.columns
    Y_columns = Y_min_df.columns
    for i in range(len(X_columns)):
        
        try:
            
            difference = float(X_columns[i]) - float(X_columns[i+1])
            
            if difference == increase:
                pass
            
            else:
                
                count = int(difference/increase)
                
                
                diff_floor = np.linspace(float(X_columns[i]),float(X_columns[i+1]),count+1)
                
                nonsensor_floor = diff_floor[1:-1]
                
                for z in nonsensor_floor:
                    
                    value_list = []
                    for value1,value2 in zip(X_min_df[X_columns[i]],X_min_df[X_columns[i+1]]):
                        

                        y[0] = float(X_columns[i+1])
                        y[1] = float(X_columns[i])
                        
                        x[0] = value2
                        x[1] = value1
                        
                        
                        x_new = np.interp(z, y, x)
                            
                        value_list.append(x_new)
                        
                    
                    X_min_df[z] = value_list
                        
                else:
                    pass
         
        except (IndexError,KeyError):
            pass
        
    for i in range(len(Y_columns)):
        
        try:
            
            difference = float(Y_columns[i]) - float(Y_columns[i+1])
            
            if difference == increase:
                pass
            
            else:
                
                count = int(difference/increase)
                
                
                diff_floor = np.linspace(float(Y_columns[i]),float(Y_columns[i+1]),count+1)
                
                nonsensor_floor = diff_floor[1:-1]
                
                for z in nonsensor_floor:
                    
                    value_list = []
                    for value1,value2 in zip(Y_min_df[Y_columns[i]],Y_min_df[Y_columns[i+1]]):
                        

                        y[0] = float(Y_columns[i+1])
                        y[1] = float(Y_columns[i])
                        
                        x[0] = value2
                        x[1] = value1
                        
                        
                        x_new = np.interp(z, y, x)
                            
                        value_list.append(x_new)
                        
                    
                    Y_min_df[z] = value_list
                        
                else:
                    pass
         
        except (IndexError,KeyError):
            pass
    
    # Scale MAX --> 2
    scale_factor = 2
    
    for i in range(len(X_max_df.index)):
        
        max_value = X_max_df.iloc[i].max()
        X_max_df.iloc[i] = (X_max_df.iloc[i]/max_value)*scale_factor
        
    for i in range(len(Y_max_df.index)):
        
        max_value = Y_max_df.iloc[i].max()
        Y_max_df.iloc[i] = (Y_max_df.iloc[i]/max_value)*scale_factor   
    
    # Scale Min --> --2
    scale_mfactor = -2
    
    for i in range(len(X_min_df.index)):
        
        min_value = X_min_df.iloc[i].min()
        X_min_df.iloc[i] = (X_min_df.iloc[i]/min_value)*scale_factor
        
    for i in range(len(Y_min_df.index)):
        
        min_value = Y_min_df.iloc[i].min()
        Y_min_df.iloc[i] = (Y_min_df.iloc[i]/min_value)*scale_mfactor 
    
    X_max_df = X_max_df.reindex(sorted(X_max_df.columns), axis=1)
    X_min_df = X_min_df.reindex(sorted(X_min_df.columns), axis=1)
    Y_min_df = X_max_df.reindex(sorted(Y_min_df.columns), axis=1)
    Y_max_df = Y_max_df.reindex(sorted(Y_max_df.columns), axis=1)

    return X_min_df,X_max_df,Y_min_df,Y_max_df
        
# modeshapeInterpolate(max_modshape,min_modshape,x_coordinates,y_coordinates,z_coordinates,directions,height,z_dim,ch_names)