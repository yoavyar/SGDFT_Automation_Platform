import UsrIntel.R1
import glob
import pandas as pd
import os
import xlsxwriter as xl
import datetime
import shutil
from datetime import timedelta

work_week_path=os.popen("workweek| **").read()
work_week_path=work_week_path.strip()
if work_week_path[-2:].isdigit(): # check if the last two characters are digits
    new_number = str(int(work_week_path[-2:]) - 1).zfill(2) # increment the number and pad with leading zeroes if necessary
    new_work_week = work_week_path[:-2] + new_number # concatenate the original string (excluding the last two digits) with the new number
else:
    new_work_wwek = work_week_path

day_path=str(datetime.date.today() - timedelta(days=7))

shutil.rmtree('/**_SG_Runs/SGDFT_Runs_'+new_work_week+'/'+day_path)
