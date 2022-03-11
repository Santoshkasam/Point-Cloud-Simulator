
import numpy as np
import pandas as pd
#import GUI



#def cutGround():

data = pd.read_csv(r'data\lidar_data\Datensatz\onePixel\22m_adjusted\12938.txt', header=None, skiprows=8, sep=" ")
df = data.loc[data[0] <= 2.7] #adapt this value to your txt-file! #default: ...[data[2] >= -0.7]
print('Daten: \n', df)
df.to_csv(r'data\lidar_data\Datensatz\onePixel\22m_adjusted\SPEICHERUNG_12938.txt', sep=" ", header=None, index=None, encoding='utf8')


