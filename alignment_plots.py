import os
import numpy as np
import matplotlib.pyplot as plt
import pandas
from scipy.optimize import curve_fit

size = 20
plt.rc("font", size=size)
plt.rc("font", weight="normal")

#function to read files: each folder in "alignment" has a motor movement
def read_motor(folder):
        """
        input: a folder "date_motor_number" containing all the .csv files with VNA data for each motor position
        outputs:
        - array with positions of the motor
        - array with means of S12 and S21 for the central frequency
        - the name of the motor and number of repetitions
        - the date to save all the files with a different name
        """
        mot_to_ax = {"zrot":"ax2", "xrotII":"ax3", "zlin":"ax6"} #to know which axis to read depending on the motor we're aligning
        pos = []
        S = []
        for file in os.listdir("./alignment/"+folder): #each file we want to read is .csv and has VNA data at different motor positions
                if file.endswith(".csv"): #to ignore the log (.txt)
                        file_info = np.array(file[:-4].split("_")) #all the words in the name: the motor to be aligned and all the axes
                        ax = mot_to_ax[file_info[0]] #selecting the axis corresponding to the motor (first word in name)
                        ind_ax = np.where(file_info==ax)[0][0] #the word that corresponds to that axis
                        pos.append(float(file_info[ind_ax+1])) #the following word tells the position of that axis
                        #VNA data:
                        S12 = pandas.read_csv("./alignment/"+folder+"/"+file, skiprows=6)["S12(DB)"]
                        S21 = pandas.read_csv("./alignment/"+folder+"/"+file, skiprows=6)["S21(DB)"]
                        #average of the transmitted back and forth, at the central frequency
                        S.append(np.mean([S12[len(S12)//2], S21[len(S21)//2]]))
        return np.array(pos), np.array(S), folder.split("_")[3:], folder[:10]

def parabola(x, par):
        a, b, c = par
        return a*pow(x, 2)+b*x+c

def cos2(x, par):
        z, A, phi = par
        return z+A*pow(np.cos(x*np.pi/180+phi), 2)

def function_motor(x, par, name):
        """
        defines the right function for the fit depending on the motor
        """
        if name=="zrot" or name=="zlin":
                return parabola(x, par)
        if name=="xrotII":
                return cos2(x, par)

def fit_mot(x, y, name):
        """
        fits the right function to data depending on the motor name
        """
        if name=="zrot" or name=="zlin":
                #parabola
                return np.polyfit(x, y, 2)
        if name=="xrotII":
                #cos^2
                return curve_fit(lambda t, *par: cos2(t, par), x, y, p0=[-66, 2, 0])[0]
        
def zero(par, name):
        """
        finds the vertex of the function, which is the zero of the alignment
        """
        if name=="zrot" or name=="zlin":
                #parabola
                return -par[1]/(2*par[0])
        if name=="xrotII":
                #cos^2
                return par[2]

def plot_fit(x, y, motor, date):
        mot_to_name = {"zrot":"$\\rm z_{rot}$ [°]", "xrotII":"$\\rm x_{rot}$'' [°]", "zlin":"$\\rm z_{lin}$ [mm]"} #labels for plot
        fig, ax = plt.subplots(1, 1, figsize=(15, 10))
        ax.plot(x, y, "ok")
        par = fit_mot(x, y, motor[0])
        x_plot = np.linspace(min(x), max(x), 500)
        ax.plot(x_plot, function_motor(x_plot, par, motor[0]), "m")
        ax.axvline(zero(par, motor[0]), color="m", ls="--", label="zero at "+str(round(zero(par, motor[0]), 4)))
        ax.set_xlabel(mot_to_name[motor[0]])
        ax.set_ylabel("S [dB]")
        ax.set_title(motor[0]+" "+motor[1]+" "+date, size=40)
        ax.legend()
        fig.savefig("alignment_plots/"+motor[0]+"_"+date+"_"+motor[1]+".png")
        plt.close()
        return 0

for folder in os.listdir("./alignment"):
        p, s, motor, date = read_motor(folder)
        plot_fit(p, s, motor, date)