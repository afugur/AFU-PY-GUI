# -*- coding: utf-8 -*-
"""
Created on Mon May 23 22:59:36 2022


Calculate Drift Ratio

inputs
=============

    Data: DataFrame
        Acceleration values of sensors
        
    x_coordinates : String <List>
        X Coordinates of sensors
    
    y_coordinates : String <List>
        Y Coordinates of sensors
        
    z_coordinates : String <List>
        Z Coordinates of sensors
        
    fs : Float
        Sampling Rate
        
    directions: String <List>
        Directions of sensors
        
    height : FLoat
        Height of the structure
    z_dim : Float
        Z-Dimension system
    
    
outputs
============

    X_relative_disp : DataFrame
        X relative displacement values of sensors
    Y_relative_disp : DataFrame
        Y relative displacement values of sensors
    X_drift_df : DataFrame
        X direction Drift values of sensors
    Y_drift_df : DataFrame
        Y direction Drift values of sensors

        
        

@author: PC
"""

from Libraries.omegaArithmetic import intf
import pandas as pd
import numpy as np
import re

def calcDrift(data,coordinate_df,fs,height,z_dim):
    

    coordinate_df2 = coordinate_df.copy()
    coordinate_df2["X"] = coordinate_df["X"].drop_duplicates()

    
    coordinate_df2 = coordinate_df2.dropna()

    combine = np.array(np.meshgrid(coordinate_df2["X"].values, coordinate_df2["Y"].values)).T.reshape(-1,len(coordinate_df2))
    
    list_length = []

    for i in combine:
        

        # calc_df = coordinate_df['X'] == i[0] and coordinate_df['Y'] == i[1]
        
        calc_df = coordinate_df.loc[(coordinate_df['X'] == i[0]) & (coordinate_df['Y'] == i[1])]
        list_length.append(len(calc_df))
        
        
    
    max_list_length = max(list_length)

    max_index = list_length.index(max_list_length)
        
    select_combine = combine[max_index]
    
    select_df = coordinate_df.loc[(coordinate_df['X'] == select_combine[0]) & (coordinate_df['Y'] == select_combine[1])]
    select_df = select_df.reset_index(drop=True)
    select_df = select_df.sort_values(by="Z",ascending=False)
    
    x_df = select_df.loc[select_df["directions"] == "X"]
    y_df = select_df.loc[select_df["directions"] == "Y"]
    
    
    # XXXXX
    
    X_disp_df = pd.DataFrame()
    
    Y_disp_df = pd.DataFrame()
    
    for column in x_df["name"]:
        
        read = intf(data[column],
                    int(fs),
        f_lo= 0.0 , f_hi=100 , 
            times=2 , winlen=1
            , unwin=False)
            
        out = read
        X_disp_df[column] = out
    
    for column in y_df["name"]:
        
        read = intf(data[column],
                    int(fs),
        f_lo= 0.0 , f_hi=100 , 
            times=2 , winlen=1
            , unwin=False)
            
        out = read
        Y_disp_df[column] = out
        
    floors = np.linspace(0,height,z_dim+1)
    
    increase = floors[1]

    x_df = x_df.reset_index(drop=True)
    y_df = y_df.reset_index(drop=True)
    
    x = [2, 3]
    y = [17.5, 22.5]
    
    list_floor = []
    str_floor = []
    X_floor = []
    Y_floor = []
    direc_list = []
    nonsensor_df = pd.DataFrame()
    nonsensor_disp_df = pd.DataFrame()
    for i in range(len(x_df["Z"])):
        
        try:
            
            difference = x_df["Z"][i] - x_df["Z"][i+1]
            
            if difference == increase:
                pass
            
            else:
                
                count = int(difference/increase)
                
                
                diff_floor = np.linspace(x_df["Z"][i],x_df["Z"][i+1],count+1)
                
                nonsensor_floor = diff_floor[1:-1]
                
                for z in nonsensor_floor:
                    
                    X_floor.append(x_df["X"][0])
                    Y_floor.append(x_df["Y"][0])
                    direc_list.append("X")
                    list_floor.append(z)
                    str_floor.append(str(z))
                    
                    value_list = []
                    for value1,value2 in zip(X_disp_df[x_df["name"][i]],X_disp_df[x_df["name"][i+1]]):
                        
                    
                        y[0] = x_df["Z"][i+1]
                        y[1] = x_df["Z"][i]
                        
                        x[0] = value2
                        x[1] = value1
                        
                        
                        x_new = np.interp(z, y, x)
                            
                        value_list.append(x_new)
                        
                    
                    nonsensor_disp_df[str(z)] = value_list
                        
                else:
                    pass
         
        except (IndexError,KeyError):
            pass
        

    if x_df["Z"][len(x_df["Z"])-1] != floors[1]:
        
        
        la = (x_df["Z"][len(x_df["Z"])-1])/increase
        
        first_floors = np.linspace(floors[0],x_df["Z"][len(x_df["Z"])-1],int(la)+1)
        
        first_floors = first_floors[1:-1]
        
        
        for z in first_floors:
            
            X_floor.append(x_df["X"][0])
            Y_floor.append(x_df["Y"][0])
            direc_list.append("X")
            list_floor.append(z)
            str_floor.append(str(z))
            value_list = []
            for value1 in X_disp_df[str(x_df["name"][len(x_df["name"])-1])]:
                
            
                y[0] = 0
                y[1] = x_df["Z"][len(x_df["Z"])-1]
                
                x[0] = 0
                x[1] = value1


                x_new = np.interp(z, y, x)
                    
                value_list.append(x_new)
                
            
            nonsensor_disp_df[str(z)] = value_list
       
    for i in nonsensor_disp_df:
        
        X_disp_df[i] = nonsensor_disp_df[i].values
    
    
    nonsensor_df["X"] = X_floor
    nonsensor_df["Y"] = Y_floor
    nonsensor_df["Z"] = list_floor
    nonsensor_df["name"] = str_floor
    nonsensor_df["directions"] = direc_list
    
    x_df = pd.concat([x_df,nonsensor_df])
    x_df = x_df.reset_index(drop=True)
    x_df["Z"] = x_df["Z"].drop_duplicates()
    x_df = x_df.dropna()
    x_df = x_df.sort_values(by="Z",ascending=False)
    x_df = x_df.reset_index(drop=True)
    
    X_relative_disp = pd.DataFrame()
    
    for i in range(len(x_df)):
        
        try:
            

            X_relative_disp["Z({0}-{1})".format(x_df["Z"][i],x_df["Z"][i+1])] = X_disp_df[x_df["name"][i]] - X_disp_df[x_df["name"][i+1]]
            X_relative_disp["Z({0}-{1})".format(x_df["Z"][i],x_df["Z"][i+1])] = abs(X_relative_disp["Z({0}-{1})".format(x_df["Z"][i],x_df["Z"][i+1])])
        except KeyError:
            
            X_relative_disp["Z({0}-0)".format(x_df["Z"][i])] = X_disp_df[x_df["name"][i]]
            X_relative_disp["Z({0}-0)".format(x_df["Z"][i])] = abs(X_relative_disp["Z({0}-0)".format(x_df["Z"][i])])
            pass
    
    X_relative_disp = X_relative_disp.max()
    X_drift_df = pd.DataFrame()
    
    for i in range(len(x_df)):
        
        try:

            
            X_drift_df["Z({0}-{1})".format(x_df["Z"][i],x_df["Z"][i+1])] = [(X_relative_disp[i] / x_df["Z"][i])]
        
        except KeyError:
            
            X_drift_df["Z({0}-0)".format(x_df["Z"][i])] = [(X_relative_disp[i] / x_df["Z"][i])]
    
