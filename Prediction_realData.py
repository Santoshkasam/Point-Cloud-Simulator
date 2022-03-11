#!/usr/bin/env python

import numpy as np
import pandas as pd


# GUCKEN OB ICH IN DER 2047 er txt auch bei -1 oder nicht -1 
# MIT DEM GENAUEN WERT FÜR DIE DISTANZ RECHNEN UND NICHT MIT DEM INTEGER-WERT
# FÜR DIE WIRKLICH KORREKTE DISTANZ DIE BINS DER JEWEILIGEN HISTOGRAMME ADDIEREN (ALSO BIN 15 AUS HIST3 MIT BIN 15 VON HIST 4, usw.) UND AUS DEM EINZELNEN HISTOGRAMM AM ENDE DEN MAXIMALWERT SUCHEN. # DANN WIEDER AUF DIE DISTANZ UMRECHNEN
# 1420 Bins entsprechen ca. 60 Meter


#####################################
## Step 1: Get the object distance ##
#####################################
# Load the Histogram txt-file:
histogram_for_distance = np.loadtxt(r'data\lidar_data\Evaluation\real_measurements\indoor\20m_white_400\Owl\2m_0Bg_white_2047.txt')
histogram_int_array = histogram_for_distance.astype(int)     # Convert float array to int array

# Get the first Histogram:
first_histogram = histogram_int_array[0]
#print(first_histogram)

# Get the length of the first Histogram:
length_first_histogram = len(first_histogram)
print('number of values in my histogram:', length_first_histogram)

# Get the penultimate element of the first Histogram for the distance value:
distance = first_histogram[length_first_histogram - 2]
print('distance:', distance, 'meters')


###################################
## Step 2: Determin starting bin ##
###################################
# Determin starting bin:
TDC_resolution_in_seconds = 312.5 * 1e-12      # 312.5 picoseconds, with *1e-12 transform to seconds
speed_of_light = 299792458                     # meters per second

distance_TDC_resolution = (speed_of_light * TDC_resolution_in_seconds) / 2

starting_bin = distance / distance_TDC_resolution 
starting_bin = starting_bin.astype(int)
print('starting bin:', starting_bin)


#############################################################################
## Step 3: Determin how many bins need to be observed (inaccuracy of SPAD) ##
#############################################################################
Pulsewidth_Owl = 18.75 # nanoseconds

observed_bins = (Pulsewidth_Owl * 1e-9) / TDC_resolution_in_seconds
observed_bins = int(observed_bins)
print('bins to observe:', observed_bins)







########################################
## Step 4: Iterate over one histogram ##
########################################
# Load Histogram:
histogram_20m_0bg_white = np.loadtxt(r'data\lidar_data\Evaluation\real_measurements\indoor\20m_white_400\Owl\2m_3Bg_white_400.txt')

# Get the first Histogram:
histogram_0bg_first = histogram_20m_0bg_white[0]
print(histogram_0bg_first)
print('length of histogram:', len(histogram_0bg_first))

# Value of starting bin:
#print(histogram_0bg_first.flat[starting_bin - 1]) # Minus 1, as we start counting from 0
# Value of last observed bin:
#print(histogram_0bg_first.flat[(starting_bin - 1) + observed_bins])

# Get the values of the observed bins:
start_value = starting_bin
print('start value:', start_value)
end_value = start_value + observed_bins
print('endl value:', end_value)

# values = []
# for element in histogram_0bg_first[start_value:end_value]:
#     values.append(element)
# np.savetxt(r'data\lidar_data\Evaluation\real_measurements\indoor\20m_white_400\Owl\values.txt', values, fmt='%d', encoding='utf8')


#########################################
## Step 5: Iterate over all histograms ##
#########################################
distances = []
bg = []
target_bins = []

for element in histogram_20m_0bg_white: # "element" ist dann das jeweilige Histogramm

    distance_values = element[(len(element) -2) : len(element)] # aus jedem Histogramm die beiden Distanzwerte auslesen
    bg_light_values = element[len(element) -3] # aus jedem Histogramm das Hintergrundlicht auslesen
    target_bin_values = element[start_value:end_value] # aus jedem Histogramm die target bins auslesen

    distances.append(distance_values)
    bg.append(bg_light_values)
    target_bins.append(target_bin_values)

