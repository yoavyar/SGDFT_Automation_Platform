#!/bin/tcsh

cd /**_SGDFT_Automation

python /**_SGDFT_Automation/excel_file_once_a_day.py

cat /**_SGDFT_Automation/text_for_mail.txt /**_SGDFT_Automation/text_netlists.txt | mail -s 'LNC-C0 SGDFT BE - Bi-weekly report' -a /**_SGDFT_Automation/Latest_indicators_SGDFT.xlsx yoav.yarden@intel.com
