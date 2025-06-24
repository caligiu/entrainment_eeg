import csv
import random
import time
from psychopy import visual, core, event
import psychopy.parallel as parallel # Module for parallel port communication

import subprocess
# Imposta il Focus Assist su 'Solo priorità' per ridurre le notifiche
subprocess.run(['powershell', '-Command', "powershell -ExecutionPolicy Bypass -Command \"&{Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings' -Name 'NOC_GLOBAL_SETTING_TOASTS_ENABLED' -Value 0}\""], shell=True)

# Function to get participant number
def get_participant_number():
    instruction_stim.text = "Please type your participant number and press Enter (or press 'Y' to exit):"
    instruction_stim.draw()
    win.flip()

    participant_id_keys = event.waitKeys(keyList=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'return', 'y'], clearEvents=False)

    participant_id = ''
    while 'return' not in participant_id_keys:
        for key in participant_id_keys:
            if key == 'y':
                core.quit()
            if key != 'return':
                participant_id += key
        instruction_stim.text = f"Please type your participant number and press Enter (or press 'Y' to exit):\n{participant_id}"
        instruction_stim.draw()
        win.flip()
        participant_id_keys = event.waitKeys(keyList=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'return', 'y'], clearEvents=False)

    return int(participant_id)

# Routine to show instructions
def show_instructions(participant_id):
    if participant_id % 2 == 0:
        instruction_text = (
            "Benvenut*!\n\n"
            "Presta attenzione a quello che vedrai sullo schermo. "
            "Alla fine di ogni blocco ti verrà chiesto se hai visto una specifica parola formata da due sillabe.\n\n"
            "Premi 'M' per SI e 'Z' per NO.\n\n"
            "Premi qualsiasi tasto per iniziare"
        )
    else:
        instruction_text = (
            "Benvenut*!\n\n"
            "Presta attenzione a quello che vedrai sullo schermo. "
            "Alla fine di ogni blocco ti verrà chiesto se hai visto una specifica parola formata da due sillabe.\n\n"
            "Premi 'Z' per SI e 'M' per NO.\n\n"
            "Premi qualsiasi tasto per iniziare"
        )
    instruction_stim.text = instruction_text
    instruction_stim.draw()
    win.flip()
    keys = event.waitKeys()
    if 'y' in keys:
        core.quit()

# Routine to pause
def show_pause():
    instruction_text = (
        "Premi la barra spaziatrice per il prossimo blocco"
    )
    instruction_stim.text = instruction_text
    instruction_stim.draw()
    win.flip()
    keys = event.waitKeys()
    if 'y' in keys:
        core.quit()

def getList(listname):
    fp = open(f'./blocks/{listname}.txt')
    line=fp.readlines()
    fp.close
    return line[0].split()

