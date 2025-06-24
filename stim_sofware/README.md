This repository contains a Python script built with PsychoPy to run a cognitive psychology experiment on the recognition of two-syllable words embedded within sequences of syllables.

# Experiment Overview
Participants are shown sequences of individual syllables. After each block, they are asked whether a specific two-syllable target word was presented during that sequence.

The experiment records:

- The syllables shown

- Participant responses (Yes/No)

- Response correctness

- Reaction times (RT)

- Precise timestamps for each syllable

The experiment supports EEG synchronization through parallel port triggers.

# Key Features
- Precise timing for stimulus presentation

- Trigger signals sent via parallel port (default: 0x4FF8)

- Counterbalanced response key mapping

- Full-screen, mouse-hidden interface

- Windows notifications disabled during the task for improved focus

- Automatic logging of trial data

# Requirements
- Windows operating system

- Python 3.x

- PsychoPy

- Parallel port (for trigger support)

- Screen resolution: 1920×1080 (recommended)

# File Structure
├── blocks/

│   ├── b*.csv           # Experimental blocks

│   ├── p*.csv           # Practice blocks

│   ├── listA.txt        # Experimental block sequence for group A

│   ├── listB.txt        # For group B

│   ├── listC.txt        # For group C

│   ├── listD.txt        # For group D

│   └── pract.txt        # Practice block sequence

├── logs/

│   └── sjXXX.csv        # Participant data log (auto-generated)

├── main_experiment.py   # Main PsychoPy script

└── README.md            # This file

# How to Run

Launch the experiment:

python main_experiment.py

When prompted, enter the participant number using the number keys and press Enter.

The experiment will:

- Show practice blocks listed in pract.txt

Then show experimental blocks listed in one of listA.txt, listB.txt, listC.txt, or listD.txt, depending on the participant number:

- participant_id % 4 == 0 → listD.txt

- participant_id % 4 == 1 → listA.txt

- participant_id % 4 == 2 → listB.txt

- participant_id % 4 == 3 → listC.txt

# Key mapping is counterbalanced:

Even participant IDs: M = YES, Z = NO

Odd participant IDs: Z = YES, M = NO

Participants press the spacebar to continue to the next block.

At the end, a completion message is shown and a log file is saved to the logs/ folder.

# Logged Data
Each row in the log CSV contains:

- timestamp: when the syllable was presented

- syllable: the syllable shown

- wp: word part metadata

- type: type of stimulus (target/distractor)

- order: position in the sequence

- block: block number

- target: two-syllable target queried after block

- correct: whether the response was correct

- RT: reaction time in ms

# Technical Notes
The parallel port address is set to 0x4FF8 by default. Change it in the script if needed.

Windows notifications are disabled at the start using PowerShell and re-enabled at the end.
