#!/usr/bin/python
#################
# The Monte-Carlo calculation of the deviations for the different uncertainty measures.
# When calculate_distributions is true, the distributions of the deviations are calculated
# for a subsample size of N = 8.
# When calculate_convergence is true, the mean deviation as a function of repetitions is
# calculated, indicating the convergence of the mean value.
# When calculate_sample_size_distributions is true, the mean and uncertainty of the 
# deviations is calculated for subsample sizes ranging from 4-20.
# Each routine creates a pickle file that can be read and plotted by Appendix-plotting.py
# Date: Sept 25 2020
# By: Karel Kok

import numpy as np
import pickle
from random import sample

# Chose which parts of the simulation have to be calculated
calculate_distributions = True
calculate_convergence = True # Requires calculate_distributions to be true
calculate_sample_size_distributions = True

def stddev(sample_set, sample = True):
	"""Takes an array and calculates its mean and uncertainty. If the parameter sample is set to true, the returned uncertainty is the sample standard deviation for a (limited) subsample is calculated, when nothing is provided, the population standard deviation is calculated. The function returns a dictionary with keys "mean" and "uncertainty"."""
	meanval = 1.*sum(sample_set)/len(sample_set)
	if sample: uncert = np.sqrt(1./(len(sample_set)-1.) * sum((sample_set-meanval)**2) )
	else: uncert = np.sqrt(1./len(sample_set) * sum((sample_set-meanval)**2) )
	return {"mean" : meanval, "uncertainty" : uncert}

def minmax(sample_set):
	"""Takes an array and calculates its mean and uncertainty. The uncertainty is the largest distance of the min/max to the mean. The function returns a dictionary with keys "mean" and "uncertainty"."""
	meanval = 1.*sum(sample_set)/len(sample_set)
	mindist = meanval - min(sample_set)
	maxdist = max(sample_set) - meanval
	uncert = max(mindist, maxdist)
	return {"mean" : meanval, "uncertainty" : uncert}

def exclextr(sample_set):
	"""Takes an array and calculates its mean and uncertainty. The variable extremesexcluded indicates how many of the extreme values from the set have to be excluded. 1 indicating that 1 max and 1 min value are excluded. The uncertainty is the largest distance of the min/max to the mean. The function returns a dictionary with keys "mean" and "uncertainty"."""
	extremesexcluded = 1
	meanval = 1.*sum(sample_set)/len(sample_set)
	sample_set = sorted(sample_set)[extremesexcluded:len(sample_set) - extremesexcluded]
	mindist = meanval - min(sample_set)
	maxdist = max(sample_set) - meanval
	uncert = max(mindist, maxdist)
	return {"mean" : meanval, "uncertainty" : uncert}
	
def middle(sample_set):
	"""Takes an array and calculates its mean and uncertainty. The variable percentage set at 50 indicates that 50% of the sorted set are used in the uncertainty calculation. The uncertainty is the largest distance of the min/max to the mean. The function returns a dictionary with keys "mean" and "uncertainty"."""
	percentage = 50
	meanval = 1.*sum(sample_set)/len(sample_set)
	sample_set = sorted(sample_set)
	cutmeasurements = int((percentage/2.)/100.*len(sample_set))
	sample_set = sample_set[cutmeasurements:len(sample_set) - cutmeasurements]
	mindist = meanval - min(sample_set)
	maxdist = max(sample_set) - meanval
	uncert = max(mindist, maxdist)
	return {"mean" : meanval, "uncertainty" : uncert}

def percmeas(sample_set):
	"""Takes an array and first calculates how many items should be discarded so that the percentage of remaining measurements is the closest to a certain percentage. This percentage is set by the variable fraction. Then it calculates the min-max interval of the remaining set."""
	fraction = .76
	meanval = 1.*sum(sample_set)/len(sample_set)
	differences = np.abs(sample_set - meanval)
	# Identify the number of measurements that need to be discarded so that the remaining set contains the closest percentage to 68% of the original set as possible.
	N = len(sample_set)
	abs_percentage_difference = np.abs((np.arange(N)+1.)/N - fraction)
	smallest_percentage_difference = min(abs_percentage_difference)
	smallest_id = np.argwhere(abs_percentage_difference == smallest_percentage_difference)[0][0]
	number_of_items_to_discard = N-(smallest_id+1)
	
	# Discard the biggest outliers as compared to the mean
	for i in range(number_of_items_to_discard):
		cut_index = np.where(differences == max(differences))[0][0]
		sample_set = np.delete(sample_set, cut_index)
		differences = np.delete(differences, cut_index)
	# Calculate uncertainty
	mindist = meanval - min(sample_set)
	maxdist = max(sample_set) - meanval
	uncert = max(mindist, maxdist)
	return {"mean" : meanval, "uncertainty" : uncert}
	
