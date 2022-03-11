 #import matlab.engine
from random import choices
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#import Neu_Hist
from numpy import savetxt
import GUI

def pmf_calculation(r_B, r_L, D_TOF):
    c = 299792458   # speed of light
    T_R = 312.5 * pow(10, -12)  # sensor resolution [s]
    T_P = 5 * pow(10, -9)  # pulse width [s]
    T_TOF = D_TOF / c * 2   # TOF [s]

    pmf = np.zeros(1310)
    for n in range(0, 1310):
        bin = n * T_R
        if bin <= T_TOF:
            pmf[n] = r_B * np.exp(-(bin+T_R/2)*r_B)*3.125*pow(10,-10)
        elif bin <= T_TOF+T_P:
            pmf[n] = (r_B+r_L) * np.exp(-((bin+T_R/2)-T_TOF)*(r_B+r_L)) * np.exp(-T_TOF*r_B)*3.125*pow(10,-10)
        else:
            pmf[n] = r_B * np.exp(-(bin+T_R/2)*r_B) * np.exp(-T_P*r_L)*3.125*pow(10,-10)
    return(pmf)



def hist_generation(r_B, r_L, D_TOF):
    bins = np.arange(0, 61.3604, 0.04684) #create bin series to store photon counts
    pmf = pmf_calculation(r_B, r_L, D_TOF)

    hist = np.zeros(1310)
    for n in range(0, N_M):
        timestamp = choices(bins,pmf)
        #print(timestamp)
        for m in range(0,1310):
            if timestamp[0] == m * 0.04684:
                hist[m] = hist[m]+1
                #print(hist[m])
            #break
    return(hist)

N_M = 400 #4000000   # number of measurements in a histogram
#hist = hist_generation(r_B, r_L, D_TOF)




def create_histogram(): # Starting matlabengine to use matlab out of Python and load the true distances from step 2:
    #engine = matlab.engine.start_matlab()
    #print("Connection to matlab established")
    
    # OLD: absolute Path: C:\Users\kevin\Desktop\Carla\Carla_0.9.11\PythonAPI\examples\
    carla_data = np.loadtxt(r'data\lidar_data\2_Distanz_Winkel_Berechnung\dist_true\dist_true.txt') #dist_true_small_test_version  #dist_true
    #carla_data = np.loadtxt(r'data\lidar_data\Datensatz\Dynamic\Test\42477.txt')
    print("True distance data successfully read")
    print("Calculation of histogram is starting...takes a few moments...")

    # Calculate Used Histogram Memory:
    count = sum(1 for _ in carla_data)  
    bins = 1400
    bit = 8
    HistMemory = count * bins * bit
    global HistMemoryMb
    HistMemoryMb = (HistMemory / 8) * 1e-6

    LaserSetting = GUI.LaserTransfer() * 1000000    # Convert to MHz
    bg_frequency = GUI.BGTransfer() * 1000000

    hist = []
    background = []
    true_distance = []

    for distance in carla_data:
        #global data
        #data = engine.HIST_Generator(1, float(65.0), float(distance), float(LaserSetting), float(bg_frequency), 1)   # HIST_Generator(NumberDetEventsPerCycle, DistMax, DistTarget, PhotonFlowLaser, PhotonFlowBG, CoincidenceLevel)
        histogram = hist_generation(bg_frequency, LaserSetting, distance)
        
        #hist.append(data[0]) # Einfügen der berechneten Histogramme in die Liste "hist" # "[0]"" = die komplette 1.Spalte wird durchgegangen
        hist.append(histogram)
        background.append(bg_frequency) 
        true_distance.append(distance)


    # Saving the histograms and the associated distances and background lights
    # OLD: absolute Path: C:\Users\kevin\Desktop\Carla\Carla_0.9.11\PythonAPI\examples\
    np.savetxt(r'data\hist_data\3_Histogrammerzeugung\histogram.txt', hist, fmt='%d', encoding='utf8') #'%d', damit die Werte als integer abgespeichert werden
    np.savetxt(r'data\hist_data\3_Histogrammerzeugung\background.txt', background, fmt='%d')
    np.savetxt(r'data\hist_data\3_Histogrammerzeugung\true_dist.txt', true_distance, fmt='%.4f') #'%.4f', damit die Werte als floats mit 4 Nachkommastellen abgespeichert werden
    print("Histogram created and saved")

    #engine.quit()
    print("Connection to Matlab terminated")


def HistMemoryCalculation():
   return "{0:.3f}".format(HistMemoryMb)   # return the Memory with only 3 decimal places


# def create_Plot():
#     histogram = np.array(data)[0] # Histogramm und Distanz in einer Liste, aber für den Plot nur hist benötigt, deswegen wählen wir das 1. Element aus -> "[0]"

#     histogram = np.convolve(histogram, np.ones(16)/16, mode="valid") # Mittelwertsfilter einfügen

#     # Darstellen eines Histogramms zur Veranschaulichung
#     plt.plot(histogram)
#     plt.show() # 1400 bins # Ein Bin entspricht 4,68 centimeter