np.savetxt(r'data\lidar_data\Evaluation\real_measurements\indoor\20m_white_400\Owl\2m_3Bg_white_400\distance_values.txt', distances, fmt='%.3f', encoding='utf8') # for integers: fmt='%d',
np.savetxt(r'data\lidar_data\Evaluation\real_measurements\indoor\20m_white_400\Owl\2m_3Bg_white_400\bg_light_values.txt', bg, fmt='%.3f', encoding='utf8') 
np.savetxt(r'data\lidar_data\Evaluation\real_measurements\indoor\20m_white_400\Owl\2m_3Bg_white_400\target_bin_values.txt', target_bins, fmt='%d', encoding='utf8') 


####################################################
## Step 6: Calculate Average & Standard deviation ##
####################################################
Added_values = []
NOE_values = []


# Zunächst die Werte addieren
for element in target_bins: # Für jeden target-Bereich-Histogramm

    Added = np.ndarray.sum(element)
    Added_values.append(Added)

    number_of_elements = len(element)
    NOE_values.append(number_of_elements)

np.savetxt(r'data\lidar_data\Evaluation\real_measurements\indoor\20m_white_400\Owl\2m_3Bg_white_400\added_values.txt', Added_values, fmt='%d', encoding='utf8') # for integers: fmt='%d',
np.savetxt(r'data\lidar_data\Evaluation\real_measurements\indoor\20m_white_400\Owl\2m_3Bg_white_400\number_of_elements.txt', NOE_values, fmt='%d', encoding='utf8') # for integers: fmt='%d',


# Calculate the average by hand:
#Sum_added_values = np.sum(Added_values)
#Average_of_all_histograms = Sum_added_values / len(Added_values)
#print('Average of all histograms: ', int(Average_of_all_histograms))

# Calculate average with numpys 'mean' function:
Average_of_all_histograms = np.mean(Added_values)
Average_of_all_histograms = np.rint(Average_of_all_histograms) # Round value to closest int
Average_of_all_histograms_np_save = np.array(Average_of_all_histograms, ndmin=1) # to be able to save this 0d array with "np.savetxt..."
print('Average of all histograms: ', Average_of_all_histograms)
np.savetxt(r'data\lidar_data\Evaluation\real_measurements\indoor\20m_white_400\Owl\2m_3Bg_white_400\avg_std\average_value_for_all_histograms.txt', Average_of_all_histograms_np_save, fmt='%d', encoding='utf8')


# Calculate the standard deviation of the added values:
std_for_all_histograms = np.std(Added_values)
std_for_all_histograms = np.rint(std_for_all_histograms) # Round value to closest int
std_for_all_histograms_np_save = np.array(std_for_all_histograms, ndmin=1) # to be able to save this 0d array with "np.savetxt..."
print('standard deviation for all histograms', std_for_all_histograms)
np.savetxt(r'data\lidar_data\Evaluation\real_measurements\indoor\20m_white_400\Owl\2m_3Bg_white_400\avg_std\std_value_for_all_histograms.txt', std_for_all_histograms_np_save, fmt='%d', encoding='utf8') 






#Average_values = []
# stD_values = []

# for element in Added_values: # Für jede aufaddierte Summe

    #Average = element / number_of_elements #np.mean(element) # Arithmetic mean is the sum of elements along an axis divided by the number of elements
    #Average_values.append(Average)

    # std = np.std(element) # durchschnittliche Entfernung aller gemessenen Werte eines Merkmals von dessen Mittelwert 
    # stD_values.append(std)

#np.savetxt(r'data\lidar_data\Evaluation\real_measurements\indoor\20m_white_400\Owl\20m_0Bg_white_400\average_values.txt', Average_values, fmt='%.3f', encoding='utf8') # for integers: fmt='%d',
#np.savetxt(r'data\lidar_data\Evaluation\real_measurements\indoor\20m_white_400\Owl\20m_0Bg_white_400\stD_values.txt', stD_values, fmt='%.3f', encoding='utf8') # for integers: fmt='%d',






#hist = [] # empty list

# for element in histogram:
#     if element > 20:
#         #hist.append(histogram.any())
#         histogram.any()
#print(hist)




############################
##         PANDAS         ##
############################
#data = pd.read_csv(r'data\lidar_data\Evaluation\real_measurements\indoor\20m_white_400\Owl\20m_0Bg_white_400.txt', header=None, sep=" ") #skiprows = 8

#df = data.loc[data[0] > 22]
#print(df)

#data.to_csv(r'data\lidar_data\Evaluation\real_measurements\indoor\20m_white_400\Owl\TEST.txt', sep=" ", header=None, index=None, encoding='utf8')

