# Entrainment EEG Sentence Rhythm Perception

This repository contains documentation, scripts, and stimulus material related to an EEG experiment investigating neural entrainment to rhythmic sentence structures.

The project is structured into multiple components: experimental stimuli, EEG preprocessing (in both MNE-Python and EEGLAB), and documentation of references and computational techniques.

## Project Overview

The experiment aims to evaluate how the human brain synchronizes to structured vs randomized sentence rhythms. Stimuli consist of rhythmic blocks of syllables presented in different syntactic conditions, while EEG recordings and tapping data are analyzed to extract spectral and phase coherence features.

## Repository Structure

```
entrainment_eeg/
eeg/                  # EEG processing and documentation
 docs/             # Bibliography and analysis references
 mne/              # Python-based analysis (MNE 1.8.0)
stim_software/        # Sentence block generator and PsychoPy experiment
HSP_2025/             # Additional project-related material
README.md             # This file
```

## EEG Analysis

### eeg/docs/

A curated set of useful links and references for:

- Power spectrum estimation (EEGLAB, MNE, Welch method)
- Inter-trial phase coherence caveats
- Lock-in detection theory and simulators
- Notable research papers related to sentence processing and EEG entrainment

### eeg/mne/

Scripts and metadata for EEG preprocessing and analysis using MNE-Python 1.8.0.

- `ent.py`: utility functions
- `preproc_ent.py`: basic MNE pipeline (import, filtering, epoching)
- `psd_ent.py`: Power spectral density estimation
- `info.md`: details about dataset and marker types
- `S1_SOA.csv`: SOA data for syllable synchronization
- `Subject*.pdf`: example plots per subject and condition

Note: .fif EEG files and raw .dat recordings are hosted externally (Google Drive).

## Stimulus Presentation (stim_software)

This folder contains a PsychoPy-based experiment for assessing recognition of two-syllable targets in syllable streams.

### Overview

Participants are shown sequences of individual syllables. After each block, they are asked whether a specific two-syllable target word was presented during that sequence.

The experiment records:

- Presented syllables
- Participant responses (Yes/No)
- Response correctness
- Reaction times (RT)
- Timestamps per syllable

Supports EEG synchronization through parallel port triggers.

### Features

- Precise timing for stimulus presentation
- Trigger signals via parallel port (default: 0x4FF8)
- Counterbalanced response key mapping
- Full-screen display with mouse hidden
- Windows notifications disabled for task focus
- Automatic logging of trial data

### Requirements

- Windows OS
- Python 3.x
- PsychoPy
- Parallel port for EEG triggers
- Screen resolution: 1920Ã—1080 (recommended)

### File Structure

```
stim_software/
 blocks/
 listA.txt ... listD.txt     # Block orders per group
 pract.txt                   # Practice block order
 logs/
 sjXXX.csv                   # Participant data logs (auto-generated)
 main_experiment.py             # PsychoPy experiment script
 README.md                      # This description
```

### Running the Experiment

Run:

```bash
python main_experiment.py
```

When prompted, enter participant number. Block sequence is determined by:

- `ID % 4 == 0`: listD.txt
- `ID % 4 == 1`: listA.txt
- `ID % 4 == 2`: listB.txt
- `ID % 4 == 3`: listC.txt

Key mapping:

- Even IDs: M = YES, Z = NO
- Odd IDs: Z = YES, M = NO

Practice blocks always: 61, 91, 71, 81 (see pract.txt)

### Logged Output

Each log CSV includes:

- timestamp
- syllable
- wp (word position)
- type (stimulus type)
- order (syllable order)
- block (block ID)
- target (2-syllable word)
- correct (1/0)
- RT (reaction time in ms)

Parallel port triggers are sent to 0x4FF8 by default. You can edit this in the script.

## HSP_2025/

Placeholder for material related to the project contribution at the [Human Sentence Processing Conference, Washington, USA, 2025](https://hsp2025.github.io/)

## References

Key references for the methodology include:

- Ding et al. (2016, 2017)
- Buiatti et al. (2009, 2019)
- Kabdebon et al. (2015)
- Nozadaran et al. (2016, 2018)
- Van Diepen & Mazaheri (2018) on phase coherence
- Welch (1967) on FFT-based PSD
- Slepian (1978) on spectral concentration

See `eeg/docs/README.md` for full list and links.

## License

This project is licensed under the **GNU General Public License v3.0**.  
You are free to copy, modify, and distribute this software under the terms of the GPL.

For the full text of the license, see [LICENSE](https://www.gnu.org/licenses/gpl-3.0.en.html) or the LICENSE file included in this repository.

##  Credits

This work has been done at the Depatment of Devepomental Psychology and Socialization of the University of Padua. It part of the the research project REPLAI (Repetition Experiments as Probes on Linguistics Analysis and Integration) funded within the MIUR PRIN-2022 - 2022JT5N3J as a part of NextGenerationEU of the EU.

[<img src="logo/logodpss.png" height="80">](https://www.dpss.unipd.it/)
