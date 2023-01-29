# -*- coding: utf-8 -*-
"""
Created on Sun May 29 16:18:13 2022

ModShape Drawing with Sensors Modal Displacements


inputs
=============

    X_df : DataFrame
        Mod shape values in X
        
        
    Y_df : DataFrame
        Mod shape values in Y
        
        
    length: FLoat
        Length of the system
    
    width : Float 
        Width of the system
        
    
    height: FLoat
        Height of the system
        
    z_dim : Int
        Dimension of Z direction
    
    mod: Int
        index of mod
        
outputs
============

    
    modshape : Figure
    
        Every mods modshape in model coordinates


@author: PC
"""

import numpy as np
import matplotlib.pyplot as plt


def modeshapeSensorDrawing(self,X_df,Y_df,length,width,height,z_dim,mod):
    
    
    length_increase = X_df.iloc[mod]
    length_list = length_increase.values
    
        
    width_increase = Y_df.iloc[mod]
    width_list = width_increase.values
    
    center = [length/2 , width/2, height/2]
    
    ox, oy, oz = center
    l, w, h = [length,width,height]
    
    x = np.linspace(ox-l/2,ox+l/2,num=3) 
    y = np.linspace(oy-w/2,oy+w/2,num=3)
    z = np.linspace(oz-h/2,oz+h/2,num=z_dim)
    
    x1, z1 = np.meshgrid(x, z)
    y11 = np.ones_like(x1)*(oy-w/2)
    y12 = np.ones_like(x1)*(oy+w/2)
    x2, y2 = np.meshgrid(x, y)
    z21 = np.ones_like(x2)*(oz-h/2)
    z22 = np.ones_like(x2)*(oz+h/2)
    y3, z3 = np.meshgrid(y, z)
    x31 = np.ones_like(y3)*(ox-l/2)
    x32 = np.ones_like(y3)*(ox+l/2)
    
    # fig = plt.figure()
    # self.ay = fig.gca(projection='3d')
    # outside surface
    self.ay.clear()
    self.ay.plot_wireframe(x1, y11, z1, color='gray',alpha=0.7) # front
    # inside surface
    self.ay.plot_wireframe(x1, y12, z1, color='gray',alpha=0.7) # behind
    
    self.ay.plot_wireframe(x2, y2, z21, color='grey',alpha=0.7) # below
    # bottom surface
    self.ay.plot_wireframe(x2, y2, z22, color='grey',alpha=0.7) # top
    # left surface
    self.ay.plot_wireframe(x31, y3, z3, color='gray',alpha=0.7) # left
    # right surface
    self.ay.plot_wireframe(x32, y3, z3, color='gray',alpha=0.7) # right
    

    # outside surface

    # bottom surface

    
    for i,l in zip(range(len(x1)),length_list):

        x1[i] = x1[i] + l
        
    for i,w in zip(range(len(y11)),width_list):
        
        y11[i] = y11[i] + w

    for i,w in zip(range(len(y12)),width_list):
        
        y12[i] = y12[i] + w
        
    self.ay.plot_wireframe(x1, y11, z1, color='red') # front
    # inside surface
    self.ay.plot_wireframe(x1, y12, z1, color='red') # behind
        
    for i,l in zip(range(len(x31)),length_list):
        
        x31[i] = x31[i] + l
        
    for i,l in zip(range(len(x32)),length_list):
        
        x32[i] = x32[i] + l   
    
    for i,w in zip(range(len(y3)),width_list):
        
        y3[i] = y3[i] + w
        
    self.ay.plot_wireframe(x31, y3, z3, color='red') # left
    # right surface
    self.ay.plot_wireframe(x32, y3, z3, color='red') # right
        
    for i in range(len(y2)):

        y2[i] = y2[i] + width_list[0]
        
    for i in range(len(x2)):
        
        x2[i] = x2[i] + length_list[0]   
        
    self.ay.plot_wireframe(x2, y2, z21, color='red') # below
    
    x2, y2 = np.meshgrid(x, y)
    z21 = np.ones_like(x2)*(oz-h/2)
    z22 = np.ones_like(x2)*(oz+h/2)
    
    for i in range(len(y2)):

        y2[i] = y2[i] + width_list[-1]
        
    for i in range(len(x2)):
        
        x2[i] = x2[i] + length_list[-1] 
    
    self.ay.plot_wireframe(x2, y2, z22, color='red') # top
    
    
    self.ay.set_xlabel('X')
    self.ay.set_ylabel('Y')
    self.ay.set_zlabel('Z')
    
    self.chart_type5.draw()
    

# modeshapeSensorDrawing(X_mself.ay_df,Y_mself.ay_df,50,18,22.5,10,5)