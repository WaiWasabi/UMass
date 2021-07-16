#!/bin/bash
#BSUB -J DSSC4 #Job name
#BSUB -q long #Computing queue to submit your job to, including long, long, interactive, parallel, and GPC
#BSUB -W 168:00 #Time limit
#BSUB -n 12 #Number of cores in total
#BSUB -R span[hosts=1] #Number of nodes where we want the cores to belong. Usually it is 1.
#BSUB -R rusage[mem=4000] #Memory required by each core
#BSUB -oo DSSC4.log #Log file
#BSUB -eo DSSC4.err #Error file

export NL=/nl/uma_zhou_lin/packages/Q-Chem_5.3/development #Q-Chem source codes in the nearline directory.
export QCROOT=/home/zl53a/Q-Chem_5.3 #Root directory for Q-Chem in my home directory.
export QC=$QCROOT/development #If you prefer the commercial version please set export QC=$QCROOT/commercial
export QCSRC=$NL #Q-Chem source files
export QCAUX=$QC/qcaux #Q-Chem auxiliary files
export QCBIN=$QC/bin #Q-Chem binary files
export QCHEM=$QCBIN/qchem #Q-Chem running script shell
export QCSCRATCH=/tmp/$USER #Local scratch folder under your username, located on the computing node.
export MYSCRATCH=/home/$USER/scratch #Global scratch folder in your home directory. This is subject to change.
unset QCLOCALSCR #Make sure this is unset. Q-Chem has a bug there.
export JOBID=DSSC4 #Job ID. This is subject to change.

#If the environemntal varaibles are not specified.
if [ -e $QCBIN/qchem.setup.sh ]
then
  $QCBIN/qchem.setup.sh
fi

#If the local scratch folder does not exist
if [ ! -e $QCSCRATCH ]
then
  mkdir $QCSCRATCH
fi

#If the global scratch folder does not exist
if [ ! -e $MYSCRATCH ]
then
  mkdir $MYSCRATCH
fi

$QCHEM -save -nt 12 $JOBID.in $JOBID.out $JOBID #Run Q-Chem over x (subject to change) core and save the scratch files. $JOBID.in $JOBID.out $JOBID represents the input file, output file, and the scratch folder name. They are all subject to change.
rm -rf $QCSCRATCH/$JOBID/ #Delete the scratch folder from the computing node. This is optional.
