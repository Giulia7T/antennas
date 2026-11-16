import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from scipy.ndimage import maximum_filter1d, uniform_filter1d

size = 20
plt.rc("font", size=size)
plt.rc("font", weight="normal")

###FUNCTIONS###
#to read and plot data
def read(folder, band, versions=None):
    antenna = "_"+band
    names = np.array(["horn", "line"]) #2 series of plots, one for component
    pos_plot = [221, 222, 223, 224] #4 for each plot
    y_label = ["S11 [dB]", "S21 [dB]", "S12 [dB]", "S22 [dB]"]
    nu_0 = [] #contains horn and line values
    S_0 = []
    nu_1 = []
    S_1 = []
    i = 0
    j = 0
    if versions!=None:
        for name in names:
            ind = np.array([f.startswith(name+antenna) for f in os.listdir(folder[0])])
            file = np.array(os.listdir(folder[0]))[ind][0]
            #data: 0 is frequency, 1+n*2 selects 1, 3, 5, 7 columns which are the amplitudes
            nu = np.loadtxt(folder[0]+"/"+file, skiprows=7)[:, 0]/1e9 #in GHz
            S11 = np.loadtxt(folder[0]+"/"+file, skiprows=7)[:, 1]
            S21 = np.loadtxt(folder[0]+"/"+file, skiprows=7)[:, 3]
            S12 = np.loadtxt(folder[0]+"/"+file, skiprows=7)[:, 5]
            S22 = np.loadtxt(folder[0]+"/"+file, skiprows=7)[:, 7]
            if file=="horn_WR10_silver_insertion_loss.s2p":
                S11 = np.loadtxt(folder[0]+"/"+file, skiprows=7)[:, 7]
                S22 = np.loadtxt(folder[0]+"/"+file, skiprows=7)[:, 1]
            nu_0.append(nu)
            S_0.append(np.array([S11, S21, S12, S22]))
            
            for vers in versions[name]:
                ind = np.array([f.startswith(name+antenna) and vers in f for f in os.listdir(folders[1])])
                if True in ind:
                    file = np.array(os.listdir(folder[1]))[ind][0]
                    #data
                    nu = np.loadtxt(folder[1]+"/"+file, skiprows=7)[:, 0]/1e9 #in GHz
                    S11 = np.loadtxt(folder[1]+"/"+file, skiprows=7)[:, 1]
                    S21 = np.loadtxt(folder[1]+"/"+file, skiprows=7)[:, 3]
                    S12 = np.loadtxt(folder[1]+"/"+file, skiprows=7)[:, 5]
                    S22 = np.loadtxt(folder[1]+"/"+file, skiprows=7)[:, 7]
                    nu_1.append(nu)
                    S_1.append(np.array([S11, S21, S12, S22]))
                    if vers=="_load":
                        fig = plt.figure(figsize=(20, 10), dpi=150)
                        for n in range(4):
                            ax = fig.add_subplot(pos_plot[n])
                            ax.plot(nu_1[j], S_1[j][n], "r", label=folder[1])
                            ax.set_xlabel("$\\nu$ [GHz]")
                            ax.set_ylabel(y_label[n])
                            ax.legend()
                        fig.suptitle(name+" "+band+vers, size=50)
                        fig.savefig("IL_results/S_"+name+"_"+folder[0]+"_"+folder[1]+"_"+band+vers+".png")
                    else:
                        fig = plt.figure(figsize=(20, 10), dpi=150)
                        for n in range(4):
                            ax = fig.add_subplot(pos_plot[n])
                            ax.plot(nu_0[i], S_0[i][n], "b", label=folder[0])
                            ax.plot(nu_1[j], S_1[j][n], "r", label=folder[1])
                            ax.set_xlabel("$\\nu$ [GHz]")
                            ax.set_ylabel(y_label[n])
                            ax.legend()
                        fig.suptitle(name+" "+band+vers, size=50)
                        fig.savefig("IL_results/S_"+name+"_"+folder[0]+"_"+folder[1]+"_"+band+vers+".png")
                    j+=1
            i+=1
        return nu_0, S_0, nu_1, S_1
    else:
        for name in names:
            ind = np.array([f.startswith(name+antenna) for f in os.listdir(folder[0])]) #which file in directory has the right name "horn" or "antenna"
            file = np.array(os.listdir(folder[0]))[ind][0] #name of the right file to plot in each case
            #data: 0 is frequency, 1+n*2 selects 1, 3, 5, 7 columns which are the amplitudes
            nu = np.loadtxt(folder[0]+"/"+file, skiprows=7)[:, 0]/1e9 #in GHz
            S11 = np.loadtxt(folder[0]+"/"+file, skiprows=7)[:, 1]
            S21 = np.loadtxt(folder[0]+"/"+file, skiprows=7)[:, 3]
            S12 = np.loadtxt(folder[0]+"/"+file, skiprows=7)[:, 5]
            S22 = np.loadtxt(folder[0]+"/"+file, skiprows=7)[:, 7]
            nu_0.append(nu)
            S_0.append(np.array([S11, S21, S12, S22]))
            
            ind = np.array([f.startswith(name+antenna) for f in os.listdir(folders[1])])
            file = np.array(os.listdir(folder[1]))[ind][0]
            #data
            nu = np.loadtxt(folder[1]+"/"+file, skiprows=7)[:, 0]/1e9 #in GHz
            S11 = np.loadtxt(folder[1]+"/"+file, skiprows=7)[:, 1]
            S21 = np.loadtxt(folder[1]+"/"+file, skiprows=7)[:, 3]
            S12 = np.loadtxt(folder[1]+"/"+file, skiprows=7)[:, 5]
            S22 = np.loadtxt(folder[1]+"/"+file, skiprows=7)[:, 7]
            if file=="horn_WR10_silver_insertion_loss.s2p":
                S11 = np.loadtxt(folder[1]+"/"+file, skiprows=7)[:, 7]
                S22 = np.loadtxt(folder[1]+"/"+file, skiprows=7)[:, 1]
            nu_1.append(nu)
            S_1.append(np.array([S11, S21, S12, S22]))
                
            fig = plt.figure(figsize=(20, 10), dpi=150)
            for n in range(4):
                ax = fig.add_subplot(pos_plot[n])
                ax.plot(nu_0[i], S_0[i][n], "b", label=folder[0])
                ax.plot(nu_1[i], S_1[i][n], "r", label=folder[1])
                ax.set_xlabel("$\\nu$ [GHz]")
                ax.set_ylabel(y_label[n])
                ax.legend()
            fig.suptitle(name+" "+band, size=50)
            fig.savefig("IL_results/S_"+name+"_"+folder[0]+"_"+folder[1]+"_"+band+".png")
            i+=1
        return nu_0, S_0, nu_1, S_1            

