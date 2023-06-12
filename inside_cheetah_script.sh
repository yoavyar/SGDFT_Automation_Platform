#!/bin/tcsh

source **
setenv PATH **/${PATH}
setenv NB_SIGKILL_TIMEOUT 720
**/spgdft_collaterals.pl $1 $2 $3 $4                #Perl script $1 - partition name, $2 - syn area,  $3 - Compiler,  $4 - Netlist path  

#cat /**/waivers_folder/waivers/block_waiver.$block.swl >> $ward/runs/$block/$tech/sgdft_netlist_drc/scripts/block_waiver.swl  ##for manual waivers
#cat /**/waivers_folder/vars/vars.$block.tcl >> $ward/runs/$block/$tech/sgdft_netlist_drc/scripts/vars.tcl				    	##for manual waivers
#cat /**/dft_data/dft_data.$block.tcl >> $ward/runs/$block/$tech/sgdft_netlist_drc/scripts/dft_data.tcl							##for manual waivers

$SGDFT_HOME/full_flow.csh $1                                                             #Running SGDFT
