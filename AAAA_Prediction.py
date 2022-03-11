#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import Evaluation
import GUI

def nnDistancePrediction():
    # Load data:
    test_raw_histograms = np.loadtxt(r'data\hist_data\3_Histogrammerzeugung\histogram.txt')
    test_distances = np.loadtxt(r'data\hist_data\3_Histogrammerzeugung\true_dist.txt')
    test_backgrounds = np.loadtxt(r'data\hist_data\3_Histogrammerzeugung\background.txt')

    # print("\n raw Histograms: \n", test_raw_histograms)
    # print("\n true Distances: \n", test_distances)
    # print("\n background rates: \n ", test_backgrounds, '\n')

    #Load model path:
    modelpath = (r'data\neuralNet_predictions\model_bgsub.h5')    # model with background subtraction
    #modelpath = "model_raw.h5"      # model without bg subtraction

    neuralnetSetting = GUI.NNTransfer() # Chosen NN option (classical, weighted, ...)
    print(neuralnetSetting)

    modelpath = GUI.loadWeights() # Correct Modelpath: raw or with bg subtraction
    print(modelpath)

    #ChosenNet = GUI.NNTransfer()

    if neuralnetSetting == 'Prediction':
        # Prediction with background subtraction:
        predict_dist_bg = Evaluation.predict_Histograms(test_raw_histograms,
                        test_distances,
                        modelpath,
                        neighbour_weighting = False,
                        sensor_shape = False,
                        num_features = 12,
                        background_subtraction = True,
                        background_data = test_backgrounds,
                        return_time = False)
        print("\n Distances with bg subtraction: \n", predict_dist_bg, '\n')

        np.savetxt(r'data\lidar_data\prediction_distance.txt', predict_dist_bg, fmt='%.4f') 

    elif neuralnetSetting == 'Classical':

        # Prediction with classical Method
        predict_old = Evaluation.old_method(test_raw_histograms, test_backgrounds)
        print("Classical Method: \n", predict_old, '\n')

        np.savetxt(r'data\lidar_data\prediction_distance.txt', predict_old, fmt='%.4f') 







# # Prediction with threshold and bg subtraction
# predict_dist_bg_thresh = Evaluation.predict_Histograms(test_raw_histograms,
#                    test_distances,
#                    modelpath,
#                    neighbour_weighting = False,
#                    sensor_shape = False,
#                    num_features = 12,
#                    background_subtraction = True,
#                    threshold = 0.7,
#                    background_data = test_backgrounds,
#                    return_time = False)
# print("Distances with threshold and bg subtraction: \n", predict_dist_bg_thresh)


# """# Prediction with neighbour weighting:"
# predict_dist_bg_weighted = Evaluation.predict_Histograms(test_raw_histograms,
#                    test_distances,
#                    modelpath,
#                    neighbour_weighting = True,
#                    sensor_shape = [100,-1],
#                    num_features = 12,
#                    background_subtraction = True,
#                    background_data = test_backgrounds,
#                    return_time = False)
# print(predict_dist_bg_weighted)"""