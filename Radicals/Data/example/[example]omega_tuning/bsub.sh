#!/bin/bash
#BSUB -J HOPV_155
#BSUB -q long
#BSUB -W 48:00
#BSUB -n 6
#BSUB -R span[hosts=1]
#BSUB -R rusage[mem=4000]
#BSUB -o HOPV_155.out
#BSUB -e HOPV_155.err

export NL=/nl/uma_zhou_lin/packages/Q-Chem_5.3/development
export QCROOT=/home/zl53a/Q-Chem_5.3
export QC=$QCROOT/development
export QCSRC=$NL &&
export QCAUX=$QC/qcaux &&
export QCBIN=$QC/bin &&
export QCHEM=$QCBIN/qchem &&
export QCSCRATCH=/tmp/$USER &&
#export MYSCRATCH=$QCROOT/scratch
unset QCLOCALSCR

if [ -e $QCBIN/qchem.setup.sh ]
then
  $QCBIN/qchem.setup.sh
fi

if [ ! -e $QCSCRATCH ]
then
  mkdir $QCSCRATCH
fi

export JOBID=HOPV_155
export PL=OptOmegaIPEA.pl
perl $PL