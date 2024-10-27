import mne
import ent


## 
##  single subject
##

sj = 2
epo = mne.read_epochs(f'S{sj:02}-epo.fif')

# display single trial psd:
#cop = epo["type=='cop'"].plot_psd()

# psd on ERP

# parameters for multitapering
bw = 0.1
fm = 0.05
fM = 6

spect=dict()
spect["cop"] = epo["type=='cop'"].average().compute_psd(method='multitaper', bandwidth=bw, fmin=fm, fmax=fM)
spect["mix"] = epo["type=='mix'"].average().compute_psd(method='multitaper', bandwidth=bw, fmin=fm, fmax=fM)
spect["ccop"] = epo["type=='ctr_cop'"].average().compute_psd(method='multitaper', bandwidth=bw,fmin=fm, fmax=fM)
spect["cmix"] = epo["type=='ctr_mix'"].average().compute_psd(method='multitaper', bandwidth=bw,fmin=fm, fmax=fM)

spect["all"] = epo.average().compute_psd(method='multitaper', bandwidth=bw,fmin=fm, fmax=fM)

#topoplot
# 
# spect["mix"].plot_topo()

# single channel condition comparisons
# ent.plotCh(spect,'CP5').show()
# ent.plotCh(spect,'PO7').show()

# all channels in a pdf...
# 
from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages(f'Subject{sj}_Spectra.pdf')
for ch in epo.ch_names:
    f = ent.plotCh(spect,ch)
    pp.savefig(f)

pp.close()


#compute ssr  (not working ...)

spectrum = epo.compute_psd(method='multitaper', bandwidth=0.1,fmin=0.1, fmax=6)
psds, freqs = spectrum.get_data(return_freqs=True)
snrs = ent.snr_spectrum(psds, noise_n_neighbor_freqs=3, noise_skip_neighbor_freqs=1)