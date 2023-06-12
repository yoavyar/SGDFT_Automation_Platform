import UsrIntel.R1
import glob
import pandas as pd
import numpy as np
import os
import requests
import xlrd
import datetime

def stripping_syn_area(matrix):                                                                                         #function that will take a matrix and strip it so in [1] place will be the syn area
    j=0
    mat_length=len(matrix)
    while j<mat_length:
        if 'syn_genus' not in matrix[j][1] and 'apr_fc' not in matrix[j][1] and 'apr_innovus' not in matrix[j][1] and 'genus_dft' not in matrix[j][1] and 'apr_cdns' not in matrix[j][1]:
            print (matrix[j][0]+" doesnt have the right adresss for collaterals files so it won't run SGDFT")
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
        elif 'apr_cdns' in matrix[i][1]:
            matrix[i][1]=matrix[i][1].partition('/apr_cdns/')[0]+'/apr_cdns/'
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
                    matrix[j][2]='cheetah_version'                                                                      #Censored
            else:
            matrix[j][2]='cheetah_version'                                                                              #Censored

os.environ["date"]=os.popen("workweek | exact_path").read()                                                             #Censored set the env needed for SG
os.chdir('exact_path')
os.system ('mkdir SGDFT_Runs_$date')                                                                                    #set the env needed for SG

day=datetime.date.today()

df=pd.read_excel('/**_SGDFT_Automation/ATPG_Status.xlsx', usecols="D,E,F,G,H", skiprows=range(14,100))                                                                 #taking from the excel only the partitions names and netlists paths
matrix=df.as_matrix()                                                                                                 #matrix will hold the partition name in [0] and netlist path in [1]
matrix=stripping_syn_area(matrix)
stripping_cheetah_version(matrix)
os.chdir('/**_SG_Runs/logs')

for i in range(len(matrix)):
    #first line - running with cheetah version of the synthesis area and the line below - latest cheetah version
    #os.system('nbjob run --target ** --qslot ** --class ** /**_SGDFT_Automation/creating_env_script.sh '+matrix[i][0]+' '+matrix[i][1]+' '+matrix[i][2]+' '+matrix[i][3]+' '+matrix[i][4]+' '+str(day)) #to run through netbatch
    os.system('nbjob run --target ** --qslot ** --class ** /**_SGDFT_Automation/creating_env_script.sh '+matrix[i][0]+' '+matrix[i][1]+' '+'cheetah_version'+' '+matrix[i][3]+' '+matrix[i][4]+' '+str(day)) #to run through netbatch
