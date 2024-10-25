import ent

sj = 2
# load subject 2 and give a look
e = ent.get_epo(ent.get_raw(sj))
e.plot() 
# marked bad:
#            epoch 452
#            channels Cz

# compute ica and exclude blinks
i = ent.get_ica(e)
i.plot_components()
i.exclude = [1]


# reconstruct epochs from ica, average ref, low pass
re = e.copy()
i.apply(re)
re.set_eeg_reference(ref_channels="average")
re.filter(l_freq=None, h_freq=80) 

# give a look, interpolate bad channels and save
re.plot()
# re.info['bads']
# Cz, FC2
re.interpolate_bads()

re.save(f'S{sj:02}-epo.fif')
