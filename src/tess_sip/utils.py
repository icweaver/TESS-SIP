import numpy as np

# Averages the xs and associated ys in each grouping of x
def bin_data(x, y, y_err, binsize=0.1):
    idxs = idxs_of_groups(x, binsize)
    groups = [(x[idx], y[idx], y_err[idx]) for idx in idxs]
    x_avg, y_avg, y_avg_err = [], [], []

    for group in groups:
        x_avg.append(np.mean(group[0]))
        y_avg_and_err = weighted_avg_and_std(group[1], (1.0/group[2])**2)
        y_avg.append(y_avg_and_err[0])
        y_avg_err.append(y_avg_and_err[1])

    return x_avg, y_avg, y_avg_err

# Given a sorted vector `v`, return the set of groups (by idx) satisfying
# the condition
# that all points in that group are ≤ Δv of the first point
def idxs_of_groups(v, dv):
    idx_start = 0
    groups = []
    group = [idx_start]

    for i in range(1, len(v)):
        if v[i] - v[idx_start] <= dv:
            group.append(i)
        else:
            groups.append(group)
            idx_start = i
            group = [i]
    groups.append(group)

    return groups

def weighted_avg_and_std(values, weights):
    """ Return the weighted average and standard deviation. values, weights -- Numpy ndarrays with the same shape."""
    average = np.average(values, weights=weights) #weights = 1./err_bar^2. Where err_bar=std & err_bar^2 = variance
    variance = np.average((values-average)**2, weights=weights) # Fast and numerically precise
    return average, np.sqrt(variance)
