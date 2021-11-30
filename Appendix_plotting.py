#!/usr/bin/python
#################
# Run after having run Appendix-MC_calculation.py 
# This script creates several plots showing the development 
# of the deviation of the different uncertainty measures. 
# Date: Sept 25 2020
# By: Karel Kok

import numpy as np
import matplotlib.pyplot as plt
import pickle
import Appendix_MC_calculation as MC_calc
from scipy import stats

# Import deviation and convergence dictionaries
deviations = pickle.load(open("C:\Users\karel\Documents\HU\Sideprojects\uncertainty_measures\App-deviations.p", "rb"))
convergence = pickle.load(open("C:\Users\karel\Documents\HU\Sideprojects\uncertainty_measures\App-convergence.p", "rb"))
development = pickle.load(open("C:\Users\karel\Documents\HU\Sideprojects\uncertainty_measures\App-development.p", "rb"))


# Print mean and uncertainty of the different uncertainty measures as shown in the distribution plot
print "              Mean SDOM SD   SD(10)"
print "Min-max:      "+str(round(MC_calc.stddev(deviations["minmax"])["mean"],2))+" "+str(round(MC_calc.stddev(deviations["minmax"])["uncertainty"]/np.sqrt(deviations["no_draws"]),2))+" "+str(round(MC_calc.stddev(deviations["minmax"])["uncertainty"],2))+" "+str(round(development["minmax_uncs"][8],2))
print "Excl. Extr.: "+str(round(MC_calc.stddev(deviations["exclextr"])["mean"],2))+" "+str(round(MC_calc.stddev(deviations["exclextr"])["uncertainty"]/np.sqrt(deviations["no_draws"]),2))+" "+str(round(MC_calc.stddev(deviations["exclextr"])["uncertainty"],2))+" "+str(round(development["exclextr_uncs"][8],2))
print "Middle 50%:  "+str(round(MC_calc.stddev(deviations["middle"])["mean"],2))+" "+str(round(MC_calc.stddev(deviations["middle"])["uncertainty"]/np.sqrt(deviations["no_draws"]),2))+" "+str(round(MC_calc.stddev(deviations["middle"])["uncertainty"],2))+" "+str(round(development["middle_uncs"][8],2))
print "MAD:         "+str(round(MC_calc.stddev(deviations["mad"])["mean"],2))+" "+str(round(MC_calc.stddev(deviations["mad"])["uncertainty"]/np.sqrt(deviations["no_draws"]),2))+" "+str(round(MC_calc.stddev(deviations["mad"])["uncertainty"],2))+" "+str(round(development["mad_uncs"][8],2))
# print "IQR:         "+str(round(MC_calc.stddev(deviations["iqr"])["mean"],2))+" "+str(round(MC_calc.stddev(deviations["iqr"])["uncertainty"]/np.sqrt(deviations["no_draws"]),2))+" "+str(round(MC_calc.stddev(deviations["iqr"])["uncertainty"],2))+" "+str(round(development["iqr_uncs"][8],2))
print "Std. Dev.:   "+str(round(MC_calc.stddev(deviations["stddev"])["mean"],2))+" "+str(round(MC_calc.stddev(deviations["stddev"])["uncertainty"]/np.sqrt(deviations["no_draws"]),2))+"  "+str(round(MC_calc.stddev(deviations["stddev"])["uncertainty"],2))+" "+str(round(development["stddev_uncs"][8],2))
print "68% meas.:   "+str(round(MC_calc.stddev(deviations["close68"])["mean"],2))+" "+str(round(MC_calc.stddev(deviations["close68"])["uncertainty"]/np.sqrt(deviations["no_draws"]),2))+"  "+str(round(MC_calc.stddev(deviations["close68"])["uncertainty"],2))+" "+str(round(development["close68_uncs"][8],2))
print "Percentage:  "+str(round(MC_calc.stddev(deviations["percmeas"])["mean"],2))+" "+str(round(MC_calc.stddev(deviations["percmeas"])["uncertainty"]/np.sqrt(deviations["no_draws"]),2))+" "+str(round(MC_calc.stddev(deviations["percmeas"])["uncertainty"],2))+" "+str(round(development["percmeas_uncs"][8],2))


