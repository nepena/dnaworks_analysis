#Contributor
Noah Peña, PhD

#Description
A simply python script for using dnaworks 

#Set-up 

Download and install dnaworks (https://github.com/davidhoover/DNAWorks)

Make dnaworks accessible to your PATH 

Script should now run when called. 


#To make runnable on 

nano ~/.bashrc

#COPY AND PASTE to bottom of /.bashrc

alias run_dnawork_analysis='python3 /path/to/generate_dnaworks_input.py' 

#SAVE 
#restart terminal 

source ~/.bashrc 

cd /path/to/directory 

generate_dnaworks_input 

