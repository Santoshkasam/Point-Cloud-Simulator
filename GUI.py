#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import filedialog, Text, messagebox
import os
from tkinter.constants import BOTTOM, COMMAND, LEFT, S, SUNKEN, TOP, W, X, Y
from pathlib import Path
from matplotlib.pyplot import show, text, title
from datetime import datetime

import AA_Distanz_Winkel_Berechnung
import AAA_Histogrammerzeugung
import AAAA_Prediction
import AAAAA_x_pred_y_pred_z_pred
import AAAAAA_pc_Visualisierung





root = tk.Tk()  # The window in which we add the Buttons etc. 
root.title("Point Cloud Generator")
root.iconbitmap(r'IMS_Icon.ico')
root.resizable(width=False, height=False) # Window size cannot be expanded reduced
data = []

# Frame and Canvas:
canvas = tk.Canvas(root, height=500, width=900, background="#263D42")   # "#263D42" # Fenster größer machen und farblich verändern (für Farbe geht auch "green", etc.)
canvas.pack()                                                           # Diese Einstellungen nun an das root-Struktur hinzufügen

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.7, relheight=0.7, relx=0.15, rely=0.1)            # relx,-y um es mittig zu platzieren

frameRun = LabelFrame(frame, text='Run:')#, highlightbackground='black', highlightthickness=1, background='white')
frameRun.place(x=425, y=10, width=110, height=145)

frameSettings = LabelFrame(frame, text='Settings:')#, highlightbackground='black', highlightthickness=1, background='white')
frameSettings.place(x=15, y=10, width=340, height=145)



def runGUI():
    root.mainloop() # Ausführen des GUI

def chooseData(): 

    #for widget in frame.winfo_children():       # Damit beim Hinzufügen des neuen Dateipfads, die alte data-Liste nicht wiederholt wird sondern direkt geupdated wird
    #    widget.destroy()

    global filename
    filename = filedialog.askopenfilename(initialdir=r'data\lidar_data\Datensatz', title="Select File") #, filetypes=(("executables", "*.exe"), ("all files", "*.*")))
    data.append(filename)  
    btrunGenerator.config   (state="normal")
    foldername()
    return filename
    

    for element in data:
        label = tk.Label(frame, text=element)      # Hinzufügen des Dateipfads auf dem frame
        label.pack()                           

#def launchGenerator(): 
    # for element in data:                   # Das in "chooseData" ausgewählte Element ausführen
    #     os.startfile(element)

    #os.startfile(r'C:\Users\kevin\Desktop\Carla\Carla_0.9.11\PythonAPI\examples\main.py')


def pfadUebergabe():        # Ich mache diese Pfadübergabe, da beim erneuten Aufruf von chooseData auch erneut das Pfad-Auswahlfenstergeöffnet wird         
    return filename

def run():
    print("\nStep 1: Calculating distances and angles of the chosen scenario:")
    print("--------------------------------------------------------------------------------------------------------")
    AA_Distanz_Winkel_Berechnung.load_prepare_data()
    AA_Distanz_Winkel_Berechnung.calc_distances()
    AA_Distanz_Winkel_Berechnung.calc_angles()
    AA_Distanz_Winkel_Berechnung.save_data()
    global line_count
    line_count = np.loadtxt(r'data\lidar_data\2_Distanz_Winkel_Berechnung\dist_true\dist_true.txt')
    lblNumberOf_Points.config(text=len(line_count))

    print("\nStep 2: Create the histogram:")
    print("--------------------------------------------------------------------------------------------------------")
    start = datetime.now().replace(microsecond=0)   # https://stackoverflow.com/questions/3426870/calculating-time-difference
    AAA_Histogrammerzeugung.create_histogram()
    #AAA_Hist_Gongbo.create_histogram()
    end = datetime.now().replace(microsecond=0) 
    global timeHistCalc
    timeHistCalc = end-start
    timeMemoryHistogram()
    #btcreateHistogramPlot.config(state="normal")

    print("\nStep 3: Neural Net Prediction:")
    print("--------------------------------------------------------------------------------------------------------")
    AAAA_Prediction.nnDistancePrediction()
    print('Neural Net Prediction completed')

    print("\nStep 4: Calculate the cartesian coordinates of the predicted distances calculated by the neural network:")
    print("--------------------------------------------------------------------------------------------------------")
    AAAAA_x_pred_y_pred_z_pred.prepare_data()
    AAAAA_x_pred_y_pred_z_pred.calc_coordinates()
    AAAAA_x_pred_y_pred_z_pred.save_data()
    btvisPointClouds.config(state="normal")
    btexportData.config(state="normal")

    print("\nStep 5: Calculate and visualize the point clouds:")
    print("--------------------------------------------------------------------------------------------------------")
    Number = AAAAAA_pc_Visualisierung.calc_pointClouds
    