def mad(sample_set):
	"""takes an array and calculates its mean and uncertainty. The uncertainty is the mean absolute deviation (MAD). The function returns a dictionary with keys "mean" and "uncertainty"."""
	meanval = 1.*sum(sample_set)/len(sample_set)
	uncert = 1.*sum( np.abs( sample_set - meanval ) )/ len(sample_set)
	return {"mean" : meanval, "uncertainty" : uncert}

def iqr(sample_set):
	"""Takes an array and calculates the mean and uncertainty. The uncertainty is the Inter Quartile Range (IQR). The function returns a dictionary with keys "mean" and "uncertainty"."""
	meanval = 1.*sum(sample_set)/len(sample_set)
	sample_set = sorted(sample_set)
	if (len(sample_set) % 2 == 0):
		lower_quart = sample_set[:int(len(sample_set)/2)]
		lower_bound = np.median(lower_quart)
		upper_quart = sample_set[int(len(sample_set)/2):]
		upper_bound = np.median(upper_quart)
		uncert = max(np.abs(lower_bound - meanval), np.abs(upper_bound - meanval))	
	else:
		lower_quart = sample_set[:int(len(sample_set)/2+1)]
		lower_bound = np.median(lower_quart)
		upper_quart = sample_set[int(len(sample_set)/2):]
		upper_bound = np.median(upper_quart)
		uncert = max(np.abs(lower_bound - meanval), np.abs(upper_bound - meanval))
	return {"mean" : meanval, "uncertainty" : uncert}

def close68(sample_set):
	"""Takes an array and first calculates how many items should be discarded so that the percentage of remaining measurements is the closest to 68%. Then it calculates the min-max interval of the remaining set."""
	meanval = 1.*sum(sample_set)/len(sample_set)
	differences = np.abs(sample_set - meanval)
	# Identify the number of measurements that need to be discarded so that the remaining set contains the closest percentage to 68% of the original set as possible.
	N = len(sample_set)
	abs_percentage_difference = np.abs((np.arange(N)+1.)/N - 0.68)
	smallest_percentage_difference = min(abs_percentage_difference)
	smallest_id = np.argwhere(abs_percentage_difference == smallest_percentage_difference)[0][0]
	number_of_items_to_discard = N-(smallest_id+1)
	
	# Discard the biggest outliers as compared to the mean
	for i in range(number_of_items_to_discard):
		cut_index = np.where(differences == max(differences))[0][0]
		sample_set = np.delete(sample_set, cut_index)
		differences = np.delete(differences, cut_index)
	# Calculate uncertainty
	mindist = meanval - min(sample_set)
	maxdist = max(sample_set) - meanval
	uncert = max(mindist, maxdist)
	return {"mean" : meanval, "uncertainty" : uncert}


