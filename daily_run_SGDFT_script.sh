#!/bin/tcsh

python /**_SGDFT_Automation/Python_SGDFT_Script.py
python /**_SGDFT_Automation/remove_runs_week_ago.py #if we change the run time (now - after 00:00, be advised to change this line as well)
