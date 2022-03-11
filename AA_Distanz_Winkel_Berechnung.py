#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import math
from math import sin
from math import cos
from math import radians
import GUI



def load_prepare_data(): # Loading the measurement data generated in the first step # Static: vehicle or person # Dynamic: moving vehicle or moving person:
    global data
    pfad = GUI.pfadUebergabe()
    print("Chosen file path: ", pfad)
    data = pd.read_csv(pfad, header=None, skiprows = 8, sep=" ")    
    data.pop(3) # Unnötige Intensitätsspalte entfernen
    data.rename(columns = {0:'x_true', 1:'y_true', 2:'z_true'}, inplace = True) # Spalten neu benennen
    print("Scenario data successfully loaded from data set")
    #print(data)
    #return data
    


def calc_distances(): # Calculation of the distance from the x-, y-, and z-coordinates:
    print("Calculating true distances and angles")
    entfernung = []
    for i, row in data.iterrows():
        distanz = ((np.square(row[0]) + np.square(row[1]) + np.square(row[2]))**(1/2)) # distanz = radius vom Sensor zum Punkt
        entfernung.append(distanz) # Die berechneten Distanz für jede Zeile wird der Liste "entfernung" hinzugefügt
        #print(distanz)
    data['Distanz_true'] = entfernung # Spalte mit berechneten Distanzinformationen zum Datenframe hinzufügen und füllen mit den berechneten Distanzen
    #return distanz



def calc_angles(): # Calculation of theta and phi angles:
    # Neue Spalten mit dem Theta- und Phi-Winkel einfügen und mit dummy-Wert beschreiben
    data['Theta'] = 0
    data['Phi'] = 0

    # Transformationsgleichungen von kartesischen Koordinaten in Kugelkoordinaten
    theta = [] # in Radiant berechnet !!!!
    phi = [] # in Radiant berechnet !!!!
   
    # ++++++ (row[0]) entspricht x ++++++ #
    # ++++++ (row[1]) entspricht y ++++++ #
    # ++++++ (row[2]) entspricht z ++++++ #

    for i, row in data.iterrows():
    
        # Theta berechnen:
        theta_wert = ((math.pi/2) - np.arctan(row[2] / ((np.square(row[0]) + np.square(row[1]))**(1/2)))) # in Radiant
        theta.append(theta_wert)
    
        # Phi berechnen
        if row[1] >= 0:
            phi_wert = np.arccos(row[0] / ((np.square(row[0]) + np.square(row[1]))**(1/2))) 
            phi.append(phi_wert)
            #print('y ist größer= 0')
    
        else:
            phi_wert = 2 * math.pi - np.arccos(row[0] / ((np.square(row[0]) + np.square(row[1]))**(1/2)))
            phi.append(phi_wert)
            #print('y ist kleiner 0')
        
        #print(theta_wert)
        #print(phi_wert)

    # In die zuvor bereits erstellten Spalten "Theta" und "Phi" nun auch die Listen für theta und phi mit den Werten einfügen
    data['Theta'] = theta
    data['Phi'] = phi
    #return data



def save_data(): # Save the data:
    # Abspeichern der x-, y-, z-Koordinaten, und der berechneten Distanzwerte und Winkel
    # OLD: absolute Path: C:\Users\kevin\Desktop\Carla\Carla_0.9.11\PythonAPI\examples\...
    data.to_csv(r'data\lidar_data\2_Distanz_Winkel_Berechnung\x_true_y_true_z_true_dist_theta_phi\x_true_y_true_z_true_dist_theta_phi.txt', sep=" ", header=None, index=None) 
    
    # Entfernen der x-, y-, und z-Distanzwerte
    data.pop('x_true')
    data.pop('y_true')
    data.pop('z_true')
    data.pop('Theta')
    data.pop('Phi')

    # Ausschließlich abspeichern der berechnetet Pixeldistanzen
    # OLD: absolute Path: C:\Users\kevin\Desktop\Carla\Carla_0.9.11\PythonAPI\examples\...
    data.to_csv(r'data\lidar_data\2_Distanz_Winkel_Berechnung\dist_true\dist_true.txt', sep=" ", header=None, index=None) 
    print("True distance and angle data saved")
    
    #return data