print "\nRange of uncertainties"
print "Min-Max:   "+str(round(min(development["minmax_uncs"]) ,2))+" - "+str(round(max(development["minmax_uncs"]) ,2))
print "Excl.Extr: "+str(round(min(development["exclextr_uncs"]) ,2))+" - "+str(round(max(development["exclextr_uncs"]) ,2))
print "Middle 50: "+str(round(min(development["middle_uncs"]) ,2))+" - "+str(round(max(development["middle_uncs"]) ,2))
print "MAD:       "+str(round(min(development["mad_uncs"]) ,2))+" - "+str(round(max(development["mad_uncs"]) ,2))
print "Std.Dev.:  "+str(round(min(development["stddev_uncs"]) ,2))+" - "+str(round(max(development["stddev_uncs"]) ,2))
print "Close68:   "+str(round(min(development["close68_uncs"]) ,2))+" - "+str(round(max(development["minmax_uncs"]) ,2))
print "Percent:   "+str(round(min(development["percmeas_uncs"]) ,2))+" - "+str(round(max(development["minmax_uncs"]) ,2))
min_size_of_sample = 4
max_size_of_sample = 21

linestyle_dict = {
	"solid" : "-",
	"dashed" : 	"--",
	"dashdotted": "-.",
	"dashdashdotted" : (0, (5, 1, 5, 1, 1, 1, 1, 1)), # (offset, (x pt. line, x pt. space, etc.))
	"dotted" : (0,(1,1))
}

fig2 = plt.figure(3)
plt.plot(range(2, len(convergence["minmax"])+2), convergence["minmax"], label = "Min-max", linewidth = 1.7, ls = linestyle_dict["solid"])
plt.plot(range(2, len(convergence["exclextr"])+2), convergence["exclextr"], label = "Exclude extremes", linewidth = 1.7, ls = linestyle_dict["dashed"])
# plt.plot(range(2, len(convergence["percmeas"])+2), convergence["percmeas"], label = "Central 50%")
plt.plot(range(2, len(convergence["middle"])+2), convergence["middle"], label = "Middle 50%", linewidth = 1.7, ls = linestyle_dict["dashdotted"])
plt.plot(range(2, len(convergence["mad"])+2), convergence["mad"], label = "MAD", linewidth = 1.7, ls = linestyle_dict["dashdashdotted"])
# plt.plot(range(2, len(convergence["iqr"])+2), convergence["iqr"], label = "IQR")
plt.plot(range(2, len(convergence["stddev"])+2), convergence["stddev"], label = "Standard deviation", linewidth = 1.7, ls = linestyle_dict["dotted"])
# plt.title("Convergence of uncertainty measures, based un subsets of 8 measurements")
plt.xlabel("Number of repetitions")
plt.ylabel(r"Mean uncertainty deviation $\Delta$")
plt.legend(loc = 1, handlelength=3.5)


fig1 = plt.figure(1)
plt.hist(deviations["minmax"], 50, alpha = .4, label = "Min-max")
plt.hist(deviations["exclextr"], 50, alpha = .4, label = "Exclude extremes")
plt.hist(deviations["middle"], 50, alpha = .4, label = "Middle 50%")
plt.hist(deviations["mad"], 50, alpha = .4, label = "MAD")
# plt.hist(deviations["iqr"], 50, alpha = .4, label = "IQR")
plt.hist(deviations["stddev"], 50, alpha = .4, label = "Standard deviation")
plt.axvline(x=0., color = "black")
# plt.title(r"$10^4$ repetitions with subsets of 8 measurements")
plt.xlabel(r"Uncertainty deviation $\Delta$")
plt.ylabel(r"Counts")
plt.legend()

