# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 13:27:59 2022

@author: PC
"""

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os
from tkinter import messagebox
import pandas as pd
from PIL import Image, ImageTk
import requests
from bs4 import BeautifulSoup
import zipfile
import shutil
from Libraries import read_V2,read_version_V2,calcFdd,half_power,log_damp,calc_Drift,calc_modeshape,modeshape_interpolate,draw_maxmodeshape,draw_minmodeshape
import numpy as np
import datetime

p1_file = os.path.dirname(os.path.realpath(__file__))


class resultsPage(tk.Toplevel):
    
    def __init__(self, main):
    
        super().__init__()
        
        self.geometry('1050x800')
        self.title("Results")
        self.resizable(True,True)
        
        self.mod_df = pd.read_excel(p1_file + "/Calculation/Event.xlsx",sheet_name="mods")
        self.half_df = pd.read_excel(p1_file + "/Calculation/Event.xlsx",sheet_name="damp_half")
        self.log_df = pd.read_excel(p1_file + "/Calculation/Event.xlsx",sheet_name="damp_log")
        
        mods_fq = [x for x in self.mod_df]
        
        self.event_names = mods_fq[0]
        mods_fq = mods_fq[1::]
        
        mf_frame = Frame(self, relief=RIDGE, borderwidth=4)
        mf_frame.grid(row=0,column=0)
        
        mod_label = Label(mf_frame,text="Modal Frequencies - Events",font=("Arial",12,"underline","bold"))
        mod_label.pack()
        
        self.mod_mq = ttk.Combobox(mf_frame,width=15,height=3,state="readonly",justify="center")
        self.mod_mq["values"] = mods_fq
        self.mod_mq.pack()
        
        self.mf_figure = plt.Figure(figsize=(13,7),dpi=60,tight_layout=True)
        self.mf = self.mf_figure.add_subplot(111)
        
        self.mf.set_xlabel("Events")
        self.mf.set_ylabel("Modal Frequencies")
        self.chart_type = FigureCanvasTkAgg(self.mf_figure,mf_frame)
        self.chart_type.get_tk_widget().pack(padx=10,pady=5)
        

        dp_frame = Frame(self, relief=RIDGE, borderwidth=4)
        dp_frame.grid(row=1,column=0)
        
        dp_label = Label(dp_frame,text="Half Power - Events",font=("Arial",12,"underline","bold"))
        dp_label.pack()
        
        self.mod_dr = ttk.Combobox(dp_frame,width=15,height=3,state="readonly",justify="center")
        self.mod_dr["values"] = mods_fq
        self.mod_dr.pack()
        
        self.dp_figure = plt.Figure(figsize=(13,7),dpi=60,tight_layout=True)
        self.dp = self.dp_figure.add_subplot(111)
        
        self.dp.set_xlabel("Damping Ratios")
        self.dp.set_ylabel("Events")
        self.chart_type2 = FigureCanvasTkAgg(self.dp_figure,dp_frame)
        self.chart_type2.get_tk_widget().pack(padx=10,pady=5)


        lr_frame = Frame(self, relief=RIDGE, borderwidth=4)
        lr_frame.grid(row=1,column=1)
        
        lr_label = Label(lr_frame,text="Logarithmic - Events",font=("Arial",12,"underline","bold"))
        lr_label.pack()
        
        self.mod_lr = ttk.Combobox(lr_frame,width=15,height=3,state="readonly",justify="center")
        self.mod_lr["values"] = mods_fq
        self.mod_lr.pack()
        
        self.lr_figure = plt.Figure(figsize=(13,7),dpi=60,tight_layout=True)
        self.lr = self.lr_figure.add_subplot(111)
        
        self.lr.set_xlabel("Damping Ratios")
        self.lr.set_ylabel("Events")
        self.chart_type3 = FigureCanvasTkAgg(self.lr_figure,lr_frame)
        self.chart_type3.get_tk_widget().pack(padx=10,pady=5)
        
        
        dr_frame = Frame(self, relief=RIDGE, borderwidth=4)
        dr_frame.grid(row=0,column=1)
        
        dr_label = Label(dr_frame,text="Drift - Events",font=("Arial",12,"underline","bold"))
        dr_label.pack()
        
        
        self.dr_figure = plt.Figure(figsize=(13,7),dpi=60)
        self.dr = self.dr_figure.add_subplot(111)
        
        self.dr.set_xlabel("Events")
        self.dr.set_ylabel("Drift Ratios")
        self.chart_type4 = FigureCanvasTkAgg(self.dr_figure,dr_frame)
        self.chart_type4.get_tk_widget().pack(padx=10,pady=5)
        
        self.mod_mq.bind('<<ComboboxSelected>>', self.showMF)
        self.mod_dr.bind('<<ComboboxSelected>>', self.showDR)
        self.mod_lr.bind('<<ComboboxSelected>>', self.showLR)
        
    def showMF(self,event):
        
        mod = self.mod_mq.get()
        

        labels = [x for x in self.mod_df[self.event_names]]
        labels.sort()
        self.mod_df["Events"] = pd.to_datetime(self.mod_df.Events)
        self.mod_df = self.mod_df.sort_values(by="Events")
        self.mod_df[self.event_names] = labels
        
        ranges = range(0,len(labels),1)
        
        self.mf.clear()
        self.mf.set_xlabel("Events")
        self.mf.set_ylabel("Modal Frequencies")
        self.mf.plot(self.mod_df[self.event_names],self.mod_df[mod],lw=1,linestyle = "dashed", marker = '>', ms= '20', mec= 'r')
        self.mf.set_xticks(ranges,labels,rotation=45,fontsize=10)
        
        self.chart_type.draw()
        
        
    def showDR(self,event):
        
        mod = self.mod_dr.get()
        labels = [x for x in self.mod_df[self.event_names]]
        labels.sort()
        self.mod_df["Events"] = pd.to_datetime(self.mod_df.Events)
        self.mod_df = self.mod_df.sort_values(by="Events")
        self.mod_df[self.event_names] = labels
        ranges = range(0,len(labels),1)
        
        self.dp.clear()
        self.dp.set_xlabel("Events")
        self.dp.set_ylabel("Damping Ratios")
        self.dp.plot(self.half_df[self.event_names],self.half_df[mod],lw=1,linestyle = "dashed", marker = '>', ms= '20', mec= 'r',mfc='orange')
        self.dp.set_xticks(ranges,labels,rotation=45,fontsize=10)
        
        self.chart_type2.draw()
        
    def showLR(self,event):
        
        mod = self.mod_lr.get()
        labels = [x for x in self.mod_df[self.event_names]]
        labels.sort()
        self.mod_df["Events"] = pd.to_datetime(self.mod_df.Events)
        self.mod_df = self.mod_df.sort_values(by="Events")
        self.mod_df[self.event_names] = labels
        ranges = range(0,len(labels),1)
        
        self.lr.clear()
        self.lr.set_xlabel("Events")
        self.lr.set_ylabel("Damping Ratios")
        self.lr.plot(self.log_df[self.event_names],self.log_df[mod],lw=1,linestyle = "dashed", marker = '>', ms= '20', mec= 'r',mfc='green')
        self.lr.set_xticks(ranges,labels,rotation=45,fontsize=10)
        
        self.chart_type3.draw()   
        

class showAnalysiss(tk.Toplevel):
    
    def __init__(self, main,data_df,fs_df,coordinate_df):
    
        super().__init__()
        
        self.data_df = data_df
        self.fs_df = fs_df
        self.coordinate_df = coordinate_df
        
        self.coordinate_df = pd.read_excel("sensors_df.xlsx")
        
        self.geometry('1400x900')
        self.title("Accelerations")
        self.resizable(True,True)
        
        fdd_frame = Frame(self, relief=RIDGE, borderwidth=4)

        fdd_frame.pack(side=LEFT,anchor="nw")
        
        self.windows_value = DoubleVar()
        self.overlap_value = DoubleVar()
        
        
        label_fdd = Label(fdd_frame,text="FDD Graph",font=("Arial",12,"underline","bold"))
        label_fdd.pack(anchor="w")
        
        self.windowing = ttk.Combobox(fdd_frame,width=15,height=3,state="readonly",justify="center",textvariable=self.windows_value)
        self.windowing["value"] = [256,512,1024,2048,4096,8192,16348]
        self.overlap = ttk.Combobox(fdd_frame,width=15,height=3,state="readonly",justify="center",textvariable=self.overlap_value)
        self.overlap["value"] = [0.33,0.66,1.0]
        
        label_fdd = Label(fdd_frame,text="Windowing",font=("Arial",10))
        label_fdd.pack(anchor="w")
        
        self.windowing.pack(anchor="w")
        
        label_fdd = Label(fdd_frame,text="Overlap",font=("Arial",10))
        label_fdd.place(x=240,y=23)
        
        calc_button = Button(fdd_frame,text="Calculate FDD",command=self.calc_FDD,bg="cyan")
        
        self.overlap.place(x=210,y=45)
        calc_button.place(x=380,y=40)
        
        self.fdd_figure = plt.Figure(figsize=(7,7),dpi=70)
        self.fd = self.fdd_figure.add_subplot(111)
        
        self.fd.set_xlabel("Frequency (Hz)")
        self.fd.set_ylabel("r'dB $[g^2/Hz]$'")
        self.chart_type = FigureCanvasTkAgg(self.fdd_figure,fdd_frame)
        self.chart_type.get_tk_widget().pack(anchor="n",side=RIGHT,pady=5)
        
        table_frame = Frame(self, relief=RIDGE, borderwidth=4)

        table_frame.pack(side=LEFT,anchor="n")
        
        table_label = Label(table_frame,text="Mod Table",font=("Arial",12,"underline","bold"))
        table_label.pack()
        self.ttv_mod = ttk.Treeview(table_frame)
        self.ttv_mod.bind("<Double-1>", self.OnDoubleClick)
        self.ttv_mod.pack()
        
        self.x_figure = plt.Figure(figsize=(4,4),dpi=70)
        self.ax = self.x_figure.gca(projection='3d')
        
        self.chart_type4 = FigureCanvasTkAgg(self.x_figure,table_frame)
        self.chart_type4.get_tk_widget().pack(padx=10,pady=5,side=LEFT,anchor="w")
        
        
        self.y_figure = plt.Figure(figsize=(4,4),dpi=70)
        self.ay = self.y_figure.gca(projection='3d')
        
        
        self.chart_type5 = FigureCanvasTkAgg(self.y_figure,table_frame)
        self.chart_type5.get_tk_widget().pack(padx=10,pady=5,side=RIGHT)
        
        
        aa = Label(self,text="Drift Table",font=("Arial",12,"underline","bold"))
        aa.place(x=10,y=580)
        
        columns = ["Floors","X-Relative Disp.","X-Drift","Y-Relative Disp","Y-Drift"]
        self.ttv_drift = ttk.Treeview(self,columns=columns, show='headings')
        
        self.ttv_drift.heading('Floors', text='Floors')
        self.ttv_drift.heading('X-Relative Disp.', text='X-Relative Disp.')
        self.ttv_drift.heading('X-Drift', text='X-Drift')
        self.ttv_drift.heading('Y-Relative Disp', text='Y-Relative Disp')
        self.ttv_drift.heading('Y-Drift', text='Y-Drift')
        

        self.ttv_drift.place(x=10,y=610)
        
        
    def OnDoubleClick(self,event):
        fs = 1/self.fs_df["fs"][0]
        item = self.ttv_mod.identify('item',event.x,event.y)
        values = self.ttv_mod.item(item)
        modfreq = values["values"][0]
        modfreq = float(modfreq)
        
        lines = self.fd.axvline(x=modfreq, color='red', linestyle='--')
        
        mod_shapes = calc_modeshape.calcModeShape(self.data_df,[modfreq],fs=fs)
        
        max_modshape = mod_shapes[0]
        min_modshape = mod_shapes[1]
        
        height = 22.5
        z_dim = 9
        length = 50
        width = 18
        ch_names = self.data_df.columns.values
        modeshape_interpolate2 = modeshape_interpolate.modeshapeInterpolate(max_modshape,min_modshape,self.coordinate_df,height,z_dim,ch_names)
        
        X_df_max = modeshape_interpolate2[1]
        Y_df_max = modeshape_interpolate2[3]
        
        # Drawing modshapes
        
        modeshapefig = draw_maxmodeshape.modeshapeSensorDrawing(self,X_df_max,Y_df_max,length,width,height,z_dim,0)
        
        X_df_max = modeshape_interpolate2[0]
        Y_df_max = modeshape_interpolate2[2]
        
        modeshapefig = draw_minmodeshape.modeshapeSensorDrawing(self,X_df_max,Y_df_max,length,width,height,z_dim,0)
        
        self.chart_type.draw()
        
        lines.remove()
        
    def calc_FDD(self):
        
        windowing = float(self.windowing.get())
        overlap = float(self.overlap.get())*100
        fs = 1/self.fs_df["fs"][0]
        self.fd.clear()
        fdd = calcFdd.calcFDD(self,self.data_df.values,fs,(fs/2)/windowing,overlap=overlap)

        mod_freqs = []
        for modfreq in fdd.values:
            
            for freq in modfreq:
                mod_freqs.append(float(freq))
    
        mod_freqs = list(set(mod_freqs))
        mod_freqs = mod_freqs[0:6]
        mod_freqs.sort()
        
        data = self.data_df
        self.mods = mod_freqs
        columns = self.data_df.columns
        
        windowing = int(windowing)
        # # Damping Ratios
        self.damp_half = half_power.dampHalf(data,self.mods,fs=fs,samples=windowing,overlap=overlap/100)
        self.damp_log = log_damp.dampLog(data,self.mods,fs=fs,samples=windowing,overlap=overlap/100,length=2000)
        
        self.modfreq_df = pd.DataFrame()
        
        damp_col = self.damp_half.columns.values
        
        for i in range(len(damp_col)):
            
            self.modfreq_df[damp_col[i]] = [self.mods[i]]
            
        indexes = self.damp_half.index
        columns = self.damp_half.columns
        

        trans_df = self.modfreq_df.T
        indexes = self.damp_half.index
        columns = self.damp_half.columns
        # self.modfreq_df = self.modfreq_df.rename(columns={0: "Mod Freq"})
        
        # self.damp_half = self.damp_half.T
        # self.damp_half = self.damp_half.rename(columns={0: "Half-Power"})

        # self.damp_log = self.damp_log.T
        # self.damp_log = self.damp_log.rename(columns={0: "Log-Decrement"})
        
        # print(self.modfreq_df)
        

        
        result_df = pd.DataFrame(data=[self.modfreq_df.iloc[0].values,self.damp_half.iloc[0].values,self.damp_log.iloc[0].values]
                                 ,index=["Mod Freq","Half-Power","Log-Decrement"],columns=columns)
        
        result_df = result_df.T
        
        result_df = result_df.round(3)
        col = list(result_df.columns)
        self.ttv_mod["columns"]=(col)
        
        for i in self.ttv_mod.get_children():
            self.ttv_mod.delete(i)
        
        for x in col:
            self.ttv_mod.column(x,width=20)
            self.ttv_mod.heading(x, text=x)
            
        result_df = result_df.sort_index()
        for index, row in  result_df.iterrows():
            
            self.ttv_mod.insert("",0,text=index,values=list(row))
            
        self.chart_type.draw()
            
        height = 22.5
        z_dim = 9
        drift = calc_Drift.calcDrift(self.data_df, self.coordinate_df, fs, height, z_dim)
            
        X_rel = drift[0].values
        Y_rel = drift[1].values
        X_Drift = drift[2].values
        Y_Drift = drift[3].values

        
        
        floors = drift[0].index
        for i in range(len(floors)):

            self.ttv_drift.insert('', tk.END, values=(floors[i],round(X_rel[i],2),round(X_Drift[0][i],2),round(Y_rel[i],2),round(Y_Drift[0][i],2)))
            
            
            
class showAccData(tk.Toplevel):
    
    def __init__(self, main,station_net,data_file,data_df,fs,time,fs_df,coordinate_df):
    
        super().__init__()
        
        self.geometry('1100x400')
        self.title("Accelerations")
        self.resizable(False,False)
        
        self.data_df = data_df
        self.fs = fs
        self.fs_df = fs_df
        self.time = time
        self.coordinate_df = coordinate_df
        
        # List X
        self.x_list = []
        self.y_list = []
        self.z_list = []
        self.n_list = []
        self.direc_list = []
        
        self.station_net = station_net
        self.data_file = data_file
        
        data_label = Label(self,text="Data Files")
        data_label.pack(anchor="nw",padx=5)
        
        data_folder = p1_file + "/Data"
        data_files = os.listdir(data_folder)
        
        self.data_combobox = ttk.Combobox(self,width=12,state="readonly",justify="center", postcommand = self.updateList)
        self.data_combobox["values"] = data_files
        self.data_combobox.pack(anchor="nw",padx=5,pady=5)
        
        self.Lb1 = Listbox(self)
        self.Lb1.pack(side=LEFT,anchor="nw",padx=5,pady=10)
        
        show_data = Button(self,text="Show Value",bg="#66CDAA",width=15,command=self.showData)
        show_data.place(x=10,y=240)
        
        channel_frame = Frame(self, relief=RIDGE, borderwidth=4)
        channel_frame.place(x=150,y=23)
        
        channel_name = Label(channel_frame,text="Channel Name",font=("Arial",12,"bold"))
        channel_name.pack()
        
        self.channel_name =  ttk.Combobox(channel_frame,width=15,height=3,state="readonly",justify="center")
        self.channel_name.pack(pady=5)
        
        
        self.x_figure = plt.Figure(figsize=(6,4),dpi=70)
        self.ax = self.x_figure.add_subplot(111)
        
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Acceleration (cm/s)")
        self.chart_type = FigureCanvasTkAgg(self.x_figure,channel_frame)
        self.chart_type.get_tk_widget().pack(padx=10,pady=5)
        
        sensor_frame = Frame(self, relief=RIDGE, borderwidth=4)
        sensor_frame.place(x=610,y=23)
        
        channel_name = Label(sensor_frame,text="Sensor Placement",font=("Arial",12,"bold"))
        channel_name.pack()
        
        
        X_name = Label(sensor_frame,text="X",font=("Arial",10))
        X_name.pack()
        
        self.X_direction = Entry(sensor_frame,justify="center")
        self.X_direction.pack(pady=5)
        
        X_name = Label(sensor_frame,text="Y",font=("Arial",10))
        X_name.pack()
        
        self.Y_direction = Entry(sensor_frame,justify="center")
        self.Y_direction.pack(pady=5)
        
        X_name = Label(sensor_frame,text="Z",font=("Arial",10))
        X_name.pack()
        
        self.Z_direction = Entry(sensor_frame,justify="center")
        self.Z_direction.pack(pady=5)
        
        X_name = Label(sensor_frame,text="Direction",font=("Arial",10))
        X_name.pack()
        
        self.direction =  ttk.Combobox(sensor_frame,width=15,height=3,state="readonly",justify="center")
        self.direction["values"] = ["X","Y","Z"]
        self.direction.pack(pady=5)
        
        place = Button(sensor_frame,text="Place Sensor",command=self.placeSensor)
        place.pack(pady=5)
        
        model_frame = Frame(self, relief=RIDGE, borderwidth=4)
        model_frame.place(x=790,y=23)
        
        channel_name = Label(model_frame,text="Model",font=("Arial",12,"bold"))
        channel_name.pack()
        

        self.model = plt.Figure(figsize=(4,4),dpi=70)
        self.ad = self.model.gca(projection='3d')
        
        height = 22.5
        width = 18
        length = 50
        
        center = [length/2 , width/2, height/2]
        
        ox, oy, oz = center
        l, w, h = [length,width,height]
        
        x = np.linspace(ox-l/2,ox+l/2,num=3) 
        y = np.linspace(oy-w/2,oy+w/2,num=3)
        z = np.linspace(oz-h/2,oz+h/2,num=10)
        x1, z1 = np.meshgrid(x, z)
        y11 = np.ones_like(x1)*(oy-w/2)
        y12 = np.ones_like(x1)*(oy+w/2)
        x2, y2 = np.meshgrid(x, y)
        z21 = np.ones_like(x2)*(oz-h/2)
        z22 = np.ones_like(x2)*(oz+h/2)
        y3, z3 = np.meshgrid(y, z)
        x31 = np.ones_like(y3)*(ox-l/2)
        x32 = np.ones_like(y3)*(ox+l/2)
        
        # outside surface
        self.ad.plot_wireframe(x1, y11, z1, color='gray') # front
        # inside surface
        self.ad.plot_wireframe(x1, y12, z1, color='gray') # behind
        # bottom surface
        self.ad.plot_wireframe(x2, y2, z21, color='gray') # below
        # upper surface
        self.ad.plot_wireframe(x2, y2, z22, color='gray') # top
        # left surface
        self.ad.plot_wireframe(x31, y3, z3, color='gray') # left
        # right surface
        self.ad.plot_wireframe(x32, y3, z3, color='gray') # right
        self.ad.set_xlabel('X')
        self.ad.set_ylabel('Y')
        self.ad.set_zlabel('Z')

        self.chart_type2 = FigureCanvasTkAgg(self.model,model_frame)
        self.chart_type2.get_tk_widget().pack(anchor="e",side=TOP)
        
        self.channel_name.bind('<<ComboboxSelected>>', self.showPlot)
        
        
        set_sensors = Button(model_frame,text="Set Channels",command=self.setchannels)
        
        set_sensors.pack(pady=10)
        
    def setchannels(self):
        
        self.coordinate_df["X"] = self.x_list
        self.coordinate_df["Y"] = self.y_list
        self.coordinate_df["Z"] = self.z_list
        self.coordinate_df["name"] = self.n_list
        self.coordinate_df["directions"] = self.direc_list
        
    def updateList(self):
        
        data_folder = p1_file + "/Data/"+ self.data_combobox.get() + "/"
        data_files = os.listdir(data_folder)
        
        self.Lb1.delete(0,END)
        for i in range(len(data_files)):
            
            self.Lb1.insert(i, data_files[i])
            
            
    def showData(self):
        
        # self.data_df = pd.DataFrame()
        # self.fs = float()
        # self.time = pd.DataFrame()
        
        self.x_list = []
        self.y_list = []
        self.z_list = []
        self.direc_list = []
        
        for i in self.Lb1.curselection():

            data_folder = p1_file + "/Data/"+ self.data_combobox.get() + "/" +  self.Lb1.get(i)
            data_files = os.listdir(data_folder)
        
            files = [c for c in data_files if c[-3::] == ".V2"]
            
            if len(files) > 1:
                
                data = read_V2.v2toData(files, data_folder)
                data_df = data[0]
                
                self.fs = data[1]
                self.time["time"] = data[2]
                
                self.channel_name["values"] = list(data_df.columns)
                
            elif len(files) == 1:
                
                read_version_V2.versionV2(files)
                
        for i in data_df:
            
            self.data_df[i] = data_df[i]
            

        self.fs_df["fs"] = [self.fs]

        
    def showPlot(self,event):

        self.ax.clear()
        self.ax.plot(self.time.values,self.data_df["{0}".format(self.channel_name.get())])
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Acceleration (cm/s)")
        self.chart_type.draw()
         
        
    def placeSensor(self):
        
        x = float(self.X_direction.get())
        y = float(self.Y_direction.get())
        z = float(self.Z_direction.get())
        name = self.channel_name.get()
        direct = self.direction.get()
        
        self.x_list.append(x)
        self.y_list.append(y)
        self.z_list.append(z)
        self.n_list.append(name)
        self.direc_list.append(direct)
    
        place_fig = self.ad.scatter(self.x_list, self.y_list, self.z_list, color='red',lw=6)
        

        
        self.chart_type2.draw()
            
class mainApplication(tk.Tk):
    
    def __init__(self):
        
        super().__init__()
        
        self.geometry('350x330')
        self.title("AFU-PY")
        self.resizable(False,False)
        
        # Data Variable
        
        self.data_df = pd.DataFrame()
        self.fs_df = pd.DataFrame()
        self.time = pd.DataFrame()
        self.coordinate_df = pd.DataFrame()
        
        self.station_net = str()
        
        p1_file = os.path.dirname(os.path.realpath(__file__))
        self.files = os.listdir(p1_file)
        download_check = [s for s in self.files if "Download" in s]
        data_check = [s for s in self.files if "Data" in s]
        self.p1_file = p1_file
        
        if download_check == []:
        
            self.download_file = os.mkdir(p1_file+"/Download")
            self.download_file = p1_file+"/Download"
        else:
            
            self.download_file = p1_file+"/Download"
            
        if data_check == []:
        
            self.data_file = os.mkdir(p1_file+"/Data")
            self.data_file = p1_file+"/Data"
        else:
            
            self.data_file = p1_file+"/Data"
        
        file_frame = Frame(self, relief=RIDGE, borderwidth=4)
        file_frame.pack(side=LEFT, anchor=NW)
        
        
        file_label = Label(file_frame,text="Web Harvesting",font=("Arial",16,"underline"))
        file_label.pack(pady=5)
        
        kandilli_label = Label(file_frame,text="KANDILLI",font=("Arial",12,"underline"))
        kandilli_label.pack(pady=5)
        
        self.photo = PhotoImage(file = r"koeri3d2.gif")
        
        kandilli_button = Button(file_frame,image=self.photo,width=200,height=50,command=self.Showkandilli)
        kandilli_button.pack()
        
        kandilli_label = Label(file_frame,text="CESMD",font=("Arial",12,"underline"))
        kandilli_label.pack(pady=5)
        
        kandilli_label = Label(file_frame,text="Station Network ID (ex. CE24386)",font=("Arial",10))
        kandilli_label.pack(pady=5)
        
        self.photo2 = PhotoImage(file = r"cesmd.PNG")
        
    
        self.station_entry = Entry(file_frame,width=18,justify="center")
        self.station_entry.pack()
        
        cesmd_button = Button(file_frame,image=self.photo2,width=200,height=50,command=self.Showcesmd)
        cesmd_button.pack(pady=5)
        
        downloadevent_button = Button(file_frame,width=15,bg="green",text="Download Event",command=self.download_event)
        downloadevent_button.pack(pady=5)
        
        table_frame = Frame(self, relief=RIDGE, borderwidth=4)
        table_frame.pack(pady=10)
        
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        frmtreeborder = tk.LabelFrame(table_frame,text='Event Table')
        
        frmtreeborder.columnconfigure(0, weight=1)
        frmtreeborder.rowconfigure(0, weight=1)
        
        self.event_treeview = ttk.Treeview(frmtreeborder,show="headings")
        
        Hscroll = ttk.Scrollbar(table_frame,orient=tk.HORIZONTAL,command=self.event_treeview.xview)
        Vscroll = ttk.Scrollbar(table_frame,orient=tk.VERTICAL,command=self.event_treeview.yview)
        self.event_treeview.configure(xscrollcommand=Hscroll.set)
        self.event_treeview.configure(yscrollcommand=Vscroll.set)
                
        frmtreeborder.grid(column=0,row=0,sticky='nsew',padx=6,pady=6)
        self.event_treeview.grid(column=0,row=0,sticky='nsew',padx=6,pady=6)
        Hscroll.grid(row=1,column=0,sticky='ew')
        Vscroll.grid(row=0,column=1,sticky='ns')
        
        menubar = Menu(self,background='#ff8000', foreground='black', activebackground='white', activeforeground='black')
        
        menu_Modelling = Menu(menubar, tearoff=0)
        menu_Modelling.add_command(label="Acceleration",command=self.showData)
        menubar.add_cascade(label="Acceleration", menu=menu_Modelling)
        
        menu_Analysis = Menu(menubar, tearoff=0)
        
        menu_Analysis.add_command(label="Analysis",command=self.showAnalysis)
        menubar.add_cascade(label="Analysis", menu=menu_Analysis)
        
        menu_ShowTerm = Menu(menubar, tearoff=0)
        
        menu_ShowTerm.add_command(label="Results",command=self.showResults)
        menubar.add_cascade(label="Results", menu=menu_ShowTerm)
        
        self.config(menu=menubar)
        self.event_treeview.bind('<<TreeviewSelect>>', self.item_selected)
        
    def showAnalysis(self):
        
        showAnalysiss(self,self.data_df,self.fs_df,self.coordinate_df)
        
    def showData(self):
        
        self.data_df = pd.DataFrame()
        self.fs = float()
        self.time = pd.DataFrame()
        showAccData(self,self.station_net,self.data_file,self.data_df,self.fs,self.time,self.fs_df,self.coordinate_df)
        
        
    def showResults(self):
        
        
        resultsPage(self)
        
        
    def Showkandilli(self):
        self.geometry('1050x330')
        html = "http://www.koeri.boun.edu.tr/scripts/lst0.asp"
        cont = requests.get(html)
        soup = BeautifulSoup(cont.content,"html.parser")
        table = soup.find("pre").contents[0]
        
        file = open("Kandilli"+".txt","w")
        file.writelines(table)
        file.close()
        
        file = open("Kandilli"+".txt","r")
        text = file.readlines()
        file.close()
        
        data1 = []

        for i in range(14,1016,2):
            veriler1 = text[i]
            veriler1 = veriler1.split()
            data1.append(veriler1)
        
        del data1[500]
        
        kandilli_df = pd.DataFrame(data1)
        kandilli_df = kandilli_df.rename(columns={0: "Tarih", 1: "Saat"
                                                ,2: "Enlem(N)",
                                                3:"Boylam(E)",4:"Derinlik(km)",
                                                5:"MD",6:"ML",7:"Mw",8:"Yer",9:"Çözüm Niteliği"})
        
        
        cols = list(kandilli_df.columns)
        kandilli_df = kandilli_df[cols[0:9]]
        cols = list(kandilli_df.columns)
        
        for i in  self.event_treeview.get_children():
            self.event_treeview.delete(i)
            
            
        self.event_treeview["columns"] = cols
        

            
        for i in cols:
            self.event_treeview.column(i, anchor="w",stretch=False)
            self.event_treeview.heading(i, text=i, anchor='w')
        
        for index, row in kandilli_df.iterrows():
            self.event_treeview.insert("",0,text=index,values=list(row))
            
        
        
    def Showcesmd(self):
        
        self.geometry('1050x330')
        
        network = self.station_entry.get()[0:2]
        station = self.station_entry.get()[2::]
        
        link = "https://www.cesmd.org/cgi-bin/CESMD/Multiplesearch1_DM2.pl?event_name=&magmin=&magmax=&byear=&eyear=&country=Any&state=Any&stn_ident=&network={0}&sta_number={1}&type=Any&Material=Any&Height=&siteclass=Any&accmin=&accmax=&hdistmin=&hdistmax=".format(network,station)
        
        pd_table = pd.read_html(link)
        
        event_table = pd_table[4]
        
        drop_list = []
        
        for i in range(len(event_table["Station"].values)):
            
        
            if str(event_table["Station"][i]) == "nan":
                
                drop_list.append(i)
            
            
        event_table = event_table.drop(axis=1,index=drop_list)
        event_table = event_table.reset_index(drop=True)
        
        cols = list(event_table.columns)
        
        for i in  self.event_treeview.get_children():
            self.event_treeview.delete(i)
        
        self.event_treeview["columns"] = cols
    
        for i in cols:
            self.event_treeview.column(i, anchor="w",stretch=False)
            self.event_treeview.heading(i, text=i, anchor='w')
        
        for index, row in event_table.iterrows():
            self.event_treeview.insert("",0,text=index,values=list(row))
            
    def item_selected(self,event):
        
        self.curItems = self.event_treeview.selection()
        
        self.event_list = []
        self.event_name = []
        for i in self.curItems:
            
            a = self.event_treeview.item(i)['values']
            self.event_name.append(a[7])
            self.event_list.append(a[10])
        
    def download_event(self):
        
        download_check = [s for s in self.files if "Download" in s]

        if download_check == []:
        
            self.download_file = os.mkdir(self.p1_file+"/Download")
            self.download_file = self.p1_file+"/Download"
        else:
            
            self.download_file = self.p1_file+"/Download"
        
        chunk_size = 128
        station_net = self.station_entry.get()
        self.station_net = station_net
        self.save_list = []
        for i,name in zip(self.event_list,self.event_name):
            
        
            url = "https://www.strongmotioncenter.org/wserv/records/query?eventid={0}&stcode={1}&orderby=epidist-asc&rettype=dataset&download=P&email=&groupby=station&nodata=404".format(i,station_net)
            
            r = requests.get(url, stream=True)
            save_path = self.download_file +"/" + str(name) + "_" + str(i) +".zip"
            event_name = str(name) + "_" + str(i)
            self.save_list.append(save_path)
            with open(save_path, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    fd.write(chunk)
                    
                    
                    
        for i,file in zip(self.save_list,self.event_name):
            
            try: 
                
                zip_file = i
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(i.split(".zip")[0])
                    
                zip_ref.close()
                
                new_file = os.listdir(i.split(".zip")[0])
                enter_file = i.split(".zip")[0] + "/"+ new_file[0]
                new_file2 = os.listdir(enter_file)
                enter_file2 = enter_file +"/" +new_file2[0]
                zip_file = os.listdir(enter_file2)
            
                zip_file = enter_file2 + "/"  + zip_file[0]
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(enter_file2 + "/" + file)
    
                zip_ref.close()
                
                afu_data = self.data_file + "/"+ station_net +"/" + file
                shutil.move(enter_file2 + "/" + file, afu_data)
            except zipfile.BadZipfile:
                
                pass
            
            
        shutil.rmtree(self.download_file)
        

                
                
        
        
mainApplication().mainloop() 
