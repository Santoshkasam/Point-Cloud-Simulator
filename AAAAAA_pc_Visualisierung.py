#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
#from open3d import *
#import pptk
#import laspy as lp
import open3d as o3d
#from pyntcloud import PyntCloud
import GUI


def calc_pointClouds():
    

    # vis = o3d.visualization.Visualizer()
    # vis.create_window()
    # pcd_true = o3d.io.read_point_cloud(r'data\Visualization\Prediction_with_bg_subtraction\BG5_LR10\x_pred_y_pred_z_pred.txt', format='xyz') #r'data\lidar_data\Datensatz\Dynamic\Test\42477.txt', format='xyz')
    
    # #cam = o3d.camera.set_intrinsics(width=640, height=480, fx=575.816, fy=575.816, cx=320.0, cy=240.0)
    # #cam.intrinsic_matrix = [[3131.02, 0.00, 1505.62], [0.00, 3131.02, 2004.13], [0.00, 0.00, 1.00]]


    
    # vis.add_geometry(pcd_true.voxel_down_sample(voxel_size=0.000001))

    # extrinsic = np.array([[1, 2, 3, 4],
    #                     [5, 6, 7, 8], 
    #                     [9, 10, 11, 12],
    #                     [13, 14, 15, 16]])

    # o3d.camera.PinholeCameraParameters(extrinsic)

    # ctr = vis.get_view_control()
    # # print("Field of view (before changing) %.2f" % ctr.get_field_of_view())
    # # ctr.change_field_of_view(step=20)
    # # print("Field of view (after changing) %.2f" % ctr.get_field_of_view())

    # vis.run()





    # =============================
    # - Fast test visualizations - 
    # =============================
    # vis = o3d.visualization.Visualizer()
    # vis.create_window()
    # #pcd_pred = o3d.io.read_point_cloud(r'data\lidar_data\4_x_pred_y_pred_z_pred_Berechnung\x_pred_y_pred_z_pred.txt', format='xyz') 
    # pcd = o3d.io.read_point_cloud(r'data\Visualization\Prediction_with_bg_subtraction\BG2_LR10\x_pred_y_pred_z_pred.txt', format='xyz') 
    # vis.add_geometry(pcd)
    # vis.run()


    # =============================
    # - Ground Truth point cloud - 
    # =============================
    pfad_true = GUI.pfadUebergabe()
    vis_true = o3d.visualization.Visualizer()
    vis_true.create_window()
    pcd_true = o3d.io.read_point_cloud(pfad_true, format='xyz') #r'data\lidar_data\Datensatz\Dynamic\Test\42477.txt', format='xyz')
    vis_true.add_geometry(pcd_true)
    vis_true.run()
    vis_true.capture_screen_image('ground_truth_pc.png')    # Saves an image of the point cloud

    print(pcd_true) # Angabe wie viele Punkte die Punktwolke hat


    # ================================
    # - Predicted Truth point cloud - 
    # ================================
    vis_pred = o3d.visualization.Visualizer()
    vis_pred.create_window()
    #pcd_pred = o3d.io.read_point_cloud(r'data\lidar_data\4_x_pred_y_pred_z_pred_Berechnung\x_pred_y_pred_z_pred.txt', format='xyz') 
    pcd_pred = o3d.io.read_point_cloud(r'data\lidar_data\4_x_pred_y_pred_z_pred_Berechnung\x_pred_y_pred_z_pred.txt', format='xyz') 
    vis_pred.add_geometry(pcd_pred)
    vis_pred.run()
    vis_pred.capture_screen_image('predicted_truth_pc.png') # Saves an image of the point cloud

    print(pcd_pred) 
    
    
    return(pcd_true)

    # ===========================
    # - Visualize point clouds - 
    # ===========================
    #downpcd = pcd_true.voxel_down_sample(voxel_size=0.0000001)
    #o3d.visualization.draw_geometries([downpcd], window_name = 'Ground Truth Point Cloud', width = 1920, height = 1000, left = 0)     
    #o3d.visualization.draw_geometries([pcd_pred], window_name = 'Predicted Truth Point Cloud', width = 1920, height = 1000, left = 0)   
    

# =======================================================================================
# - Berechnen der Distanzen der zwischen den Pixeln in der True PC und der Predicted PC - 
# =======================================================================================
#dists = pcd_true.compute_point_cloud_distance(pcd_pred)
#dists = np.asarray(dists)
#print(dists)

# ===========================================================
# - Abspeichern der Distanzen zwischen den einzelnen Pixeln - 
# ===========================================================
#np.savetxt(r'C:\Users\kevin\Desktop\Carla\Carla_0.9.11\PythonAPI\examples\data\lidar_data\Sprint\second_scenario\sensor50m_person18m_car40m\Predictions\Distanzen\abstaende_zw_Pixeln.txt', dists, delimiter=",") #sep=" ", header=None, index=None) 
#pd.DataFrame(dists).to_csv(r'C:\Users\kevin\Desktop\Carla\Carla_0.9.11\PythonAPI\examples\data\lidar_data\Sprint\second_scenario\sensor50m_person18m_car40m\Predictions\Distanzen\abstaende_check.txt', sep=" ", header=None, index=None)

# ====================================================
# - Visualisieren der beiden Punktwolken in Relation - 
# ====================================================
#ind = np.where(dists < 1)[0]
#pcdTrue_without_pcdPred = pcd_true.select_by_index(ind)
#o3d.visualization.draw_geometries([pcdTrue_without_pcdPred], width = 1920, height = 1000, left = 0)