fig3 = plt.figure(2)
plt.fill_between(range(min_size_of_sample,max_size_of_sample), development["minmax_means"] - development["minmax_uncs"], development["minmax_means"] + development["minmax_uncs"], alpha = .2)
plt.fill_between(range(min_size_of_sample,max_size_of_sample), development["exclextr_means"] - development["exclextr_uncs"], development["exclextr_means"] + development["exclextr_uncs"], alpha = .2)
plt.fill_between(range(min_size_of_sample,max_size_of_sample), development["middle_means"] - development["middle_uncs"], development["middle_means"] + development["middle_uncs"], alpha = .2)
plt.fill_between(range(min_size_of_sample,max_size_of_sample), development["mad_means"] - development["mad_uncs"], development["mad_means"] + development["mad_uncs"], alpha = .2)
plt.fill_between(range(min_size_of_sample,max_size_of_sample), development["stddev_means"] - development["stddev_uncs"], development["stddev_means"] + development["stddev_uncs"], alpha = .2)
plt.plot(range(min_size_of_sample,max_size_of_sample), development["minmax_means"], linewidth = 1.7, label = "Min-max", ls = linestyle_dict["solid"])
plt.plot(range(min_size_of_sample,max_size_of_sample), development["exclextr_means"], linewidth = 1.7, label = "Exclude extremes", ls = linestyle_dict["dashed"])
plt.plot(range(min_size_of_sample,max_size_of_sample), development["middle_means"], linewidth = 1.7, label = "Middle 50%", ls = linestyle_dict["dashdotted"])
plt.plot(range(min_size_of_sample,max_size_of_sample), development["mad_means"], linewidth = 1.7, label = "MAD", ls = linestyle_dict["dashdashdotted"])
plt.plot(range(min_size_of_sample,max_size_of_sample), development["stddev_means"], linewidth = 1.7, label = "Standard deviation", ls = linestyle_dict["dotted"])
plt.axhline(y=0., color = "black")
plt.xlabel(r"Number of measurements per subsample $N$")
plt.ylabel(r"Uncertainty deviation $\Delta$ ")
plt.ylim(-0.9, 1.8)
# plt.title(r"""Development of average uncertainty as a function of the number of draws
# Based on 10$^4$ repetitions.
# Highlighted regions indicate standard deviation of single subsamples.""")
plt.legend(handlelength=3.5)


fig4 = plt.figure(4)
plt.fill_between(range(min_size_of_sample,max_size_of_sample), development["middle_means"] - development["middle_uncs"], development["middle_means"] + development["middle_uncs"], alpha = .2, color = "C2")
# plt.fill_between(range(min_size_of_sample,max_size_of_sample), development["percmeas_means"] - development["percmeas_uncs"], development["percmeas_means"] + development["percmeas_uncs"], alpha = .2, color = "C5")
# plt.fill_between(range(min_size_of_sample,max_size_of_sample), development["close68_means"] - development["close68_uncs"], development["close68_means"] + development["close68_uncs"], alpha = .2, color = "C9")
# plt.fill_between(range(min_size_of_sample,max_size_of_sample), development["iqr_means"] - development["iqr_uncs"], development["iqr_means"] + development["iqr_uncs"], alpha = .2, color="C1")
# plt.fill_between(range(min_size_of_sample,max_size_of_sample), development["stddev_means"] - development["stddev_uncs"], development["stddev_means"] + development["stddev_uncs"], alpha = .2, color = "C4")
plt.plot(range(min_size_of_sample,max_size_of_sample), development["middle_means"], linewidth = 1.7, label = "Middle 50%", ls = linestyle_dict["solid"], color = "C2")
plt.plot(range(min_size_of_sample,max_size_of_sample), development["close68_means"], linewidth = 1.7, label = "68% of measurements", ls = linestyle_dict["dashed"], color = "C9")
plt.plot(range(min_size_of_sample,max_size_of_sample), development["percmeas_means"], linewidth = 1.7, label = "76% of measurements", ls = linestyle_dict["dashdotted"], color = "C5")
plt.plot(range(min_size_of_sample,max_size_of_sample), development["iqr_means"], linewidth = 1.7, label = "IQR", ls = linestyle_dict["dotted"], color="C1")
# plt.plot(range(min_size_of_sample,max_size_of_sample), development["stddev_means"], linewidth = 1.7, label = "Standard deviation", ls = linestyle_dict["dotted"], color = "C4")
plt.axhline(y=0., color = "black")
plt.xlabel(r"Number of measurements per subsample $N$")
plt.ylabel(r"Uncertainty deviation $\Delta$")
plt.ylim(-0.9, 1.8)
# plt.title(r"""Development of average uncertainty as a function of the number of draws
# Based on 10$^4$ repetitions.
# Highlighted regions indicate standard deviation of single subsamples.""")
plt.legend(handlelength=3.5)


plt.show()