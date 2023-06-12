import UsrIntel.R1
import glob
import pandas as pd
import numpy as np
import os
import xlsxwriter as xl
import datetime
import sys
from datetime import timedelta

def directories_as_array (work_week_path,day_path):
    return glob.glob ("/**_SG_Runs/SGDFT_Runs_"+work_week_path+"/"+day_path+"/*_"+work_week_path+"/runs/*/*/*/reports/sgdft.rpt")

def check_which_rules (rule): #check which rule we need to sum and return the name of the rules
    if 'RULE_CAT_1' in rule:
        return 'RULE_CAT_1'

    if 'RULE_CAT_2' in rule:
        return 'RULE_CAT_2'

    if 'RULE_CAT_3' in rule:
        return 'RULE_CAT_3'

    if 'RULE_CAT_4' in rule:
        return 'RULE_CAT_4'

    if 'RULE_CAT_5' in rule:
        return 'RULE_CAT_5'

    if 'RULE_CAT_6' in rule:
        return 'RULE_CAT_6'

    if 'RULE_CAT_7' in rule:
        return 'RULE_CAT_7'

    if 'RULE_CAT_8' in rule:
        return 'RULE_CAT_8'

    if 'RULE_CAT_9' in rule:
        return 'RULE_CAT_9'

    if 'RULE_CAT_10' in rule:
        return 'RULE_CAT_10'

    if 'RULE_CAT_11' in rule:
        return 'RULE_CAT_11'

    if 'RULE_CAT_12' in rule:
        return 'RULE_CAT_12'

    if 'RULE_CAT_13' in rule:
        return 'RULE_CAT_13'

    if 'RULE_CAT_14' in rule:
        return 'RULE_CAT_14'

    if 'RULE_CAT_15' in rule:
        return 'RULE_CAT_15'

def strip_partition_name(directory_path):
    start="/**_Automations/**_SG_Runs/SGDFT_Runs_"+work_week_path+'/'
    end="_"+work_week_path
    return directory_path[directory_path.find(start)+len(start):directory_path.rfind(end)]

def stripping_syn_area(matrix):                                                                                         #function that will take a matrix and strip it so in [1] place will be the syn area
    j=0
    mat_length=len(matrix)
    while j<mat_length:
        if 'syn_genus' not in matrix[j][1] and 'apr_fc' not in matrix[j][1] and 'apr_innovus' not in matrix[j][1] and 'genus_dft' not in matrix[j][1]:
            #print (matrix[j][0]+" doesnt have the right adresss for collaterals files so it won't run SGDFT")
            matrix=np.delete(matrix,(j),axis=0)
            mat_length-=1
            j-=1
        j+=1
    for i in range(len(matrix)):                                                                                        #changing all the partition names into lower char and the netlist path to the Syn_area path
        if 'syn_genus' in matrix[i][1]:
            matrix[i][1]=matrix[i][1].partition('/syn_genus/')[0]+'/syn_genus/'
        elif 'apr_fc' in matrix[i][1]:
            matrix[i][1]=matrix[i][1].partition('/apr_fc/')[0]+'/apr_fc/'
        elif 'apr_innovus' in matrix[i][1]:
            matrix[i][1]=matrix[i][1].partition('/apr_innovus/')[0]+'/apr_innovus/'
        elif 'genus_dft' in matrix[i][1]:
            matrix[i][1]=matrix[i][1].partition('/genus_dft/')[0]+'/genus_dft/'
        matrix[i][0]=matrix[i][0].lower()
    return matrix

def stripping_cheetah_version(matrix):
    cheetah_version_col=[0]*len(matrix)
    for j in range (len(matrix)):
        cheetah_version_col[j]=matrix[j][1]
        if 'sc:' not in cheetah_version_col[j]:
            cheetah_version_col[j]=cheetah_version_col[j].partition('/runs/')[0]+'/sd.reopen'
            try:
                f = open(cheetah_version_col[j], "r")
                matrix[j][2]=f.read()
                matrix[j][2]=matrix[j][2].partition('-proj ')[2]
                matrix[j][2]=matrix[j][2].partition(' -cfg')[0]
            except FileNotFoundError:
                matrix[j][2]='*cheetah_version*'
        else:
            matrix[j][2]='*cheetah_version*'

rules_names=['*list_of_rules_named*']
directories=[]
day_path=str(datetime.date.today() - timedelta(days=0))

day_path=str(datetime.date.today())

work_week_path=os.popen("workweek|**").read()
work_week_path=work_week_path.strip()

directories=directories_as_array(work_week_path,day_path)            #set the directory in array while getting the current ww folder

all_dict_array=[]                               #array that will hold the rules for each partition
partitions_names=[]                              #array that will hold the partitions_names
for directory in directories:
    rules_sums={'RULE_CAT_1': 0, 'RULE_CAT_2': 0, 'RULE_CAT_3': 0, 'RULE_CAT_4': 0, 'RULE_CAT_5': 0, 'RULE_CAT_6': 0, 'RULE_CAT_7': 0, 'RULE_CAT_8': 0,'RULE_CAT_9': 0, 'RULE_CAT_10': 0, 'RULE_CAT_11': 0, 'RULE_CAT_12': 0, 'RULE_CAT_13': 0, 'RULE_CAT_14': 0, 'RULE_CAT_14': 0}
    with open(directory, 'r') as f:             #open sthe specifed file
        for line in f.readlines():              #runs onQ all the lines
            for rule in rules_names:            #runs on all the rules
                if rule in line:                #checks if a certain rule is in the line
                    if check_which_rules(rule)!='RULE_CAT_15':                          #for Rule_cat_15 rule the int is in different place
                        rules_sums[check_which_rules(rule)]+=int(line.split()[-2])      #add to the dictionary the number of violations
                    else:
                        rules_sums['RULE_CAT_15']+=int(line.split()[2])
    all_dict_array.append(rules_sums)
    partitions_names.append(strip_partition_name(directory))
    f.close()


##creating the excel file of the violations

df_excel=pd.DataFrame.from_dict(all_dict_array)
df_excel.index=partitions_names
df_excel.loc['Total',:]= df_excel.sum(axis=0)
df_excel.loc[:,'Total per Partition'] = df_excel.sum(axis=1)

excel_name='Latest_indicators_SGDFT.xlsx'
df_excel.to_excel(excel_name, index_label="Partition name")


##Creating file that will contain the netlists used in the latest run in order to send it as mail

df=pd.read_excel('/**_SGDFT_Automation/ATPG_Status.xlsx', usecols="D,E,F,G,H", skiprows=range(12,100))                                                                 #taking from the excel only the partitions names and netlists paths
matrix=df.as_matrix()                                                                                                 #matrix will hold the partition name in [0] and netlist path in [1]
matrix=stripping_syn_area(matrix)
stripping_cheetah_version(matrix)
f_netlist = open('/**_SGDFT_Automation/text_netlists.txt', "w")
for j in range(len(matrix)):
    f_netlist.write(matrix[j][0]+": "+matrix[j][4]+"\n")

f_netlist.write("\nSummary of the excel file (total violations per partition):\n")
f_netlist.writelines(str(df_excel['Total per Partition']))
f_netlist.write("\n\nAll the runs are saved in the following work area (IDC) and ready for you for debug if needed: \n/**_SG_Runs/SGDFT_Runs_"+work_week_path+"/"+day_path)

f_netlist.write("\n\nThanks\nYoav Yarden")
f_netlist.close()

