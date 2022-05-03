import os
import numpy as np
import librosa
from scipy.fftpack import next_fast_len
from scipy.signal import spectrogram


def __get_norm(norm):
    if norm == 0 or norm is None:
        return None, None
    else:
        try:
            norm1, norm2 = norm
        except TypeError:
            norm1 = norm2 = norm
        return norm1, norm2


def __freq_ind(freq, f0):
    try:
        return [np.argmin(np.abs(freq - f)) for f in f0]
    except TypeError:
        return np.argmin(np.abs(freq - f0))


def __product_other_freqs(spec, indices, synthetic=(), t=None):
    p1 = np.prod([amplitude * np.exp(2j * np.pi * freq * t + phase)
                  for (freq, amplitude, phase) in synthetic], axis=0)
    p2 = np.prod(spec[:, indices[len(synthetic):]], axis=1)
    return p1 * p2


def _polycoherence_0d(data, fs, *freqs, norm=2, synthetic=(), **kwargs):
    """Polycoherence between freqs and sum of freqs"""
    norm1, norm2 = __get_norm(norm)
    freq, t, spec = spectrogram(data, fs=fs, mode='complex', **kwargs)
    ind = __freq_ind(freq, freqs)
    sum_ind = __freq_ind(freq, np.sum(freqs))
    spec = np.transpose(spec, [1, 0])
    p1 = __product_other_freqs(spec, ind, synthetic, t)
    p2 = np.conjugate(spec[:, sum_ind])
    coh = np.mean(p1 * p2, axis=0)
    if norm is not None:
        coh = np.abs(coh)
        coh **= 2
        temp2 = np.mean(np.abs(p1) ** norm1 * np.abs(p2) ** norm2, axis=0)
        coh /= temp2
        coh **= 0.5
    return coh


def _polycoherence_1d(data, fs, *freqs, norm=2, synthetic=(), **kwargs):
    """
    Polycoherence between f1 given freqs and their sum as a function of f1
    """
    norm1, norm2 = __get_norm(norm)
    freq, t, spec = spectrogram(data, fs=fs, mode='complex', **kwargs)
    spec = np.transpose(spec, [1, 0])
    ind2 = __freq_ind(freq, freqs)
    ind1 = np.arange(len(freq) - sum(ind2))
    sumind = ind1 + sum(ind2)
    otemp = __product_other_freqs(spec, ind2, synthetic, t)[:, None]
    temp = spec[:, ind1] * otemp
    temp2 = np.mean(np.abs(temp) ** 2, axis=0)
    temp *= np.conjugate(spec[:, sumind])
    coh = np.mean(temp, axis=0)
    if norm is not None:
        coh = np.abs(coh)
        coh **= 2
        temp2 *= np.mean(np.abs(spec[:, sumind]) ** 2, axis=0)
        coh /= temp2
        coh **= 0.5
    return freq[ind1], coh


def _polycoherence_1d_sum(data, fs, f0, *ofreqs, norm=2,
                          synthetic=(), **kwargs):
    """Polycoherence with fixed frequency sum f0 as a function of f1"""
    norm1, norm2 = __get_norm(norm)
    freq, t, spec = spectrogram(data, fs=fs, mode='complex', **kwargs)
    spec = np.transpose(spec, [1, 0])
    ind3 = __freq_ind(freq, ofreqs)
    otemp = __product_other_freqs(spec, ind3, synthetic, t)[:, None]
    sumind = __freq_ind(freq, f0)
    ind1 = np.arange(np.searchsorted(freq, f0 - np.sum(ofreqs)))
    ind2 = sumind - ind1 - sum(ind3)
    temp = spec[:, ind1] * spec[:, ind2] * otemp
    if norm is not None:
        temp2 = np.mean(np.abs(temp) ** 2, axis=0)
    temp *= np.conjugate(spec[:, sumind, None])
    coh = np.mean(temp, axis=0)
    if norm is not None:
        coh = np.abs(coh)
        coh **= 2
        temp2 *= np.mean(np.abs(spec[:, sumind]) ** 2, axis=0)
        coh /= temp2
        coh **= 0.5
    return freq[ind1], coh


def _polycoherence_2d(data, fs, *ofreqs, norm=2, flim1=None, flim2=None,
                      synthetic=(), **kwargs):
    """
    Polycoherence between freqs and their sum as a function of f1 and f2
    """
    norm1, norm2 = __get_norm(norm)
    freq, t, spec = spectrogram(data, fs=fs, mode='complex', **kwargs)
    spec = np.require(spec, 'complex64')
    spec = np.transpose(spec, [1, 0])  # transpose (f, t) -> (t, f)
    if flim1 is None:
        flim1 = (0, (np.max(freq) - np.sum(ofreqs)) / 2)
    if flim2 is None:
        flim2 = (0, (np.max(freq) - np.sum(ofreqs)) / 2)
    ind1 = np.arange(*np.searchsorted(freq, flim1))
    ind2 = np.arange(*np.searchsorted(freq, flim2))
    ind3 = __freq_ind(freq, ofreqs)
    otemp = __product_other_freqs(spec, ind3, synthetic, t)[:, None, None]
    sumind = ind1[:, None] + ind2[None, :] + sum(ind3)
    temp = spec[:, ind1, None] * spec[:, None, ind2] * otemp
    if norm is not None:
        temp2 = np.mean(np.abs(temp) ** norm1, axis=0)
    temp *= np.conjugate(spec[:, sumind])
    coh = np.mean(temp, axis=0)
    del temp
    if norm is not None:
        coh = np.abs(coh, out=coh)
        coh **= 2
        temp2 *= np.mean(np.abs(spec[:, sumind]) ** norm2, axis=0)
        coh /= temp2
        coh **= 0.5
    return freq[ind1], freq[ind2], coh