def draw_set(SET, no_iterations, no_draws, return_distribution):
	"""Function that lets you draw no_draws from the SET (making a SUBSET), calculate the different uncertainties, calculate the difference of this uncertainty with the standard deviation of the complete set, and express this in standard deviations. This is done no_iterations times."""
	# Make empty numpy arrays
	frac_stddev_minmax = np.array([])
	frac_stddev_exclextr = np.array([])
	frac_stddev_percmeas = np.array([])
	frac_stddev_middle = np.array([])
	frac_stddev_mad = np.array([])
	frac_stddev_iqr = np.array([])
	frac_stddev_close68 = np.array([])
	frac_stddev_stddev = np.array([])
	

	# Run the calculational process no_iterations times
	for run in range(no_iterations):
		# Draw the SUBSET
		SUBSET = sample(sorted(SET),no_draws)
		# Calculate uncertainties
		frac_stddev_minmax = np.append(frac_stddev_minmax, (minmax(SUBSET)["uncertainty"] - real_stddev) / real_stddev)
		frac_stddev_exclextr = np.append(frac_stddev_exclextr, (exclextr(SUBSET)["uncertainty"] - real_stddev) / real_stddev)
		frac_stddev_percmeas = np.append(frac_stddev_percmeas, (percmeas(SUBSET)["uncertainty"] - real_stddev) / real_stddev)
		frac_stddev_middle = np.append(frac_stddev_middle, (middle(SUBSET)["uncertainty"] - real_stddev) / real_stddev)
		frac_stddev_mad = np.append(frac_stddev_mad, (mad(SUBSET)["uncertainty"] - real_stddev) / real_stddev)
		frac_stddev_iqr = np.append(frac_stddev_iqr, (iqr(SUBSET)["uncertainty"] - real_stddev) / real_stddev)
		frac_stddev_close68 = np.append(frac_stddev_close68, (close68(SUBSET)["uncertainty"] - real_stddev) / real_stddev)
		frac_stddev_stddev = np.append(frac_stddev_stddev, (stddev(SUBSET, True)["uncertainty"] - real_stddev) / real_stddev)
	
	# Return the complete distribution
	if return_distribution:
		return (frac_stddev_minmax, frac_stddev_exclextr, frac_stddev_percmeas, frac_stddev_middle,  frac_stddev_mad, frac_stddev_iqr, frac_stddev_close68, frac_stddev_stddev)
	
	# Only return the mean and standard deviation of these uncertainty measures, as compared to the standard deviation of the whole set.
	else:
		return (stddev(frac_stddev_minmax)["mean"], stddev(frac_stddev_minmax)["uncertainty"], stddev(frac_stddev_exclextr)["mean"], stddev(frac_stddev_exclextr)["uncertainty"], stddev(frac_stddev_percmeas)["mean"], stddev(frac_stddev_percmeas)["uncertainty"], stddev(frac_stddev_middle)["mean"], stddev(frac_stddev_middle)["uncertainty"], stddev(frac_stddev_mad)["mean"], stddev(frac_stddev_mad)["uncertainty"], stddev(frac_stddev_iqr)["mean"], stddev(frac_stddev_iqr)["uncertainty"], stddev(frac_stddev_close68)["mean"], stddev(frac_stddev_close68)["uncertainty"], stddev(frac_stddev_stddev)["mean"], stddev(frac_stddev_stddev)["uncertainty"])

