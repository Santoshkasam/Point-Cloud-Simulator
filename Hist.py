from random import choices
import numpy as np
import matplotlib.pyplot as plt


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
    bins = np.arange(0, 60.59667, 0.046257) #create bin series to store photon counts
    pmf = pmf_calculation(r_B, r_L, D_TOF)

    hist = np.zeros(1310)
    for n in range(0, N_M):
        timestamp = choices(bins,pmf)
        #print(timestamp)
        for m in range(0,1310):
            if timestamp[0] == m * 0.046257:
                hist[m] = hist[m]+1
                #print(hist[m])
            #break
    return(hist)

r_L = 10 * pow(10, 6)   # received laser photon detection rate
r_B = 5 * pow(10, 6)    # received background photon detection rate
D_TOF = 20      # TOF [m]
N_M = 400 #4000000   # number of measurements in a histogram


hist = hist_generation(r_B, r_L, D_TOF)
plt.plot(hist)
plt.show()


'''
class Hist_Generation:
    def __init__(self, r_B, r_L, D_TOF, N_M):
        self.r_B = r_B
        self.r_L = r_L
        self.D_TOF = D_TOF
        self.N_M = N_M
        self.c = 299792458
        self.T_R = 312.5 * pow(10, -12)
        self.T_P = 5 * pow(10, -10)
        self.T_TOF = self.D_TOF / c * 2#
        self.bins = np.arange(0, 60.59667,0.046257)

    def run(self):
        pmf = self.pmf_calculation(self.r_B, self.r_L, self.D_TOF)
        hist = hist_formation(pmf)
        plt.plot(hist)
        plt.show()
        return(hist)

    def pmf_calculation(self):
        pmf = np.zeros(1310)
        for n in range(0, 1310):
            #y[n] = math.exp(-level_aml[nth_sample]*x[n]) * (1 - math.exp(-level_aml[nth_sample]*14*3.125/pow(10,10)))
            bin = n * self.T_R
            if bin <= self.T_TOF:
                pmf[n] = self.r_B * np.exp(-(bin+self.T_R/2)*self.r_B)*3.125*pow(10,-10)#*400
            elif bin <= self.T_TOF+self.T_P:
                pmf[n] = (self.r_B+self.r_L) * np.exp(-((bin+self.T_R/2)-self.T_TOF)*(self.r_B+self.r_L)) * np.exp(-self.T_TOF*self.r_B)*3.125*pow(10,-10)#*400
            else:
                pmf[n] = self.r_B * np.exp(-(bin+self.T_R/2)*self.r_B) * np.exp(-self.T_P*self.r_L)*3.125*pow(10,-10)#*400
        return(pmf)

    def hist_formation(self, pmf):
        hist = np.zeros(1310)
        for n in range(0, self.N_M):
            timestamp = choices(bins, pmf)
            # print(timestamp)
            for m in range(0, 1310):
                if timestamp[0] == m * 0.046257:
                    hist[m] = hist[m] + 1
        return(hist)

if __name__ == "__main__":
    r_L = 10 * pow(10, 6)
    r_B = 5 * pow(10, 6)
    D_TOF = 20
    N_M = 400
'''