import os
import numpy as np
import pandas as pd

import mne
import matplotlib.pyplot as plt
from mne.preprocessing import ICA

def check_soa(sj, saveCsv = True):
    '''
    Checks SOA between stimulus marked as 1 (syllable onset)
    '''
    data_folder = '/home/vespa/mne_data/entrainment/'
    raw_file = os.path.join(data_folder, f"S{sj:03}.vhdr")
    raw = mne.io.read_raw_brainvision(raw_file, verbose='ERROR')
    events, event_dict = mne.events_from_annotations(raw, verbose='ERROR') 
    t = events[events[:,2]==1,0]
    delta_t = 2*(t[1:(t.size)]-t[0:(t.size-1)])
    if saveCsv:
        pd.DataFrame(delta_t).to_csv(f'S1_SOA_sj{sj:2}.csv', header=False, index=False)
    bins = np.array([0.0, 232.0, 235.0, 240.0, 250.0, 280.0, 400, np.inf])
    ind = np.digitize(delta_t,bins)
    for i in range(ind.min(), ind.max()+1):
        print(f'bin{i+1}: ]{bins[i-1]:4} :  {bins[i]:4}] {sum(ind==i):6}')


def get_raw(sj):
    data_folder = '/home/vespa/mne_data/entrainment/'
    raw_file = os.path.join(data_folder, f"S{sj:03}.vhdr")
    raw = mne.io.read_raw_brainvision(raw_file)
    raw.set_montage('easycap-M1') 
    return raw
    epochs = mne.Epochs(
        raw, 
        events, 
        tmin=-0.2, 
        tmax=18.2, 
        baseline=None, 
        detrend=1, 
        event_id = list(range(11, 51)), 
        preload=True
    )

def get_epo(raw):
    events, event_dict = mne.events_from_annotations(raw)
    epochs = mne.Epochs(
        raw, 
        events, 
        tmin=-0.2, 
        tmax=18.2, 
        baseline=None, 
        detrend=1, 
        event_id = list(range(11, 51)), 
        preload=True
    )
    d = pd.DataFrame(
        list(   
            epochs.events[:,2]),
            columns=["marker"], index=range(len(epochs)
            )
    )
    d['type'] = np.where( 
        d['marker'] > 40, 'ctr_mix',  
        np.where( 
            d['marker']>30, 'ctr_cop', 
            np.where(
                d['marker']>20, 'mix',
                'cop'
            )
        )
    )
    epochs.metadata = d
    return epochs 

def get_ica(epochs, lp=1.0, hp=None, ncomp=32):
    filt_epo = epochs.copy().filter(l_freq=lp, h_freq=hp)  # note mne doc says h_freq=None (but I think for saccades)
    ica = ICA(n_components=ncomp, max_iter="auto", random_state=97)
    ica.fit(filt_epo)
    return ica

def plotCh(spect, ch, vlines = [1000/(6*234), 1000/(3*234), 1000/234]):
    f,ax=plt.subplots()
    ax.set_yscale('log')
    d1 = spect['cop'].copy().pick(ch).get_data().transpose()
    d2 = spect['mix'].copy().pick(ch).get_data().transpose()
    d3 = spect['ccop'].copy().pick(ch).get_data().transpose()
    d4 = spect['cmix'].copy().pick(ch).get_data().transpose()
    ax.plot(spect['cop'].freqs, d1, color='black', label ='cop')
    ax.plot(spect['mix'].freqs, d2, color='green', label ='mix')
    ax.plot(spect['ccop'].freqs, d3, '--', linewidth=2, color='black', label ='ctrc')
    ax.plot(spect['cmix'].freqs, d4, '--', linewidth=2, color='green', label ='ctrm')
    ax.legend()
    ax.set_title(ch)
    ax.set_xlabel('Freq [Hz]')
    ax.set_ylabel('Power [AU]')
    for v in vlines:
        ax.axvline(v)
    
    return f


def snr_spectrum(psd, noise_n_neighbor_freqs=1, noise_skip_neighbor_freqs=1):
    """Compute SNR spectrum from PSD spectrum using convolution.

    Parameters
    ----------
    psd : ndarray, shape ([n_trials, n_channels,] n_frequency_bins)
        Data object containing PSD values. Works with arrays as produced by
        MNE's PSD functions or channel/trial subsets.
    noise_n_neighbor_freqs : int
        Number of neighboring frequencies used to compute noise level.
        increment by one to add one frequency bin ON BOTH SIDES
    noise_skip_neighbor_freqs : int
        set this >=1 if you want to exclude the immediately neighboring
        frequency bins in noise level calculation

    Returns
    -------
    snr : ndarray, shape ([n_trials, n_channels,] n_frequency_bins)
        Array containing SNR for all epochs, channels, frequency bins.
        NaN for frequencies on the edges, that do not have enough neighbors on
        one side to calculate SNR.
    """
    # Construct a kernel that calculates the mean of the neighboring
    # frequencies
    averaging_kernel = np.concatenate(
        (
            np.ones(noise_n_neighbor_freqs),
            np.zeros(2 * noise_skip_neighbor_freqs + 1),
            np.ones(noise_n_neighbor_freqs),
        )
    )
    averaging_kernel /= averaging_kernel.sum()

    # Calculate the mean of the neighboring frequencies by convolving with the
    # averaging kernel.
    mean_noise = np.apply_along_axis(
        lambda psd_: np.convolve(psd_, averaging_kernel, mode="valid"), axis=-1, arr=psd
    )

    # The mean is not defined on the edges so we will pad it with nas. The
    # padding needs to be done for the last dimension only so we set it to
    # (0, 0) for the other ones.
    edge_width = noise_n_neighbor_freqs + noise_skip_neighbor_freqs
    pad_width = [(0, 0)] * (mean_noise.ndim - 1) + [(edge_width, edge_width)]
    mean_noise = np.pad(mean_noise, pad_width=pad_width, constant_values=np.nan)

    return psd / mean_noise