# def plot_Histogram():
#     AAA_Hist_Gongbo.create_Plot()

def subMenuFunction():
    print("This is the function of the subMenu!")

def visualizePC(): 
    AAAAAA_pc_Visualisierung.calc_pointClouds()
    #status.config(text="Status Changed!")

# def graph():
#     housePrices = np.random.normal(200000, 25000, 5000) # (Average Price, Standard deviation, number of Data Points)
#     plt.hist(housePrices, bins=50)  
#     plt.show()

def foldername():
    global partialFilename
    partialFilename = Path(filename).parts # Splits the filename into its different parts -> List

    lblScenarioType.config(text=partialFilename[10]) # ADAPT THE CHOSEN PART OF PATH IF FILEPATH IS CHANGED -> (partialFilenam[xx]) !!!
    lblScenarioObject.config(text=partialFilename[11]) # ADAPT THE CHOSEN PART OF PATH IF FILEPATH IS CHANGED -> (partialFilenam[xx]) !!!
    lblScenarioDistance.config(text=partialFilename[12]) # ADAPT THE CHOSEN PART OF PATH IF FILEPATH IS CHANGED -> (partialFilenam[xx]) !!!

def BGSetting(clicked_BG):
    lblChosen_BG.config(text=str(clicked_BG) + " MHz")
    global bgStatus
    bgStatus = clicked_BG   # Int-Variable(clicked_BG) now becomes an Int(bgStatus)
    return bgStatus

def BGTransfer():
    return bgStatus

def LaserSetting(clicked_Laser):
    lblChosen_Laser.config(text=str(clicked_Laser) + ' MHz')
    dropdown.configure(state='active')
    global laserStatus
    laserStatus = clicked_Laser
    return laserStatus

def LaserTransfer():
    return laserStatus

def NNSetting(clicked_NN):
    # btPredict.config(state='active')
    btchooseDataset.config(state='active')
    lblChosen_NN.config(text=clicked_NN)
    global NNStatus
    NNStatus = clicked_NN
    return NNStatus

def NNTransfer():
    return NNStatus

def timeMemoryHistogram():
   lblHistTime.config(text=str(timeHistCalc))
   lblHistMemory.config(text=str(AAA_Histogrammerzeugung.HistMemoryCalculation()) + ' MB')

def radiobutton():
    btLoadNN.config(state='active')

def loadWeights(): 
    if rbState.get() == 1:    # State 1 corresponds to rbNNraw
        modelpath = (r'data\neuralNet_predictions\model_raw.h5')
        print("NN weights loaded: ", modelpath)


    if rbState.get() == 2:    # State 2 corresponds to rbNNwithBGSub
        modelpath = (r'data\neuralNet_predictions\model_bgsub.h5')
        print("NN weights loaded: ", modelpath)

    return modelpath

# def NNPredict():
#     AAAA_Prediction.nnDistancePrediction()

