#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from time import perf_counter
from tensorflow import keras
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import classification_report
import seaborn as sns
dist_bin = 0.0468425715625 # in meter
Tbin = 312.5e-12


#Note, this code is taken straight from the SKLEARN website, an nice way of viewing confusion matrix.
import itertools
def plot_confusion_matrix(cm, classes,
                          normalize=True,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def dist_prediction(probabilities, feature_indices, filter_delay=0):
    
    t_start = perf_counter()
    
    prediction_label = label_prediciton(probabilities)
    rows = np.arange(len(prediction_label))
    prediction_distance = calc_distance(feature_indices[rows.reshape(-1,1), prediction_label.reshape(-1,1)])
    prediction_distance = prediction_distance.flatten() - calc_distance(filter_delay)
    
    t_stopp = perf_counter()
    
    prediciton_time = (t_stopp-t_start) / prediction_distance.shape[0]
    
    return prediction_distance, prediciton_time


def label_prediciton(probabilities):
    return np.argmax(probabilities, axis=1)


def probability_prediction(feature_peaks, modelpath):
    model = keras.models.load_model(modelpath) 
    
    t_start = perf_counter()
    prediction_probabilities = model.predict(feature_peaks)
    t_stopp = perf_counter()
    
    prediction_time = (t_stopp-t_start) / prediction_probabilities.shape[0]
    
    return prediction_probabilities, prediction_time

def label_true_distances(true_distances, feature_borders):
    true_index = dist_to_ind(true_distances)
    true_labels = np.array([np.argmax(feature_borders > ind)-1 for ind in true_index])
    return true_labels


def calc_distance(array):
    Tbin = 312.5e-12
    c = 299792458
    return Tbin * array * c / 2

def dist_to_ind(array):
    Tbin = 312.5e-12
    c = 299792458
    return (2 * array / (Tbin * c)).astype(int)

def feature_extraction(conv_histograms, num_features, background=False):
    
    #do featrue extraction
    t_start = perf_counter()
    
    bins = conv_histograms.shape[1] # number of bins in one histogram
    # get number of bins for one feature area
    bin_features = int(bins/num_features)
    
    # get indices where the feature borders are located
    borders = [i*bin_features for i in range(num_features)]
    borders.append(bins)
    borders = np.array(borders)
    
    # split the Dataset indo feature areas for faster computing
    split_hist = np.split(conv_histograms, borders[1:-1], axis=1)
    
    # get indices and peaks by compute maxima of the feature areas in split_hist
    feature_indices = [np.argmax(i, axis=1) for i in split_hist]
    feature_peaks = [np.max(i, axis=1) for i in split_hist]
    
    feature_indices = np.array(feature_indices).T + borders[:-1]
    feature_peaks = np.array(feature_peaks).T 
    
    t_stopp = perf_counter()
    
    extraction_time = (t_stopp - t_start)/conv_histograms.shape[0]
    
    #if not background:
    #    return feature_peaks, feature_indices, borders, extraction_time
    
    try:   
    #if background:
        num_measurements = 400
        Tbin = 312.5e-12
        t_start = perf_counter()
    
        #reshape background and repeat it to get #histograms x number_of_features array with same values in axis 1 
        bg_rate = np.repeat(background.reshape(-1,1), num_features, axis=1)
    
        # calculate background at the peak positions, take 400 measurement cycles
        bg = num_measurements * bg_rate * Tbin * np.exp(- bg_rate * Tbin * feature_indices)
        feature_peaks -= bg
        feature_peaks = np.array([p/np.max(p) for p in feature_peaks])
    
        t_stopp = perf_counter()
        background_sub_time = (t_stopp - t_start)/conv_histograms.shape[0]
        
        return feature_peaks, feature_indices, borders, extraction_time + background_sub_time
    
    except:
        feature_peaks = np.array([p/np.max(p) for p in feature_peaks])
        return feature_peaks, feature_indices, borders, extraction_time
        
def filtering(histograms):
    
    kernel = np.ones(16)/16
    
    # perform normal numpy convolution and time the 
    t_start = perf_counter()
    conv_Histograms = np.array([np.convolve(x, kernel, mode="same") for x in histograms])
    t_stopp = perf_counter()
    conv_time = (t_stopp-t_start) / histograms.shape[0]
    
    # convolution creates shift of peaks
    peak_shift = (len(kernel)-1) / 2
    
    return conv_Histograms, peak_shift, conv_time


def weight_pixel_peaks(feature_peaks,
                       feature_indices,
                       nn_probabilities,
                       num_horizontal_lines,
                       alpha=2, std=15):
    '''
    Be aware that this function only works with rectangle shaped sensors.
    Arrays should be two dim with first dim number of histograms and second dim number of features.
    Returns weighted Peaks.
    '''
    t_start = perf_counter()
    # reshape arrays to be shape (#horizontal_lines, #vertical_lines, #features)
    peaks_sensor_shape = feature_peaks.reshape(num_horizontal_lines,-1,feature_peaks.shape[1]) 
    indices_sensor_shape = feature_indices.reshape(num_horizontal_lines,-1,feature_indices.shape[1]) 
    probabilities_sensor_shape = nn_probabilities.reshape(num_horizontal_lines,-1, nn_probabilities.shape[1]) 
    
    # weight pixels in each line with their neighbour pixels
    for line in range(num_horizontal_lines):
        peaks_sensor_shape[line] = weight_func(peaks_sensor_shape[line],
                                               indices_sensor_shape[line],
                                               probabilities_sensor_shape[line],
                                               alpha=alpha, std=std)
    t_stopp = perf_counter()
    weighting_time = (t_stopp - t_start) / feature_peaks.shape[0]
    
    # return new weighted peaks with shape of peaks given to the function
    return peaks_sensor_shape.reshape(-1,feature_peaks.shape[1]), weighting_time
    

def weight_func(feature_peaks, feature_indices, nn_probabilities, alpha = 2, std=15):
    ''' 
    Weight peaks with neighbours predicted probabilities. 
    peaks[i] = peaks[i] * factor[i-1] * factor[i+1]
    
    '''
    probs_left, probs_middle, probs_right = append_left_right(nn_probabilities)
    _,peaks_middle,_ = append_left_right(feature_peaks)
    ind_left, ind_middle, ind_right = append_left_right(feature_indices)
    
    exp_lm = np.exp(- 0.5 * (ind_left - ind_middle)**2 / std**2)
    exp_rm = np.exp(- 0.5 * (ind_right - ind_middle)**2 / std**2)
    
    factor_lm = 1 + probs_left/alpha * exp_lm 
    factor_rm = 1 + probs_left/alpha * exp_rm
    new_peaks = peaks_middle * factor_lm * factor_rm
    
    return new_peaks[1:-1]


def append_left_right(array):
    ''' 
    create two equal arrays from given array with shapes:
    
    array_right = [[0,0,...,0,0],
                   [0,0,...,0,0],
                   [a01,...,a0N],
                   [a11,...,a1N],
                   [...........],
                   [aM1,...,aMN]]
                   
    array_middle =[[0,0,...,0,0],
                   [a01,...,a0N],
                   [a11,...,a1N],
                   [...........],
                   [aM1,...,aMN],
                   [0,0,...,0,0]]
    
    array_left =  [[a01,...,a0N],
                   [a11,...,a1N],
                   [...........],
                   [aM1,...,aMN],
                   [0,0,...,0,0],
                   [0,0,...,0,0]]
    '''
    right = np.vstack([array, np.zeros((2,array.shape[1]))])
    left = np.vstack([np.zeros((2,array.shape[1])),array])
    middle = np.vstack([np.zeros(array.shape[1]), array, np.zeros(array.shape[1])])
    return left, middle, right

def predict_Histograms(raw_histograms,
                       true_distances,
                       modelpath,
                       neighbour_weighting = False,
                       sensor_shape = False,
                       num_features = 12,
                       background_subtraction = False,
                       background_data = False,
                       threshold = False,
                       return_time = False):
    
    # default for filtering is convolution with mean filter of size 16
    filtered_histograms, filter_delay, filter_time = filtering(raw_histograms)
    
    # extract features
    #if background_subtraction:
        #if not background_data:
        #    print("Please provide background rate data if you want to do background subtraction")
        #    exit()
    try:
        peaks, indices, borders, extraction_time = feature_extraction(filtered_histograms,
                                                               num_features,
                                                               background=background_data)
        
    except:
        peaks, indices, borders, extraction_time = feature_extraction(filtered_histograms,
                                                               num_features,
                                                               background=False)
       


    true_labels = label_true_distances(true_distances, borders)
    
    probabilities, probability_prediction_time = probability_prediction(peaks, modelpath)

    # Saving probabilities and indices for OTSU evaluation
    np.savetxt(r'data\lidar_data\probabilities.txt', probabilities, fmt='%.4f')
    np.savetxt(r'data\lidar_data\indices.txt', indices, fmt='%.4f')

    if neighbour_weighting:
        peaks, weighting_time = weight_pixel_peaks(peaks,
                                                   indices,
                                                   probabilities,
                                                   sensor_shape[0],
                                                   alpha=2, std=15)
        
        probabilities, probability_prediction_time = probability_prediction(peaks, modelpath)
        
    pred_label = label_prediciton(probabilities)
    
    pred_dist, dis_pred_time = dist_prediction(probabilities, indices, filter_delay=filter_delay)
    if threshold:
        for i in range(len(pred_dist)):
            if np.max(probabilities[i]) <= threshold:
                pred_dist[0] = 0
        
    
    computation_time = np.array([filter_time, extraction_time, probability_prediction_time, dis_pred_time])
    
    if neighbour_weighting:
        np.insert(computation_time,-2,weighting_time+probability_prediction_time)
    
    if return_time:
        return pred_dist, computation_time
    else: 
        return pred_dist

def old_method(raw_histograms,
               backgrounds):
    kernel = np.ones(16)/16
    conv = np.array([np.convolve(h, kernel) for h in raw_histograms])
    sub = [400 * bg_rate * Tbin * np.exp(- bg_rate * Tbin * np.arange(len(hist))) for hist,bg_rate in zip(conv, backgrounds)]
    
    conv -= sub
    distance = np.array([np.argmax(h) for h in conv]) * dist_bin
    return distance

def acc_feature_extraction(histograms, true_d, num_features=12):
    # default for filtering is convolution with mean filter of size 16
    filtered_histograms, filter_delay, filter_time = filtering(histograms)
    
    peaks, indices, borders, extraction_time = feature_extraction(filtered_histograms,
                                                               num_features,
                                                               background=False)
    
    true_index = dist_to_ind(true_d)
    
    feat_indices = indices - filter_delay
    
    corr = []
    for i in range(len(true_index)):
        diff = abs(true_index[i]-feat_indices[i])
        correct_distance = diff <= (true_index[i] * 0.1/2)
        corr.append(any(correct_distance))
    
    return corr, np.sum(corr)/len(corr)