#to compute the upper envelope
def envelope(v, S, edges=None):
    if edges!=None:
        ind_hole = (v>=edges[0])==(v<=edges[1])
        ind_break = np.where(v>=edges[0])[0][0] #when the hole starts
        peaks = maximum_filter1d(S[~ind_hole], len(S)//12)
        roll_mean = uniform_filter1d(peaks, len(S)//12)
        hole = np.interp(v[ind_hole], [v[ind_hole][0], v[ind_hole][-1]], [roll_mean[ind_break], roll_mean[ind_break+1]])
        return np.array(list(roll_mean[:ind_break])+list(hole)+list(roll_mean[ind_break:]))
    else:
        peaks = maximum_filter1d(S, len(S)//12)
        return uniform_filter1d(peaks, len(S)//12)

#to correct S12 and S21 for reflection
def correct_transmitted(S_matrix):
    #S_matrix = [S11, S21, S12, S22]
    #linear
    linear_S11 = 10**(S_matrix[0]/10)
    linear_S21 = 10**(S_matrix[1]/10)
    linear_S12 = 10**(S_matrix[2]/10)
    linear_S22 = 10**(S_matrix[3]/10)
    #correction
    linear_S21_corr = linear_S21/(1-linear_S11)
    linear_S12_corr = linear_S12/(1-linear_S22)
    #back to dB
    S21_corr = 10*np.log10(linear_S21_corr)
    S12_corr = 10*np.log10(linear_S12_corr)
    return S21_corr, S12_corr

#to compute the IL in different frequency points for the line
def IL_v(S, frequencies):
    mean = np.zeros(len(frequencies))
    std = np.zeros(len(frequencies))
    mean[0] = -np.mean(S[:frequencies[0]])
    std[0] = np.std(S[:frequencies[0]])
    for n in range(1, len(frequencies)):
        mean[n] = -np.mean(S[frequencies[n-1]:frequencies[n]])
        std[n] = np.std(S[frequencies[n-1]:frequencies[n]])
    return mean, std

#to round well
def rounding(number, n):
    if str(round(number, n)).endswith((n-1)*"0"+"1") or str(round(number, n)).endswith(".0"):
        return rounding(number, n+1)
    return round(number, n)

#to plot raw and corrected
def plot_raw(nu, S, S_corr, titles, name):
    #S is S12 or S21 with entrances [W band for the first material, D for the first, W for the second, D for the second]
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(25, 15))
    axs = [ax1, ax2, ax3, ax4]
    colour = ["b", "g"]
    band = ["W", "D"]
    for i in range(4):
        ax = axs[i]
        ax.plot(nu[i], S[i], colour[i%2], alpha=0.4, label="raw")
        ax.plot(nu[i], S_corr[i], colour[i%2], label="corrected")
        ax.set_xlabel("$\\nu$ [GHz]")
        ax.set_ylabel(name+" [dB]")
        ax.set_title(titles[i]+" - "+band[i%2]+"-band")
        ax.legend()
    f.suptitle("Waveguide Insertion Loss - "+name, size=50)
    f.savefig("IL_results/corrected_"+name+"_"+titles[0]+"_"+titles[2]+".png")

#to plot IL for lines
def plot_lineIL(nu, S, edges, IL, titles, name):
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(25, 15))
    axs = [ax1, ax2, ax3, ax4]
    colour = ["b", "g"]
    band = ["W", "D"]
    for i in range(4):
        ax = axs[i]
        ax.plot(nu[i], S[i], colour[i%2], alpha=0.5, label="corrected")
        ax.plot(nu[i], uniform_filter1d(S[i], len(S[i])//32), colour[i%2], label="smoothed")
        ax.plot(nu[i][np.array(edges[i])], uniform_filter1d(S[i], len(S[i])//32)[np.array(edges[i])], "^k")
        for v in edges[i]:
            y = uniform_filter1d(S[i], len(S[i])//32)[v]
            #ax.text(nu[i][v], y-0.01, str(-rounding(IL[i][edges[i]==v][0], 2)), backgroundcolor="w")
            ax.text(nu[i][v], y-0.01, str(-rounding(uniform_filter1d(S[i], len(S[i])//32)[edges[i]][edges[i]==v][0], 2)), backgroundcolor="w")
        ax.set_xlim(min(nu[i])-5, max(nu[i])+5)
        ax.set_xlabel("$\\nu$ [GHz]")
        ax.set_ylabel(name+" [dB]")
        ax.set_title(titles[i]+" - "+band[i%2]+"-band")
        ax.legend()
    f.suptitle("Waveguide Insertion Loss - "+name+" smoothed", size=50)
    f.savefig("IL_results/IL_line_"+name+"_"+titles[0]+"_"+titles[2]+".png")

###DATA###
folder0 = input("material 1: ")
folder1 = input("material 2: ")
folders = np.array([folder0, folder1])
#sorting so that the first material is always at the same index
if "copper" in folders:
    ind = folders=="copper"
    folders = np.array([folders[~ind][0], folders[ind][0]])
if "no_silver" in folders:
    ind = folders=="no_silver"
    folders = np.array([folders[ind][0], folders[~ind][0]])
versions = None
if folders[1]=="copper":
    versions = {"horn":["_short", "_load"], "line":["_1", "_2"]} #dictionary for the versions of horn and line
nu_W_0, S_W_0, nu_W_1, S_W_1 = read(folders, "WR10", versions) #all S have entrance [0] for horn and [1] for line
nu_D_0, S_D_0, nu_D_1, S_D_1 = read(folders, "WR06", versions)


#HORN
#upper envelope
env_W_0 = envelope(nu_W_0[0], S_W_0[0][0])
env_W_1 = envelope(nu_W_1[0], S_W_1[0][0])
env_D_0 = envelope(nu_D_0[0], S_D_0[0][0])
env_D_1 = envelope(nu_D_1[0], S_D_1[0][0])
if folders[0]=="no_silver" and folders[1]=="silver":
    env_D_0 = envelope(nu_D_0[0], S_D_0[0][0], [124.5, 126.5])
    env_D_1 = envelope(nu_D_1[0], S_D_1[0][0], [124.5, 126.5])
if folders[0]=="silver":
    env_D_0 = envelope(nu_D_0[0], S_D_0[0][0], [124.5, 126.5])
if folders[1]=="copper":
    env_W_1_v1 = envelope(nu_W_1[0], S_W_1[0][0])
    env_D_1_v2 = envelope(nu_D_1[0], S_D_1[0][0])
    env_W_1_v2 = envelope(nu_W_1[0], S_W_1[0][3]) #S11 is version 1 and S22 is version 2
#IL
ILh_W_0 = -np.mean(env_W_0)/2
ILh_err_W_0 = np.std(env_W_0)/2
ILh_W_1 = -np.mean(env_W_1)/2
ILh_err_W_1 = np.std(env_W_1)/2
ILh_D_0 = -np.mean(env_D_0)/2
ILh_err_D_0 = np.std(env_D_0)/2
ILh_D_1 = -np.mean(env_D_1)/2
ILh_err_D_1 = np.std(env_D_1)/2
if folders[1]=="copper":
    ILh_W_1_v1 = -np.mean(env_W_1_v1)/2
    ILh_err_W_1_v1 = np.std(env_W_1_v1)/2
    ILh_W_1_v2 = -np.mean(env_W_1_v2)/2
    ILh_err_W_1_v2 = np.std(env_W_1_v2)/2
    ILh_D_1_v2 = -np.mean(env_D_1_v2)/2
    ILh_err_D_1_v2 = np.std(env_D_1_v2)/2
#plot
if folders[0]=="no_silver":
    title0 = "AlSi10Mg"
if folders[1]=="silver":
    title1 = "Silver plated"
if folders[0]=="silver":
    title0 = "Silver plated"
if folders[1]=="copper":
    title1 = "Copper"
f, (ax1, ax2) = plt.subplots(2, 1, sharex=True, sharey=True, figsize=(25, 15))
ax1.plot(nu_W_0[0], S_W_0[0][0], "b", alpha=0.3)
ax1.plot(nu_W_0[0], env_W_0, "b", lw=4)
ax1.text(nu_W_0[0][len(nu_W_0[0])//2], -0.1, "W-band", color="b")
ax1.plot(nu_D_0[0], S_D_0[0][0], "g", alpha=0.3)
ax1.plot(nu_D_0[0], env_D_0, "g", lw=4)
ax1.text(nu_D_0[0][len(nu_D_0[0])//2], -0.1, "D-band", color="g")
ax1.axvline(110, ls="--", color="k")
ax1.set_xlabel("$\\nu$ [GHz]")
ax1.set_ylabel("S11 [dB]")
ax1.set_title(title0)
ax1.set_ylim(-3, 0.2)
ax1.text(nu_D_0[0][len(nu_D_0[0])//2], -2.8, "W-band:("+"{:.3f}".format(rounding(ILh_W_0, 2))+"$\\pm$"+"{:.3f}".format(rounding(ILh_err_W_0, 2))+") dB\nD-band:("+"{:.2f}".format(rounding(ILh_D_0, 2))+"$\\pm$"+"{:.2f}".format(rounding(ILh_err_D_0, 2))+") dB", backgroundcolor="w")
ax2.plot(nu_W_1[0], S_W_1[0][0], "b", alpha=0.3)
ax2.plot(nu_W_1[0], env_W_1, "b", lw=4)
ax2.text(nu_W_1[0][len(nu_W_1[0])//2], -0.1, "W-band", color="b")
ax2.plot(nu_D_1[0], S_D_1[0][0], "g", alpha=0.3)
ax2.plot(nu_D_1[0], env_D_1, "g", lw=4)
ax2.text(nu_D_1[0][len(nu_D_1[0])//2], -0.1, "D-band", color="g")
ax2.axvline(110, ls="--", color="k")
ax2.set_xlabel("$\\nu$ [GHz]")
ax2.set_ylabel("S11 [dB]")
ax2.set_title(title1)
ax2.text(nu_D_1[0][len(nu_D_1[0])//2], -2.8, "W-band:("+"{:.2f}".format(rounding(ILh_W_1, 2))+"$\\pm$"+"{:.2f}".format(rounding(ILh_err_W_1, 2))+") dB\nD-band:("+"{:.2f}".format(rounding(ILh_D_1, 2))+"$\\pm$"+"{:.2f}".format(rounding(ILh_err_D_1, 2))+") dB", backgroundcolor="w")
if folders[1]=="copper":
    ax2.plot(nu_W_1[0], S_W_1[0][0], "b", alpha=0.3)
    ax2.plot(nu_W_1[0], env_W_1_v1, "b", lw=4)
    ax2.plot(nu_W_1[0], S_W_1[0][3], "b", alpha=0.3)
    ax2.plot(nu_W_1[0], env_W_1_v2, "b", lw=4)
    ax2.text(nu_W_1[0][len(nu_W_1[0])//2], -0.1, "W-band", color="b")
    ax2.plot(nu_D_1[0], S_D_1[0][0], "g", alpha=0.3)
    ax2.plot(nu_D_1[0], env_D_1_v2, "g", lw=4)
    ax2.text(nu_D_1[0][len(nu_D_1[0])//2], -0.1, "D-band", color="g")
    ax2.axvline(110, ls="--", color="k")
    ax2.set_xlabel("$\\nu$ [GHz]")
    ax2.set_ylabel("S11 [dB]")
    ax2.set_title(title1)
    ax2.text(nu_D_1[0][len(nu_D_1[0])//2], -2.8, "W-band: v1 ("+"{:.2f}".format(rounding(ILh_W_1_v1, 2))+"$\\pm$"+"{:.2f}".format(rounding(ILh_err_W_1_v1, 2))+") dB - v2 ("+"{:.2f}".format(rounding(ILh_W_1_v2, 2))+"$\\pm$"+"{:.2f}".format(rounding(ILh_err_W_1_v2, 2))+") dB\nD-band: v2 ("+"{:.2f}".format(rounding(ILh_D_1_v2, 2))+"$\\pm$"+"{:.2f}".format(rounding(ILh_err_D_1_v2, 2))+") dB", backgroundcolor="w")
f.suptitle("Horn insertion loss", size=50)
f.savefig("IL_results/envelopes_"+folder0+"_"+folder1+".png")

#LINE
#correcting for reflection
S21_corr_W_0, S12_corr_W_0 = correct_transmitted(S_W_0[1])
S21_corr_W_1, S12_corr_W_1 = correct_transmitted(S_W_1[1])
S21_corr_D_0, S12_corr_D_0 = correct_transmitted(S_D_0[1])
S21_corr_D_1, S12_corr_D_1 = correct_transmitted(S_D_1[2])
if folders[1]=="copper":
    norm_S11 = np.loadtxt(folders[1]+"/thru_prima_response.s2p", skiprows=7)[:, 1]
    norm_S21 = np.loadtxt(folders[1]+"/thru_prima_response.s2p", skiprows=7)[:, 3]
    norm_S12 = np.loadtxt(folders[1]+"/thru_prima_response.s2p", skiprows=7)[:, 5]
    norm_S22 = np.loadtxt(folders[1]+"/thru_prima_response.s2p", skiprows=7)[:, 7]
    norm = np.array([-norm_S11, norm_S21, norm_S12, -norm_S22])
    S21_corr_W_1_v1, S12_corr_W_1_v1 = correct_transmitted(S_W_1[2]-norm)
    S21_corr_W_1_v2, S12_corr_W_1_v2 = correct_transmitted(S_W_1[3]-norm)
    S21_corr_D_1_v1, S12_corr_D_1_v1 = correct_transmitted(S_D_1[2])
#dividing into windows
middle_freq_W = [85, 95, 105, 110]
middle_freq_W_0 = [np.abs(nu_W_0[1]-f).argmin() for f in middle_freq_W]
middle_freq_W_1 = [np.abs(nu_W_1[1]-f).argmin() for f in middle_freq_W]
edge_freq_W = [80, 90, 100, 110]
edge_freq_W_0 = [np.abs(nu_W_0[1]-f).argmin() for f in edge_freq_W]
edge_freq_W_1 = [np.abs(nu_W_1[1]-f).argmin() for f in edge_freq_W]
ILwg12_W_0, ILwg12_err_W_0 = IL_v(S12_corr_W_0, middle_freq_W_0)
ILwg21_W_0, ILwg21_err_W_0 = IL_v(S21_corr_W_0, middle_freq_W_0)
ILwg12_W_1, ILwg12_err_W_1 = IL_v(S12_corr_W_1, middle_freq_W_1)
ILwg21_W_1, ILwg21_err_W_1 = IL_v(S21_corr_W_1, middle_freq_W_1)
if folders[1]=="copper":
    ILwg12_W_1_v1, ILwg12_err_W_1_v1 = IL_v(S12_corr_W_1_v1, middle_freq_W_1)
    ILwg21_W_1_v1, ILwg21_err_W_1_v1 = IL_v(S21_corr_W_1_v1, middle_freq_W_1)
    ILwg12_W_1_v2, ILwg12_err_W_1_v2 = IL_v(S12_corr_W_1_v2, middle_freq_W_1)
    ILwg21_W_1_v2, ILwg21_err_W_1_v2 = IL_v(S21_corr_W_1_v2, middle_freq_W_1)
#dividing into windows
middle_freq_D = [115, 125, 135, 145, 155, 165, 170]
middle_freq_D_0 = [np.abs(nu_D_0[1]-f).argmin() for f in middle_freq_D]
middle_freq_D_1 = [np.abs(nu_D_1[1]-f).argmin() for f in middle_freq_D]
edge_freq_D = [110, 120, 130, 140, 150, 160, 170]
edge_freq_D_0 = [np.abs(nu_D_0[1]-f).argmin() for f in edge_freq_D]
edge_freq_D_1 = [np.abs(nu_D_1[1]-f).argmin() for f in edge_freq_D]
ILwg12_D_0, ILwg12_err_D_0 = IL_v(S12_corr_D_0, middle_freq_D_0)
ILwg21_D_0, ILwg21_err_D_0 = IL_v(S21_corr_D_0, middle_freq_D_0)
ILwg12_D_1, ILwg12_err_D_1 = IL_v(S12_corr_D_1, middle_freq_D_1)
ILwg21_D_1, ILwg21_err_D_1 = IL_v(S21_corr_D_1, middle_freq_D_1)
if folders[1]=="copper":
    nu = [nu_W_0[1], nu_D_0[1], nu_W_1[1], nu_D_1[1]]
    edges = [edge_freq_W_0, edge_freq_D_0, edge_freq_W_1, edge_freq_D_1]
    ILwg12_D_1_v1, ILwg12_err_D_1_v1 = IL_v(S12_corr_D_1_v1, middle_freq_D_1)
    ILwg21_D_1_v1, ILwg21_err_D_1_v1 = IL_v(S21_corr_D_1_v1, middle_freq_D_1)
    #ILwg12_D_1_v2, ILwg12_err_D_1_v2 = IL_v(S12_corr_D_1_v2, middle_freq_D_1)
    #ILwg21_D_1_v2, ILwg21_err_D_1_v2 = IL_v(S21_corr_D_1_v2, middle_freq_D_1)

    #version 1
    S21 = [S_W_0[1][1], S_D_0[1][1], (S_W_1[2]-norm)[1], S_D_1[2][1]]
    S21_corr = [S21_corr_W_0, S21_corr_D_0, S21_corr_W_1_v1, S21_corr_D_1_v1]
    S12 = [S_W_0[1][2], S_D_0[1][2], (S_W_1[2]-norm)[2], S_D_1[2][2]]
    S12_corr = [S12_corr_W_0, S12_corr_D_0, S12_corr_W_1_v1, S12_corr_D_1_v1]
    plot_raw(nu, S21, S21_corr, [title0, title0, title1+"_v1", title1+"_v1"], "S21")
    plot_raw(nu, S12, S12_corr, [title0, title0, title1+"_v1", title1+"_v1"], "S12")
    #version 2
    S21 = [S_W_0[1][1], S_D_0[1][1], (S_W_1[3]-norm)[1], S_D_1[2][1]]
    S21_corr = [S21_corr_W_0, S21_corr_D_0, S21_corr_W_1_v2, S21_corr_D_1_v1]
    S12 = [S_W_0[1][2], S_D_0[1][2], (S_W_1[3]-norm)[2], S_D_1[2][2]]
    S12_corr = [S12_corr_W_0, S12_corr_D_0, S12_corr_W_1_v2, S12_corr_D_1_v1]
    plot_raw(nu, S21, S21_corr, [title0, title0, title1+"_v2", title1+"_v2"], "S21")
    plot_raw(nu, S12, S12_corr, [title0, title0, title1+"_v2", title1+"_v2"], "S12")

    #version 1
    IL_21 = [ILwg21_W_0, ILwg21_D_0, ILwg21_W_1_v1, ILwg21_D_1_v1]
    IL_12 = [ILwg12_W_0, ILwg12_D_0, ILwg12_W_1_v1, ILwg12_D_1_v1]
    plot_lineIL(nu, S21_corr, edges, IL_21, [title0, title0, title1+"_v1", title1+"_v1"], "S21")
    plot_lineIL(nu, S12_corr, edges, IL_12, [title0, title0, title1+"_v1", title1+"_v1"], "S12")
    #version 2
    IL_21 = [ILwg21_W_0, ILwg21_D_0, ILwg21_W_1_v2, ILwg21_D_1_v1]
    IL_12 = [ILwg12_W_0, ILwg12_D_0, ILwg12_W_1_v2, ILwg12_D_1_v1]
    plot_lineIL(nu, S21_corr, edges, IL_21, [title0, title0, title1+"_v2", title1+"_v2"], "S21")
    plot_lineIL(nu, S12_corr, edges, IL_12, [title0, title0, title1+"_v2", title1+"_v2"], "S12")
    
else:
    #plotting
    nu = [nu_W_0[1], nu_D_0[1], nu_W_1[1], nu_D_1[1]]
    S21 = [S_W_0[1][1], S_D_0[1][1], S_W_1[1][1], S_D_1[1][1]]
    S21_corr = [S21_corr_W_0, S21_corr_D_0, S21_corr_W_1, S21_corr_D_1]
    S12 = [S_W_0[1][2], S_D_0[1][2], S_W_1[1][2], S_D_1[1][2]]
    S12_corr = [S12_corr_W_0, S12_corr_D_0, S12_corr_W_1, S12_corr_D_1]
    plot_raw(nu, S21, S21_corr, [title0, title0, title1, title1], "S21")
    plot_raw(nu, S12, S12_corr, [title0, title0, title1, title1], "S12")

    edges = [edge_freq_W_0, edge_freq_D_0, edge_freq_W_1, edge_freq_D_1]
    IL_21 = [ILwg21_W_0, ILwg21_D_0, ILwg21_W_1, ILwg21_D_1]
    IL_12 = [ILwg12_W_0, ILwg12_D_0, ILwg12_W_1, ILwg12_D_1]
    plot_lineIL(nu, S21_corr, edges, IL_21, [title0, title0, title1, title1], "S21")
    plot_lineIL(nu, S12_corr, edges, IL_12, [title0, title0, title1, title1], "S12")