# Function to read syllables and trigger info from a CSV file
def read_syllables_from_csv(filename):
    syllables_info = []
    with open(filename, newline='', mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            syllables_info.append(row)
    return syllables_info

def show_block(block, seq):
    # Trigger before the first syllable of the group
    parallel.setData(int(block))  # Example trigger before the group
    core.wait(0.008)
    parallel.setData(0)
    core.wait(1)  # Wait for 1 second
    info = []
    
    t0 = time.time()
    for syllable_info in seq:
        syllable_stim.text = syllable_info.get('SYLL', 'N/A')
        syllable_stim.draw()
        # Wait for 225 milliseconds from t0 (13.5 frames at 60Hz from stimulus onset)
        core.wait(0.225-time.time()+t0)
        win.flip()
        t0 = time.time()
        syllable_info.update([('timestamp', time.time())])
        info.append(syllable_info)
        parallel.setData(1)
        core.wait(0.008)
        parallel.setData(0)
        # Wait for 125 milliseconds from t0 (7.5 frames at 60Hz from stimulus onset)
        core.wait(0.125-time.time()+t0)
        # starts blank
        win.flip()
        
    
    # Trigger after the last syllable of the group
    core.wait(1)  # Wait for 1 second
    parallel.setData(int(block)+100) 
    core.wait(0.008)
    parallel.setData(0)
    percent_complete = (progress / totalblocks) * 100
    target = syllable_info.get('TARGET', 'N/A')
    present = syllable_info.get('PRESENT', 'N/A')
    resp = show_task(target=target, isyes=present, progress=int(percent_complete), participant_id=participant_id)
    log_event(logfile, info, block, target, correct=resp[0], RT=resp[1])

# Routine to show the task after each group with feedback and progress
def show_task(target, isyes, progress, participant_id):
    # Counterbalanced keys for instructions
    if participant_id % 2 == 0:
        yes_key = 'm'
        no_key = 'z'
    else:
        yes_key = 'z'
        no_key = 'm'

    task_stim.text = f"Hai visto questa parola?\n\n{target}\n\nPremi '{yes_key.upper()}' per SI o '{no_key.upper()}' per NO"
    task_stim.draw()
    win.flip()
    start = time.time()
    keys = event.waitKeys(keyList=['m', 'z', 'y'])
    if 'y' in keys:
        core.quit()
    else:
        rt = time.time()-start
    
    # Determine if response was correct
    response = keys[0]
    correct = None
    if bool(int(isyes)) :
        correct = response == yes_key
    else:
        correct = response == no_key
    feedback_text = "Corretto!" if correct else "Sbagliato!"
    
    # Show feedback and progress
    feedback_stim.text = f"{feedback_text}\n\nProgress: {progress}% completato"  if progress>0 else f"{feedback_text}\n\n"
    feedback_stim.draw()
    win.flip()
    core.wait(3)  # show the feedback for 3 seconds
    return correct, rt

# Function to log events
def log_event(logfile, infos, block, target, correct=None, RT=None):
    fieldnames = ['timestamp', 'syllable', 'wp', 'type', 'order', 'block', 'target', 'correct', 'RT']
    for info in infos:
        row = {
            'timestamp': info.get('timestamp', 'N/A'),
            'syllable': info.get('SYLL', 'N/A'),
            'wp': info.get('WP', 'N/A'),
            'type': info.get('TYPE', 'N/A'),
            'order': info.get('ORDER', 'N/A'),
            'block': block,
            'target':target,
            'correct': correct,
            'RT': RT
        }
        with open(logfile, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(row)

# set parallel port address and set all bits to zero
parallel.setPortAddress(0x4FF8)
parallel.setData(0)
    
# Setup the window
win = visual.Window(size=[1920, 1080], color= [-0.7,-0.7,-0.7], fullscr=True, checkTiming=True, units='pix')  # Dark gray background
win.mouseVisible = False  # Hide mouse cursor

# Create text stimulus for syllables and instructions
syllable_stim = visual.TextStim(win, text='', color='white', height=50, anchorHoriz='left', alignText='left')  # Larger, more readable text
instruction_stim = visual.TextStim(win, text='', color='white', pos=(0, 0), height=30)  # Larger, readable text for instructions
feedback_stim = visual.TextStim(win, text='', color='white', pos=(0, -200), height=30)  # Larger, readable feedback text
task_stim = visual.TextStim(win, text='', color='white', pos=(0, -100), height=50)  # Task centered but lowered

# Avvia l'esperimento
participant_id = get_participant_number()

# Log file setup
logfile = f"logs/sj{participant_id:03d}.csv"

# Initialize log file
fieldnames = ['timestamp', 'syllable', 'wp', 'type', 'order', 'block', 'target', 'correct', 'RT']
with open(logfile, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

show_instructions(participant_id)

# Read practice list 

plist = getList('pract')
progress = 0
totalblocks = 40

for pb in plist:
    syllables = read_syllables_from_csv(f'./blocks/p{pb}.csv')
    show_pause()
    show_block(pb, syllables)

show_instructions(participant_id)

# Read exp list 

oo = ['D', 'A','B', 'C']

l = oo[participant_id % 4]

elist = getList(f'list{l}')

for eb in elist:
    progress = progress +1
    syllables = read_syllables_from_csv(f'./blocks/b{eb}.csv')
    show_pause()
    show_block(eb, syllables)

# End of experiment
instruction_stim.text = "L'esperimento è terminato. Grazie per la tua partecipazione!"
instruction_stim.draw()
win.flip()
event.waitKeys()
win.close()
core.quit()
subprocess.run(['powershell', '-Command', "powershell -ExecutionPolicy Bypass -Command \"&{Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings' -Name 'NOC_GLOBAL_SETTING_TOASTS_ENABLED' -Value 1}\""], shell=True)
