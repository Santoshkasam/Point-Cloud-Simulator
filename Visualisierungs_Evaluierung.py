#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
#from open3d import *
import pptk
import laspy as lp
import open3d as o3d
from pyntcloud import PyntCloud
#import GUI


# ===========================
# - Visualize point clouds - 
# ===========================
pcd_true = o3d.io.read_point_cloud(r'data\Visualization\classical_method\BG8_LR10\newUpdate_42477.txt', format='xyz') 
pcd_pred = o3d.io.read_point_cloud(r'data\Visualization\classical_method\BG8_LR10\x_pred_y_pred_z_pred.txt', format='xyz') 

o3d.visualization.draw_geometries([pcd_true], window_name = 'Ground Truth Point Cloud', width = 1920, height = 1000, left = 0)     
o3d.visualization.draw_geometries([pcd_pred], window_name = 'Predicted Truth Point Cloud', width = 1920, height = 1000, left = 0)   


# Berechnen der Distanzen der zwischen den Pixeln in der True PC und der Predicted PC 
dists = pcd_true.compute_point_cloud_distance(pcd_pred)
dists = np.asarray(dists)
print('\n distances between true pcd pixels and pred pcd pixels: \n', dists, '\n')

np.savetxt(r'data\Visualization\classical_method\BG8_LR10\abstaende_zw_Pixeln.txt', dists, fmt='%.4f', encoding='utf8')#, delimiter=",") #sep=" ", header=None, index=None) 


Average_distance = np.mean(dists)
print('Average distance from pcd_true to pcd_pred: ', Average_distance)
Average_distance_np_save = np.array(Average_distance, ndmin=1) # to be able to save this 0d array with "np.savetxt..."
np.savetxt(r'data\Visualization\classical_method\BG8_LR10\abstaende_Mittelwert.txt', Average_distance_np_save, fmt='%.6f', encoding='utf8')#, delimiter=",") #sep=" ", header=None, index=None) 

std_distance = np.std(dists)
print('Standard deviation from pcd_true to pcd_pred: ', std_distance, '\n')
std_distance_np_save = np.array(std_distance, ndmin=1)
np.savetxt(r'data\Visualization\classical_method\BG8_LR10\abstaende_std.txt', std_distance_np_save, fmt='%.6f', encoding='utf8')#, delimiter=",") #sep=" ", header=None, index=None) 





# ====================================================
# - Visualisieren der beiden Punktwolken in Relation - 
# ====================================================
#ind = np.where(dists < 1)[0]
#pcdTrue_without_pcdPred = pcd_true.select_by_index(ind)
#o3d.visualization.draw_geometries([pcdTrue_without_pcdPred], width = 1920, height = 1000, left = 0)