if __name__=="__main__":

	# Create the base set and calculate mean and uncertainty.
	np.random.seed(2)
	
	SET = np.random.normal(100,20,1000)
	real_mean = stddev(SET)["mean"]
	real_stddev = stddev(SET)["uncertainty"]

	# Routine to calculate the distributions of the uncertainty measures, as compared to the standard deviation of the complete set.
	if calculate_distributions:
		# Run the monte carlo simulation
		no_draws = 10
		dev_minmax, dev_exclextr, dev_percmeas, dev_middle, dev_mad, dev_iqr, dev_close68, dev_stddev = draw_set(SET, 10000, no_draws, True)
		# Write the results to a dictionary
		deviations = {}
		deviations["minmax"] = dev_minmax
		deviations["exclextr"] = dev_exclextr
		deviations["percmeas"] = dev_percmeas
		deviations["middle"] = dev_middle
		deviations["mad"] = dev_mad
		deviations["iqr"] = dev_iqr
		deviations["close68"] = dev_close68
		deviations["stddev"] = dev_stddev
		deviations["SET"] = SET
		deviations["no_draws"] = no_draws
		pickle.dump(deviations, open("./App-deviations.p", "wb"))
		print("Deviation dictionary succesfully saved")

		# Routine to calculate how the uncertainty of the set of uncertainties converges with increasing iterations.
		if calculate_convergence:
			convergence_minmax = convergence_exclextr = convergence_percmeas = convergence_middle =  convergence_mad = convergence_iqr = convergence_close68 = convergence_stddev = np.array([])
			for i in range(len(dev_minmax)):
				convergence_minmax = np.append(convergence_minmax, stddev(dev_minmax[:i+1],False)["mean"])
				convergence_exclextr = np.append(convergence_exclextr, stddev(dev_exclextr[:i+1],False)["mean"])
				convergence_percmeas = np.append(convergence_percmeas, stddev(dev_percmeas[:i+1],False)["mean"])
				convergence_middle = np.append(convergence_middle, stddev(dev_middle[:i+1],False)["mean"])
				convergence_mad = np.append(convergence_mad, stddev(dev_mad[:i+1],False)["mean"])
				convergence_iqr = np.append(convergence_iqr, stddev(dev_iqr[:i+1],False)["mean"])
				convergence_close68 = np.append(convergence_close68, stddev(dev_close68[:i+1],False)["mean"])
				convergence_stddev = np.append(convergence_stddev, stddev(dev_stddev[:i+1],False)["mean"])
			
			# Write the whole thing to a dictionary
			convergence = {}
			convergence["minmax"] = convergence_minmax
			convergence["exclextr"] = convergence_exclextr
			convergence["percmeas"] = convergence_percmeas
			convergence["middle"] = convergence_middle
			convergence["mad"] = convergence_mad
			convergence["iqr"] = convergence_iqr
			convergence["close68"] = convergence_close68
			convergence["stddev"] = convergence_stddev
			convergence["no_draws"] = no_draws
			pickle.dump(convergence, open("./App-convergence.p", "wb"))
			print("Convergence dictionaries saved")

	# Routine to calculate how the distributions of uncertainties develops with different number of draws.
	if calculate_sample_size_distributions:
		# Make empty numpy arrays
		minmax_means = minmax_uncs = exclextr_means = exclextr_uncs = percmeas_means = percmeas_uncs = middle_means = middle_uncs = mad_means = mad_uncs = iqr_means = iqr_uncs = close68_means = close68_uncs = stddev_means = stddev_uncs = np.array([])

		min_size_of_sample = 4
		max_size_of_sample = 21

		# Execute the draw_set function for different SUBSAMPLE sizes. They will range from min_size_of_sample to max_size_of_sample.
		for no_measurements in range(min_size_of_sample,max_size_of_sample):
			minmax_mean, minmax_unc, exclextr_mean, exclextr_unc, percmeas_mean, percmeas_unc, middle_mean, middle_unc, mad_mean, mad_unc, iqr_mean, iqr_unc, close68_mean, close68_unc, stddev_mean, stddev_unc = draw_set(SET, 10000, no_measurements, False)
			minmax_means = np.append(minmax_means, minmax_mean)
			minmax_uncs = np.append(minmax_uncs, minmax_unc)
			percmeas_means = np.append(percmeas_means, percmeas_mean)
			percmeas_uncs = np.append(percmeas_uncs, percmeas_unc)
			exclextr_means = np.append(exclextr_means, exclextr_mean)
			exclextr_uncs = np.append(exclextr_uncs, exclextr_unc)
			middle_means = np.append(middle_means, middle_mean)
			middle_uncs = np.append(middle_uncs, middle_unc)
			mad_means = np.append(mad_means, mad_mean)
			mad_uncs = np.append(mad_uncs, mad_unc)
			iqr_means = np.append(iqr_means, iqr_mean)
			iqr_uncs = np.append(iqr_uncs, iqr_unc)
			close68_means = np.append(close68_means, close68_mean)
			close68_uncs = np.append(close68_uncs, close68_unc)
			stddev_means = np.append(stddev_means, stddev_mean)
			stddev_uncs = np.append(stddev_uncs, stddev_unc)

		# Write the whole thing to a dictionary
		development = {}
		development["minmax_means"] = minmax_means
		development["minmax_uncs"] = minmax_uncs
		development["percmeas_means"] = percmeas_means
		development["percmeas_uncs"] = percmeas_uncs
		development["exclextr_means"] = exclextr_means
		development["exclextr_uncs"] = exclextr_uncs
		development["middle_means"] = middle_means
		development["middle_uncs"] = middle_uncs
		development["mad_means"] = mad_means
		development["mad_uncs"] = mad_uncs
		development["iqr_means"] = iqr_means
		development["iqr_uncs"] = iqr_uncs
		development["close68_means"] = close68_means
		development["close68_uncs"] = close68_uncs
		development["stddev_means"] = stddev_means
		development["stddev_uncs"] = stddev_uncs
		pickle.dump(development, open("./App-development.p", "wb"))
		print("Development dictionary succesfully saved")
