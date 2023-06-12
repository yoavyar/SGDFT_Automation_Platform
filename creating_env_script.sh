#!/bin/tcsh

cd /**_Runs/																									

setenv partition $1
setenv date `exact_path`																															
cd /**_Runs/SGDFT_Runs_$date																						
setenv SYN_AREA $2              #set SYN_AREA as env variable that will be used in the inside_cheetah_script

setenv COMPILER $4
setenv NETLIST_PATH $5

setenv day $6
mkdir $6
cd /**_Runs/SGDFT_Runs_$date/$6																						

/**/cth_psetup -proj $3 -cfg ** -ward . -x '$SETUP_R2G -w ${partition}_${date}_** -b ${partition} -force ;  /**_SGDFT_Automation/inside_cheetah_script.sh $partition $SYN_AREA $COMPILER $NETLIST_PATH ' 

