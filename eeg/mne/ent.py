import os
import numpy as np
import pandas as pd

import mne
import matplotlib.pyplot as plt
from mne.preprocessing import ICA

def get_raw(sj):
    data_folder = '/home/vespa/mne_data/entrainment/'
    raw_file = os.path.join(data_folder, f"S{sj:03}.vhdr")
    raw = mne.io.read_raw_brainvision(raw_file)
    raw.set_montage('easycap-M1') 
    return raw

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