def export_Data():
    # distances = pd.read_csv(r'data\lidar_data\prediction_distance.txt')
    # distances.to_csv(r'data\recent_generator_run\prediction_distance.txt', index=None)
    # predicted_coordinates = pd.read_csv(r'data\lidar_data\4_x_pred_y_pred_z_pred_Berechnung\x_pred_y_pred_z_pred.txt')
    # predicted_coordinates.to_csv(r'data\recent_generator_run\x_pred_y_pred_z_pred.txt', index=None)

    # groundTruth_data = pd.read_csv(filename, header=None, skiprows = 8, sep=" ")   
    # groundTruth_data.to_csv(r'data\recent_generator_run\groundTruth_data.txt', sep=" ", header=None, index=None)

    #str(bgStatus).to_csv(r'data\recent_generator_run\parameters.txt') #bgStatus(Int) = 2       #clicked_BG(IntVar) = PyVAR

    with open('data\generated_data\parameters.txt', 'w') as file: # with this method, the file will be automatically closed # w = write mode: overrides existing data in our file # 'r' = reading a file  # 'a' = appending to a file  # 'r+' = for reading and writing # 'rb' = read binaries # 'wb' = write binarys
        file.write('Data from the most recent generator run: \n')
        file.write('----------------------------------------------------- \n')
        file.write('Scenario: \n')
        file.write(partialFilename[10] + '\n')
        file.write(partialFilename[11] + '\n')
        file.write(partialFilename[12] + '\n')
        file.write('----------------------------------------------------- \n')
        file.write('Chosen background light rate:    ' + str(bgStatus) + 'MHz' + '\n')
        file.write('Chosen laser rate:               ' + str(laserStatus) + 'MHz' + '\n')
        file.write('Chosen neural net type:          ' + NNStatus + '\n')
        file.write('Duration for histogram creation: ' + str(timeHistCalc) + ' (h:mm:ss)' + '\n')
        file.write('Used memory for histogram:       ' + str(AAA_Histogrammerzeugung.HistMemoryCalculation()) + ' MB' + '\n')
        file.write('Number of points in point cloud: ' + str(len(line_count)))

 


# Buttons:
btchooseDataset = tk.Button(frame, text="Choose Dataset", padx=38, pady=1, fg="white", bg="#263D42", command=chooseData, state='disabled') # padx,-y für die Höhe und Breite des Buttons # fg für die Farbe des Textes, command = Befehl hinzufügen
btchooseDataset.place(x=22, y=122) #old: x=20, y=20
#chooseDataset.grid(row=0, column=0)
#chooseDataset.pack(side=LEFT, padx=2, pady=2) # "padx, -y" in pixels: gives space between the Buttons

btrunGenerator = tk.Button(frame, text="Run Generator", padx=8, pady=1, fg="white", bg="#263D42", command=run, state="disabled") 
btrunGenerator.place(x=430, y=30) #old: x=20, y=60

# btcreateHistogramPlot = tk.Button(frame, text="Plot Histogram", padx=5.5, pady=1, fg="white", bg="#263D42", command=plot_Histogram, state="disabled")
# btcreateHistogramPlot.place(x=430, y=60)

btvisPointClouds = tk.Button(frame, text="Visualize PC", padx=14, pady=1, fg="white", bg="#263D42", command=visualizePC, state="disabled")
btvisPointClouds.place(x=430, y=90) #old: x=20, y=100

btexportData = tk.Button(frame, text="Export Data", padx=14.5, command=export_Data, fg="white", bg="#263D42", state='disabled')
btexportData.place(x=430, y=120) #old: x=20, y=180

# btgraph = tk.Button(frame, text="Graph", command=graph)
# btgraph.place(x=500, y=200)

btLoadNN = tk.Button(frame, text='Load NN weights', command=loadWeights, state='disabled', fg="white", bg="#263D42")
btLoadNN.place(x=220, y=90)

# btPredict = tk.Button(frame, text="Predict", command=NNPredict, state='disabled')
# btPredict.place(x=360, y=140)




