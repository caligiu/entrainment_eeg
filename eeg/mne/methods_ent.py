import mne 
import ent


# takes channel AF4 of subject 3 and 
# check for different PSD calculation

sj = 3
epo = mne.read_epochs(f'S{sj:02}-epo.fif')

af4= epo.copy().pick(['AF4'])

w = af4["type=='cop'"].average().compute_psd(method='welch', fmin=0, fmax=10)
#w.plot()

tmin = 0.0
tmax = 18.2
fmin = 0.5
fmax = 6.0
sfreq = af4.info["sfreq"]
w1 = epo["type=='mix'"].average().compute_psd(
    "welch",
    n_fft=int(sfreq * (tmax - tmin)),
    n_overlap=0,
    n_per_seg=None,
    tmin=tmin,
    tmax=tmax,
    fmin=fmin,
    fmax=fmax,
    window="boxcar",
    verbose=False,    
)
#w1.plot()
w1.plot(dB=False)

# compute ssr 
# see https://mne.tools/dev/auto_tutorials/time-freq/50_ssvep.html#sphx-glr-auto-tutorials-time-freq-50-ssvep-py


tmin = 0.0
tmax = 18.2
fmin = 0.2
fmax = 6.0
sfreq = af4.info["sfreq"]

spectrum = af4["type=='mix'"].compute_psd(
    "welch",
    n_fft=int(sfreq * (tmax - tmin)),
    n_overlap=0,
    n_per_seg=None,
    tmin=tmin,
    tmax=tmax,
    fmin=fmin,
    fmax=fmax,
    window="boxcar",
    verbose=False,
)

psds, freqs = spectrum.get_data(return_freqs=True)
snrs = ent.snr_spectrum(psds, noise_n_neighbor_freqs=4, noise_skip_neighbor_freqs=2)

import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(2, 1, sharex="all", sharey="none", figsize=(8, 5))

freq_range = range(
    np.where(freqs >0.5 )[0][0], np.where(freqs >5.0)[0][0]
)

psds_plot = 10 * np.log10(psds)
psds_mean = psds_plot.mean(axis=(0, 1))[freq_range]
psds_std = psds_plot.std(axis=(0, 1))[freq_range]
axes[0].plot(freqs[freq_range], psds_mean, color="b")
axes[0].fill_between(
    freqs[freq_range], psds_mean - psds_std, psds_mean + psds_std, color="b", alpha=0.2
)
axes[0].set(title="PSD spectrum", ylabel="Power Spectral Density [dB]")

# SNR spectrum
snr_mean = snrs.mean(axis=(0, 1))[freq_range]
snr_std = snrs.std(axis=(0, 1))[freq_range]

axes[1].plot(freqs[freq_range], snr_mean, color="r")
axes[1].fill_between(
    freqs[freq_range], snr_mean - snr_std, snr_mean + snr_std, color="r", alpha=0.2
)
axes[1].set(
    title="SNR spectrum",
    xlabel="Frequency [Hz]",
    ylabel="SNR",
    ylim=[-2, 30],
    xlim=[fmin, fmax],
)
fig.show()
