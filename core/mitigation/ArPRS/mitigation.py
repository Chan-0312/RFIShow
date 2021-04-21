import numpy as np
from numba import njit, prange
from scipy import ndimage
from scipy.optimize import curve_fit
from .baseline import ArPLS, gaussian_filter

#####################
# Global parameters #
#####################

# Maximum neighbourhood size
MAX_PIXELS = 8

# smoothing default params
KERNEL_M = 40
KERNEL_N = 20
SIGMA_M = 7.5
SIGMA_N = 15

# dilation default params
STRUCT_SIZE = 3

p = 1.5
m = np.arange(1, MAX_PIXELS)
M = 2 ** (m - 1)


@njit
def _sumthreshold(data, mask, i, chi, ds0, ds1):
    """
    The operation of summing and thresholding.
    copy from https://github.com/cosmo-ethz/seek/blob/master/seek/mitigation/sum_threshold.py

    Input:
        data:
            input data for sumthreshold
        mask:
            original mask
        i:
            number of iterations
        chi:
            thresholding criteria
        ds0:
            dimension of the first axis
        ds1:
            dimension of hte second axis

    Output:
        SumThredshold mask
    """
    tmp_mask = mask[:]
    for x in range(ds0):
        sum = 0.0
        cnt = 0

        for ii in range(0, i):
            if mask[x, ii] != True:
                sum += data[x, ii]
                cnt += 1

        for y in range(i, ds1):
            if sum > chi * cnt:
                for ii2 in range(0, i):
                    tmp_mask[x, y - ii2 - 1] = True

            if mask[x, y] != True:
                sum += data[x, y]
                cnt += 1

            if mask[x, y - i] != 1:
                sum -= data[x, y - i]
                cnt -= 1

    return tmp_mask


def _run_sumthreshold(data, init_mask, eta, M, chi_i, **sm_kwargs):
    """
    Perform one SumThreshold operation: sum the un-masked data after
    subtracting a smooth background and threshold it.
    copy from https://github.com/cosmo-ethz/seek/blob/master/seek/mitigation/sum_threshold.py

    Input:
        data:
            data
        init_mask:
            initial mask
        eta:
            number that scales the chi value for each iteration
        M:
            number of iterations
        chi:
            thresholding criteria
        sm_kwargs:
            smoothing keyword
    Output:
        SumThreshold mask
    """

    smoothed_data = gaussian_filter(data, init_mask, **sm_kwargs)
    res = data - smoothed_data

    st_mask = init_mask.copy()

    for m, chi in zip(M, chi_i):
        chi = chi / eta
        if m == 1:
            st_mask = st_mask | (chi <= res)
        else:
            st_mask = _sumthreshold(res, st_mask, m, chi, *res.shape)
            st_mask = _sumthreshold(res.T, st_mask.T, m, chi, *res.T.shape).T

    return st_mask


def _run_sumthreshold_arpls(diff_temp, chi_1=3):
    '''
    A function to call sumthreshold for a list of threshold value

    Inputs:
        diff_temp:
            The difference of the data and the estimated baseline
        chi_1:
            The first threshold value
    Output:
        SumThredshold mask

    '''
    res = diff_temp.copy()
    # use first threshold value to compute the whole list of threshold for sumthreshold algorithm
    chi_i = chi_1 / p ** np.log2(m)
    if len(res.shape) == 1:
        res = res[:, np.newaxis]
    st_mask = np.full(res.shape, False)

    for mi, chi in zip(M, chi_i):
        if mi == 1:
            st_mask = st_mask | (chi <= res)
        else:
            if diff_temp.shape[-1] != 1:
                st_mask = _sumthreshold(res, st_mask, mi, chi, *res.shape)

            st_mask = _sumthreshold(res.T, st_mask.T, mi, chi, *res.T.shape).T

    return st_mask


def ksigma(data):
    '''
    The automatic parameter setup based on the K sigma criterion

    Inputs:
        data:
            input data
    Output:
        popt:
            the estimated standard deviation of the input data
    '''
    med = np.median(data)
    hist_result = np.histogram(data, bins=50, density=True)
    x_val = (hist_result[1][1:] + hist_result[1][:-1]) / 2

    def gaus(x, sigma):
        return np.exp(-(x - med) ** 2 / (2 * sigma ** 2)) / (np.sqrt(2 * np.pi) * sigma)

    popt, pcov = curve_fit(gaus, x_val, hist_result[0], p0=[1])
    return popt