# YYYYYYYYYYY basliyor

    x = [2, 3]
    y = [17.5, 22.5]
    
    list_floor = []
    str_floor = []
    X_floor = []
    Y_floor = []
    direc_list = []
    nonsensor_df = pd.DataFrame()
    nonsensor_disp_df = pd.DataFrame()
    for i in range(len(y_df["Z"])):
        
        try:
            
            difference = y_df["Z"][i] - y_df["Z"][i+1]
            
            if difference == increase:
                pass
            
            else:
                
                count = int(difference/increase)
                
                
                diff_floor = np.linspace(y_df["Z"][i],y_df["Z"][i+1],count+1)
                
                nonsensor_floor = diff_floor[1:-1]
                
                for z in nonsensor_floor:
                    
                    X_floor.append(y_df["X"][0])
                    Y_floor.append(y_df["Y"][0])
                    direc_list.append("X")
                    list_floor.append(z)
                    str_floor.append(str(z))
                    
                    value_list = []
                    for value1,value2 in zip(Y_disp_df[y_df["name"][i]],Y_disp_df[y_df["name"][i+1]]):
                        
                    
                        y[0] = y_df["Z"][i+1]
                        y[1] = y_df["Z"][i]
                        
                        x[0] = value2
                        x[1] = value1
                        
                        
                        x_new = np.interp(z, y, x)
                            
                        value_list.append(x_new)
                        
                    
                    nonsensor_disp_df[str(z)] = value_list
                        
                else:
                    pass
         
        except (IndexError,KeyError):
            pass
        

    if y_df["Z"][len(y_df["Z"])-1] != floors[1]:
        
        
        la = (y_df["Z"][len(y_df["Z"])-1])/increase
        
        first_floors = np.linspace(floors[0],y_df["Z"][len(y_df["Z"])-1],int(la)+1)
        
        first_floors = first_floors[1:-1]
        
        
        for z in first_floors:
            
            X_floor.append(y_df["X"][0])
            Y_floor.append(y_df["Y"][0])
            direc_list.append("X")
            list_floor.append(z)
            str_floor.append(str(z))
            value_list = []
            for value1 in Y_disp_df[str(y_df["name"][len(y_df["name"])-1])]:
                
            
                y[0] = 0
                y[1] = y_df["Z"][len(y_df["Z"])-1]
                
                x[0] = 0
                x[1] = value1


                x_new = np.interp(z, y, x)
                    
                value_list.append(x_new)
                
            
            nonsensor_disp_df[str(z)] = value_list
       
    for i in nonsensor_disp_df:
        
        Y_disp_df[i] = nonsensor_disp_df[i].values
    
    
    nonsensor_df["X"] = X_floor
    nonsensor_df["Y"] = Y_floor
    nonsensor_df["Z"] = list_floor
    nonsensor_df["name"] = str_floor
    nonsensor_df["directions"] = direc_list
    
    y_df = pd.concat([y_df,nonsensor_df])
    y_df = y_df.reset_index(drop=True)
    y_df["Z"] = y_df["Z"].drop_duplicates()
    y_df = y_df.dropna()
    y_df = y_df.sort_values(by="Z",ascending=False)
    y_df = y_df.reset_index(drop=True)
    
    Y_relative_disp = pd.DataFrame()
    
    for i in range(len(y_df)):
        
        try:
            

            Y_relative_disp["Z({0}-{1})".format(y_df["Z"][i],y_df["Z"][i+1])] = Y_disp_df[y_df["name"][i]] - Y_disp_df[y_df["name"][i+1]]
            Y_relative_disp["Z({0}-{1})".format(y_df["Z"][i],y_df["Z"][i+1])] = abs(Y_relative_disp["Z({0}-{1})".format(y_df["Z"][i],y_df["Z"][i+1])])
        except KeyError:
            
            Y_relative_disp["Z({0}-0)".format(y_df["Z"][i])] = Y_disp_df[y_df["name"][i]]
            Y_relative_disp["Z({0}-0)".format(y_df["Z"][i])] = abs(Y_relative_disp["Z({0}-0)".format(y_df["Z"][i])])
            pass
    
    Y_relative_disp = Y_relative_disp.max()
    Y_drift_df = pd.DataFrame()
    
    for i in range(len(y_df)):
        
        try:

            
            Y_drift_df["Z({0}-{1})".format(y_df["Z"][i],y_df["Z"][i+1])] = [(Y_relative_disp[i] / y_df["Z"][i])]
        
        except KeyError:
            
            Y_drift_df["Z({0}-0)".format(y_df["Z"][i])] = [(Y_relative_disp[i] / y_df["Z"][i])]
            


    return X_relative_disp,Y_relative_disp,X_drift_df,Y_drift_df
    
# calcDrift(data,x_coordinates,y_coordinates,z_coordinates,50,directions,22.5,9)