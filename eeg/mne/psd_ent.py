import ent
import mne


## 
##  single subject
##

sj = 2 
epo = mne.read_epochs(f'S{sj:02}-epo.fif')
#cop = epo["type=='cop'"].plot_psd()

cop = epo["type=='cop'"].average().compute_psd(method='multitaper', bandwidth=0.1, fmin=0.1, fmax=6)
mix = epo["type=='mix'"].average().compute_psd(method='multitaper', bandwidth=0.1, fmin=0.1, fmax=6)
ccop = epo["type=='ctr_cop'"].average().compute_psd(method='multitaper', bandwidth=0.1,fmin=0.1, fmax=6)
cmix = epo["type=='ctr_mix'"].average().compute_psd(method='multitaper', bandwidth=0.1,fmin=0.1, fmax=6)
all = epo.average().compute_psd(method='welch', fmax=6)

all.plot_topo()