def polycoherence(data, *args, dim=2, **kwargs):
    """
    Polycoherence between frequencies and their sum frequency

    Polycoherence as a function of two frequencies.

    |<prod(spec(fi)) * conj(spec(sum(fi)))>| ** n0 /
        <|prod(spec(fi))|> ** n1 * <|spec(sum(fi))|> ** n2

    i ... 1 - N: N=2 bicoherence, N>2 polycoherence
    < > ... averaging
    | | ... absolute value

    data: 1d data
    fs: sampling rate
    ofreqs: further positional arguments are fixed frequencies

    dim:
        2 - 2D polycoherence as a function of f1 and f2, ofreqs are additional
            fixed frequencies (default)
        1 - 1D polycoherence as a function of f1, at least one fixed frequency
            (ofreq) is expected
        'sum' - 1D polycoherence with fixed frequency sum. The first argument
            after fs is the frequency sum. Other fixed frequencies possible.
        0 - polycoherence for fixed frequencies
    norm:
        2 - return polycoherence, n0 = n1 = n2 = 2 (default)
        0 - return polyspectrum, <prod(spec(fi)) * conj(spec(sum(fi)))>
        tuple (n1, n2): general case with n0=2
    synthetic:
        used for synthetic signal for some frequencies,
        list of 3-item tuples (freq, amplitude, phase), freq must coincide
        with the first fixed frequencies (ofreq, except for dim='sum')
    flim1, flim2: for 2D case, frequency limits can be set
    **kwargs: are passed to scipy.signal.spectrogram. Important are the
        parameters nperseg, noverlap, nfft.
    """
    N = len(data)
    kwargs.setdefault('nperseg', N // 20)
    kwargs.setdefault('nfft', next_fast_len(N // 10))
    if dim == 0:
        f = _polycoherence_0d
    elif dim == 1:
        f = _polycoherence_1d
    elif dim == 'sum':
        f = _polycoherence_1d_sum
    elif dim == 2:
        f = _polycoherence_2d
    else:
        raise
    return f(data, *args, **kwargs)

def get_all_filenames(file_dir):
    all_files = [file for file in os.listdir(file_dir)]
    # print(all_files)
    return all_files


def get_bi_spectrum(file_folder, class_list, data_num=2000):
    dataset = np.zeros((1,256,256,1))
    for class_nam in class_list:
        path = os.path.join(file_folder, class_nam)
        all_files = get_all_filenames(path)
        index = 0
        for name in all_files[:data_num]:
            file_path = os.path.join(path, name)
            sig, sr = librosa.load(file_path, sr=1000) # load heart sound data
            # down_sig =  librosa.resample(sig, 8000, 1000, res_type='sinc_best') # down-sampling
            freq1, freq2, bi_spectrum = polycoherence(sig, nfft=1024, nperseg=256, noverlap = 100, fs = 1000, norm=None)
            bi_spectrum = np.array(abs(bi_spectrum))  # calculate bi_spectrum
            bi_spectrum = bi_spectrum.reshape((256, 256, 1))
            bi_spectrum = 255 * (bi_spectrum - np.min(bi_spectrum)) / (np.max(bi_spectrum) - np.min(bi_spectrum))
            dataset = np.vstack((dataset, np.array([bi_spectrum])))  # concat the dataset
            index+=1
            print(class_nam,'num:',index)
        # remove the first one of the dataset, due to initialization
    dataset = np.delete(dataset, 0, 0)
    return dataset


import matplotlib.pyplot as plt

def plot_polycoherence(freq1, freq2, bicoh):
    df1 = freq1[1] - freq1[0]
    df2 = freq2[1] - freq2[0]
    freq1 = np.append(freq1, freq1[-1] + df1) - 0.5 * df1
    freq2 = np.append(freq2, freq2[-1] + df2) - 0.5 * df2
    plt.figure(figsize=(4,4),dpi=300)
    # fig, ax = plt.subplots()
    plt.pcolormesh(freq2, freq1, np.abs(bicoh),cmap=plt.cm.jet)
    plt.axis('off')
    plt.xticks([])
    plt.yticks([])
    plt.show()

    plt.figure(figsize=(4,4),dpi=300)
    ax = plt.subplot(1, 1, 1)
    plt.contour(freq2[:-1], freq1[:-1], np.abs(bicoh),10,linewidths=1,cmap=plt.cm.jet)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.xticks([])
    plt.yticks([])
    plt.show()


if __name__ =="__main__":
    file_folder = '../../project/databases/database_1000'
    class_name = ['N','AS','MS','MR','MVP']
    dataset = get_bi_spectrum(file_folder, class_name, 1)



