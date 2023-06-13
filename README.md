For the implementation I’ve used the following method, in the following order:
1.	Excel file that includes the following information for each partition:
		I.	Partition Name
		II.	Synthesis area
		III.	Compiler used for synthesis
		IV.	Latest Netlist path


2.	Python scripts of two kinds (from which the user can choose one):
		I.	‘Python_SGDFT_Script.py’ – that takes all the partition in the excel file and create SGDFT runs for them in a central location
		II.	‘Manually_Python_SGDFT_Scripy.py’ – that gets as input one partition name and create SGDFT run only for him.
	Both types are collecting all the data into matrix, creating the first variables needed for cheetah, and allocating remote machines according to the number of partitions mentioned in the excel.
	After allocating the remote machines, a log file is being created in order to show all the actions that are being done inside the remote machine until it finishes.
	In addition, the script can be configured to find the cheetah version of each partition if needed or to a certain cheetah version.
	From this point on, the scripts are working in parallel, meaning each remote machine that was allocated to a certain partition will run independently.

3.	Shell script named ‘creating_env_script.sh’, that takes the data that was sent from the python script, organizing it, entering the central area that will include all the results, and then entering the Cheetah environment.

4.	Shell script named ‘inside_cheetah_script.sh’, that working inside Cheetah environment and do the follows:
		I.	Running Perl script that creating all the collaterals files, depending on the input that were taken from the excel file (partition name, synthesis area, compiler, netlist).
		II.	Modifying the waivers files if needed
		III.	Sending the SGDFT run 

5.	While the runs are in progress, the user can use Python script named ‘which_partitions_finished.py’ that reads all the log files created in stage 2 and prints the status of each partition: “Succeeded runs”, “Failed runs” and 	“Ongoing runs”.

6.	After all the SGDFT runs are finished, they can be seen in a central area that includes all the results, the central area is changing each day to make the script run in a daily basis. 

7.	Python script named ‘excel_file_once_a_day.py’ that collecting all the reports from the central area and generating an excel file that shows the status of each partition – number of violations per set of rules (after 	categorizing), the total number of violations per partition, the total number of violations per set of rules and the total number of violations for all the partitions combined.

8.	Synopsys GUI used from the central area to debug each partition.


9.	Python script and Shell scripts named ‘remove_runs_week_ago.py, ‘daily_run_excel_and_mail.sh’ and ‘daily_run_SGDFT_script.sh’ that are using for the daily management, to remove old runs that are no longer relevant and create the 	summarized violation excel.
	Those script are meant to create full automation – using them with Cron (which is a command in Linux) will make no need of human interface in order to get the results automatically and daily.


by using the given excel file (as example - given in the name 'ATPG_Status.xlsx', and running the command 'Python Python_SGDFT_Script.py' all the process will run automatily