# Label:
lblFraunhofer = tk.Label(root, text="Fraunhofer IMS")
lblFraunhofer.place(x=136, y=31)

# lblChooseNN = tk.Label(frame, text="Choose Neural Net:", bg="white")
# lblChooseNN.place(x=20, y=145)

lblLine = tk.Label(frame, text="____________________________________________________________________________________________________________________________", bg="white")
lblLine.place(x=5, y=180) #old: x=300, y=10

lblScenario = tk.Label(frame, text="Scenario:", bg="white")
lblScenario.place(x=20, y=210) #old: x=300, y=10

lblScenarioType = tk.Label(frame, text="-", bg="white") 
lblScenarioType.place(x=20, y=230) #old: x=300, y=30

lblScenarioObject = tk.Label(frame, text="-", bg="white")
lblScenarioObject.place(x=20, y=250) #old: x=300, y=50

lblScenarioDistance = tk.Label(frame, text="-", bg="white")
lblScenarioDistance.place(x=20, y=270) #old: x=300, y=70

lblHist_Time = tk.Label(frame, text="Time Hist:", bg="white")
lblHist_Time.place(x=100, y=210) #old: x=430, y=10

lblHistTime = tk.Label(frame, text='-', bg='white')
lblHistTime.place(x=210, y=210) #old: x=540, y=10

lblHist_Memory = tk.Label(frame, text="Memory Hist:", bg="white")
lblHist_Memory.place(x=100, y=230) #old: x=430, y=30

lblHistMemory = tk.Label(frame, text='-', bg='white')
lblHistMemory.place(x=210, y=230) #old: x=540, y=30

lblChosenBG = tk.Label(frame, text='Chosen BG Light:', bg='white')
lblChosenBG.place(x=100, y=250) #old: x=430, y=50

lblChosen_BG = tk.Label(frame, text='-', bg='white')
lblChosen_BG.place(x=210, y=250) #old: x=540, y=50

lblChosenLaser = tk.Label(frame, text='Chosen Laser rate:', bg='white')
lblChosenLaser.place(x=100, y=270) #old: x=430, y=70

lblChosen_Laser = tk.Label(frame, text='-', bg='white')
lblChosen_Laser.place(x=210, y=270) #old: x=540, y=70

lblChosenNN = tk.Label(frame, text='Chosen NN:', bg='white')
lblChosenNN.place(x=100, y=290) #old: x=430, y=90

lblChosen_NN = tk.Label(frame, text='-', bg='white')
lblChosen_NN.place(x=210, y=290) #old: x=540, y=90

lblNumberOfPoints = tk.Label(frame, text='Nr. of points:', bg='white')
lblNumberOfPoints.place(x=100, y=310) #old: x=430, y=110

lblNumberOf_Points = tk.Label(frame, text='-', bg='white')
lblNumberOf_Points.place(x=210, y=310) #old: x=540, y=110

lblChooseNNWeights = tk.Label(frame, text='Choose NN weights:')#, bg='white')
lblChooseNNWeights.place(x=220, y=20) #old: x=140, y=180

#lblEvaluation = tk.Label(frame, text='Evaluation:', bg='white')
#lblEvaluation.place(x=350, y=210)



# Dropdown Box:
clicked_BG = IntVar()   # item selected in dropdown box will be assigned to the 'clicked' variable
options_BG = [          # The chosen background frequency will be stored in the variable "options_BG"
    1, 
    2,
    3,
    4,
    5,
    6,
    7,
    8
]
clicked_BG.set("Set BG Light [MHz]")   # For default Value
dropdown = tk.OptionMenu(frame, clicked_BG, *options_BG, command=BGSetting)
dropdown.config(fg='white', bg='#263D42', padx=17.5)
dropdown.place(x=20, y=30) #old: x=140, y=100


