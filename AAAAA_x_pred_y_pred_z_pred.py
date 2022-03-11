#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import math
from math import sin
from math import cos
from math import radians


def prepare_data():

    global winkel
    # Loading the file with all coordinates + distances + angles from the second step  
    #C:\Users\kevin\Desktop\Carla\Carla_0.9.11\PythonAPI\examples\
    winkel = pd.read_csv(r'data\lidar_data\2_Distanz_Winkel_Berechnung\x_true_y_true_z_true_dist_theta_phi\x_true_y_true_z_true_dist_theta_phi.txt', header=None, sep=" ")

    # Remove the x_true, y_true, z_true values and the true_distance # Only Theta and Phi remain
    winkel.pop(0)
    winkel.pop(1)
    winkel.pop(2)
    winkel.pop(3)

    # ========================================================================
    # -- Loading the distances predicted by the neural network ---------------
    # - Choose which data of the NN should be loaded -------------------------
    # - Selection = "klassisch" / "prediction" / "weighted" / "threshold" / -
    # -           "pointgroup" -----------------------------------------------
    # ========================================================================
    # global Selection
    # Selection = "classical"

    # if Selection == "classical":
    #     pred_dist = pd.read_csv(r'data\neuralNet_predictions\classical_distance.txt', header=None, sep=" ")

    # elif Selection == "prediction":
    #     pred_dist = pd.read_csv(r'data\neuralNet_predictions\prediction_distance.txt', header=None, sep=" ")

    # elif Selection == "weighted":
    #     pred_dist = pd.read_csv(r'data\neuralNet_predictions\prediction_distance_weighted.txt', header=None, sep=" ")

    # elif Selection == "threshold":
    #     pred_dist = pd.read_csv(r'data\neuralNet_predictions\prediction_distance_weighted_tresh70.txt', header=None, sep=" ")

    # elif Selection == "pointgroup":
    #     pred_dist = pd.read_csv(r'data\neuralNet_predictions\prediction_distance_steven.txt', header=None, sep=" ")

    # else:
    #     print("You need to make a choice for the NN Evaluation!")
    
    # print("Data with distances and angles and NN predictions loaded successfully")

    pred_dist = np.loadtxt(r'data\lidar_data\prediction_distance.txt')

    # Als Spalte an die Winkel-Daten hinzufügen
    winkel['pred_dist'] = pred_dist

    # Benennen der Spalten
    winkel.rename(columns = {4:'theta', 5:'phi'}, inplace = True)

    # Einmal durchiterieren, damit gleich alle "row[x]" verwendet werden können
    for i, row in winkel.iterrows():
        dummyVariable = 3 # irgendein Vorgang, der keinen Einfluss auf den eigentichen Prozess hat
    
    print("Data preparation completed")



def calc_coordinates(): # Retransformation from spherical coordinates to cartesian coordinates

    # ++++++ row[0] = theta ++++++ #
    # ++++++ row[1] = phi ++++++ #
    # ++++++ row[2] = pred_distance = Radius ++++++ #

    x_pred = [] 
    y_pred = []
    z_pred = []

    for i, row in winkel.iterrows():
        
        # x_pred berechnen:
        x_pred_wert = row[2] * sin(row[0]) * cos(row[1])
        x_pred.append(x_pred_wert)
        
        # y_pred berechnen:
        y_pred_wert = row[2] * sin(row[0]) * sin(row[1])
        y_pred.append(y_pred_wert)
        
        # z_pred berechnen:
        z_pred_wert = row[2] * cos(row[0])
        z_pred.append(z_pred_wert)
        
        #print(x_pred_wert)
        #print(y_pred_wert)
        #print(z_pred_wert)

    # Adding the Cartesian coordinates calculated from the predictions to the data frame
    # Dataframe structure: "theta, phi, pred_dist, x_pred, y_pred, z_pred"
    winkel['x_pred'] = x_pred
    winkel['y_pred'] = y_pred
    winkel['z_pred'] = z_pred

    print("Coordinates calculated successfully")