def blob_mitigation(data, baseline, line_mask, threshold):
    '''
    The function to identify the blob RFI

    Inputs:
        data:
            the input data
        baseline:
            the estimated baseline of the input data
        line_mask:
            the band mask
        threshold:
            the first threshold value of the sumthreshold algorithm
    Outputs:
        blob RFI mask
    '''
    valid_index = np.where(line_mask == False)[0]
    valid_data = data - baseline[:, np.newaxis]
    valid_data = valid_data[valid_index]
    point_mask_temp = _run_sumthreshold_arpls(valid_data, chi_1=threshold)
    point_mask = np.full(data.shape, False)
    point_mask[valid_index] = point_mask_temp

    return point_mask


def arpls_mask(data):
    """
    Computes a mask to cover the RFI in a data set based on ArPLS-ST.

    Inputs:
        data:
            array containing the signal and RFI

    Outputs:
        mask:
            the mask covering the identified RFI
    """

    # compute SED curve
    freq_mean = data.mean(axis=1)
    # estimate the baseline of SED curve based on ArPLS
    bl = ArPLS(freq_mean, lam=100000)
    # compute the difference between SED curve and its baseline
    diff = freq_mean - bl
    # compute the first threshold value for band RFI mitigation
    popt = ksigma(diff)
    # band RFI mitigation
    line_mask = _run_sumthreshold_arpls(diff, 2 * popt)

    line_index = np.where(line_mask == True)[0]
    final_curve = freq_mean.copy()
    final_curve[line_index] = bl[line_index]
    valid_index = np.where(line_mask == False)[0]
    valid_data = data - final_curve[:, np.newaxis]
    valid_data = valid_data[valid_index]

    # compute the first threshold value for blob RFI mitgation
    popt_point = ksigma(valid_data)
    # blob RFI mitigation
    mask = blob_mitigation(data, final_curve, line_mask, 5 * popt_point)

    mask[line_index] = True
    return mask
    # blob_mask = mask.copy()
    # mask[line_index] = True
    # return mask, line_mask, blob_mask


def st_mask(data, eta_i=[0.5, 0.55, 0.62, 0.75, 1], chi_1=20):
    """
    Computes a mask to cover the RFI in a data set.
    copy from https://github.com/cosmo-ethz/seek/blob/master/seek/mitigation/sum_threshold.py

    :param data: array containing the signal and RFI
    :param chi_1: First threshold
    :param eta_i: List of sensitivities

    :return mask: the mask covering the identified RFI
    """
    # 将字符串转换
    if isinstance(chi_1, str):
        chi_1 = int(chi_1)
    if isinstance(eta_i, str):
        eta_i = eta_i.replace('[', '')
        eta_i = eta_i.replace(']', '')
        eta_i = list(map(float, eta_i.split(",")))

    mask = np.full(data.shape, False)
    chi_i = chi_1 / p ** np.log2(m)

    st_mask = mask
    for eta in eta_i:
        st_mask = _run_sumthreshold(data, st_mask, eta, M, chi_i)

    return st_mask


def get_sm_kwargs(kernel_m=KERNEL_M, kernel_n=KERNEL_N, sigma_m=SIGMA_M, sigma_n=SIGMA_N):
    """
    Creates a dict with the smoothing keywords.

    :param kernel_m: kernel window size in axis=1
    :param kernel_n: kernel window size in axis=0
    :param sigma_m: kernel sigma in axis=1
    :param sigma_n: kernel sigma in axis=0

    :return: dictionary with the smoothing keywords
    """
    return dict(M=kernel_m, N=kernel_n, sigma_m=sigma_m, sigma_n=sigma_n)


def get_di_kwargs(struct_size_0=STRUCT_SIZE, struct_size_1=STRUCT_SIZE):
    """
    Creates a dict with the dilation keywords.

    :param struct_size_0: struct size in axis=0
    :param struct_size_1: struct size in axis=1

    :return: dictionary with the dilation keywords
    """
    return dict(struct_size_0=struct_size_0, struct_size_1=struct_size_1)


def binary_mask_dilation(mask, struct_size_0, struct_size_1):
    """
    Dilates the mask.

    copy from https://github.com/cosmo-ethz/seek/blob/master/seek/mitigation/sum_threshold.py

    :param mask: original mask
    :param struct_size_0: dilation parameter
    :param struct_size_1: dilation parameter

    :return: dilated mask
    """
    struct = np.ones((struct_size_0, struct_size_1), np.bool)
    return ndimage.binary_dilation(mask, structure=struct, iterations=2)