clicked_Laser = IntVar()   # item selected in dropdown box will be assigned to the 'clicked_Laser' variable
options_Laser = [          # The chosen Laser frequency will be stored in the variable "options_Laser"
    1, 
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10
]
clicked_Laser.set("Set Laser rate [MHz]")   # For default Value
dropdown = tk.OptionMenu(frame, clicked_Laser, *options_Laser, command=LaserSetting)
dropdown.config(fg='white', bg='#263D42', padx=14.5)
dropdown.place(x=20, y=60) #old: x=282, y=100


clicked_NN = StringVar()   # item selected in dropdown box will be assigned to the 'clicked_NN' variable
options_NN = [             # The chosen neural network method will be stored in the variable "options_NN"
    "Classical", 
    "Prediction"
    #"Weighted",
    #"Threshold",
    #"Pointgroup"
]
clicked_NN.set("Choose Neural Network")   # For default Value
dropdown = tk.OptionMenu(frame, clicked_NN, *options_NN, command=NNSetting)
dropdown.configure(fg='white', bg='#263D42', state='disabled')
dropdown.place(x=20, y=90) #old: x=140, y=140




# Photos:
photo = tk.PhotoImage(file=r'IMS_Logo.png')
label = tk.Label(frame, image=photo)         # Photos need to be put into a label to display them with tkinter
label.place(x=357, y=285)



# Menu:
menu = tk.Menu(root)        # Main menu at the top of the program
root.config(menu=menu)      # By this we tell tKinter that it is a menu

subMenu = tk.Menu(menu, tearoff=0)     # Create a Submenu inside the main menu for the following dropdown # "tearoff" get rid of dashed line at the top
menu.add_cascade(label="File", menu=subMenu)    # To create the dropdown functionality
subMenu.add_command(label="New Project", command=subMenuFunction)
subMenu.add_command(label="Hola", command=subMenuFunction)



# Status Bar:
status = tk.Label(root, text="Status:", relief=SUNKEN, bd=1, anchor=W) # bd = Border around the Label # relief=SUNKEN = Looks like it is placed in your screen # anchor=W = Label appears on the Left  
status.pack(side=BOTTOM, fill=X)



# Messagebox:
#messagebox.showinfo("Pop up Window", "Hello")
#answer = messagebox.askquestion("Question", "Are you older than 18?")
#if answer == 'yes':
#    print('xdxdxdxd')



# Create a new Window:
#top = Toplevel()    # You could put this into a function that gets called when clicking a button



# Checkbox:
#var = IntVar()  # tKinter variable of the type Integer # when box is checked = 1, when unchecked = 0
#var = StringVar() # in line below: onvalue="whatever", offvalue="gibberish"
#cbStatic = tk.Checkbutton(frame, text='static', variable=var) 
#cbStatic.place(x=430, y=210)

#cbdynamic = tk.Checkbutton(frame, text='dynamic')
#cbdynamic.place(x=430, y=230)

#cbNNraw = tk.Checkbutton(frame, text='raw')
#cbNNraw.place(x=270, y=180)

# cbNNwithBGSub = tk.Checkbutton(frame, text='with bg subtraction')
# cbNNwithBGSub.place(x=270, y=200)


# Radiobutton:
rbState = IntVar()
rbState.set('0')

rbNNraw = tk.Radiobutton(frame, text='raw', variable=rbState, value=1, command=radiobutton)#, tristatevalue=0)
rbNNraw.place(x=220, y=40) #old: x=270, y=180         

rbNNwithBGSub = tk.Radiobutton(frame, text='with bg subtraction', variable=rbState, value=2, command=radiobutton)#, tristatevalue=0)
rbNNwithBGSub.place(x=220, y=60) #old: x=270, y=200

# lblRadiobutton = tk.Label(frame, text=rbState.get(), bg='white')
# lblRadiobutton.place(x=350, y=180)




# Entries:
#entry_1 = tk.Image(root)
#entry_1.place(x=80, y=10)



# Toolbar:
# Frame als langen Streifen machen und dann Buttons einfügen...



#runGUI()