def save_data():

    # Abspeichern aller pred_Daten
    #winkel.to_csv(r'C:\Users\kevin\Desktop\Carla\Carla_0.9.11\PythonAPI\examples\data\lidar_data\4_x_pred_y_pred_z_pred_Berechnung\theta_phi_dist_pred_x_pred_y_pred_z_pred.txt', sep=" ", header=None, index=None)
    # Abspeichern nur der predicted x-, y- und z-Koordinaten
    #winkel.pop('theta')
    #winkel.pop('phi')
    #winkel.pop('pred_dist')
    #winkel.to_csv(r'C:\Users\kevin\Desktop\Carla\Carla_0.9.11\PythonAPI\examples\data\lidar_data\4_x_pred_y_pred_z_pred_Berechnung\x_pred_y_pred_z_pred.txt', sep=" ", header=None, index=None)

    # if Selection == "classical":
    #     winkel.to_csv(r'data\lidar_data\4_x_pred_y_pred_z_pred_Berechnung\classical\theta_phi_dist_pred_x_pred_y_pred_z_pred.txt', sep=" ", header=None, index=None)
    #     winkel.pop('theta')
    #     winkel.pop('phi')
    #     winkel.pop('pred_dist')
    #     winkel.to_csv(r'data\lidar_data\4_x_pred_y_pred_z_pred_Berechnung\classical\x_pred_y_pred_z_pred.txt', sep=" ", header=None, index=None)

    # elif Selection == "prediction":
    #     winkel.to_csv(r'data\lidar_data\4_x_pred_y_pred_z_pred_Berechnung\prediction\theta_phi_dist_pred_x_pred_y_pred_z_pred.txt', sep=" ", header=None, index=None)
    #     winkel.pop('theta')
    #     winkel.pop('phi')
    #     winkel.pop('pred_dist')
    #     winkel.to_csv(r'data\lidar_data\4_x_pred_y_pred_z_pred_Berechnung\prediction\x_pred_y_pred_z_pred.txt', sep=" ", header=None, index=None)

    # elif Selection == "weighted":
    #     winkel.to_csv(r'data\lidar_data\4_x_pred_y_pred_z_pred_Berechnung\weighted\theta_phi_dist_pred_x_pred_y_pred_z_pred.txt', sep=" ", header=None, index=None)
    #     winkel.pop('theta')
    #     winkel.pop('phi')
    #     winkel.pop('pred_dist')
    #     winkel.to_csv(r'data\lidar_data\4_x_pred_y_pred_z_pred_Berechnung\weighted\x_pred_y_pred_z_pred.txt', sep=" ", header=None, index=None)

    # elif Selection == "threshold":
    #     winkel.to_csv(r'data\lidar_data\4_x_pred_y_pred_z_pred_Berechnung\threshold\theta_phi_dist_pred_x_pred_y_pred_z_pred.txt', sep=" ", header=None, index=None)
    #     winkel.pop('theta')
    #     winkel.pop('phi')
    #     winkel.pop('pred_dist')
    #     winkel.to_csv(r'data\lidar_data\4_x_pred_y_pred_z_pred_Berechnung\threshold\x_pred_y_pred_z_pred.txt', sep=" ", header=None, index=None)

    # elif Selection == "pointgroup":
    #     winkel.to_csv(r'data\lidar_data\4_x_pred_y_pred_z_pred_Berechnung\pointgroup\theta_phi_dist_pred_x_pred_y_pred_z_pred.txt', sep=" ", header=None, index=None)
    #     winkel.pop('theta')
    #     winkel.pop('phi')
    #     winkel.pop('pred_dist')
    #     winkel.to_csv(r'data\lidar_data\4_x_pred_y_pred_z_pred_Berechnung\pointgroup\x_pred_y_pred_z_pred.txt', sep=" ", header=None, index=None)
    # else:
    #     print("You need to make a choice for the NN Evaluation!")

    winkel.to_csv(r'data\lidar_data\4_x_pred_y_pred_z_pred_Berechnung\theta_phi_dist_pred_x_pred_y_pred_z_pred.txt', sep=" ", header=None, index=None)
    winkel.pop('theta')
    winkel.pop('phi')
    winkel.pop('pred_dist')
    winkel.to_csv(r'data\lidar_data\4_x_pred_y_pred_z_pred_Berechnung\x_pred_y_pred_z_pred.txt', sep=" ", header=None, index=None)
    print("Coordinates saved")