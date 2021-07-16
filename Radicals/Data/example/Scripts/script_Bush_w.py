import os

core_num=8
path = r'tuningw/'
file_all = []
for filename in os.listdir(path):
    file_all.append(os.path.join(filename))

for i in range(0,len(file_all)):
    
    jobname = str(file_all[i])
    
    scripts_out='tuningw/'+str(file_all[i]) + '/bsub.sh'

    jiaoben = open(scripts_out, 'w')
    jiaoben.write('#!/bin/bash')
    jiaoben.write('\n#BSUB -J '+str(jobname))
    jiaoben.write('\n#BSUB -q long')
    jiaoben.write('\n#BSUB -W 48:00')
    jiaoben.write('\n#BSUB -n '+str(core_num))
    jiaoben.write('\n#BSUB -R span[hosts=1]')
    jiaoben.write('\n#BSUB -R rusage[mem=4000]')
    jiaoben.write('\n#BSUB -o '+str(jobname) + '.out')
    jiaoben.write('\n#BSUB -e '+str(jobname) + '.err')
    jiaoben.write('\n')
    jiaoben.write('\nexport NL=/nl/uma_zhou_lin/packages/Q-Chem_5.3/development')
    jiaoben.write('\nexport QCROOT=/home/zl53a/Q-Chem_5.3')
    jiaoben.write('\nexport QC=$QCROOT/development')
    jiaoben.write('\nexport QCSRC=$NL &&')
    jiaoben.write('\nexport QCAUX=$QC/qcaux &&')
    jiaoben.write('\nexport QCBIN=$QC/bin &&')
    jiaoben.write('\nexport QCHEM=$QCBIN/qchem &&')
    jiaoben.write('\nexport QCSCRATCH=/tmp/$USER &&')
    jiaoben.write('\n#export MYSCRATCH=$QCROOT/scratch')
    jiaoben.write('\nunset QCLOCALSCR')
    jiaoben.write('\n')
    jiaoben.write('\nif [ -e $QCBIN/qchem.setup.sh ]')
    jiaoben.write('\nthen')
    jiaoben.write('\n  $QCBIN/qchem.setup.sh')
    jiaoben.write('\nfi')
    jiaoben.write('\n')
    jiaoben.write('\nif [ ! -e $QCSCRATCH ]')
    jiaoben.write('\nthen')
    jiaoben.write('\n  mkdir $QCSCRATCH')
    jiaoben.write('\nfi')
    jiaoben.write('\n')
    jiaoben.write('\nexport JOBID='+str(jobname))
    jiaoben.write('\nexport PL=OptOmegaIPEA.pl')
    jiaoben.write('\nperl $PL')

    jiaoben.close()
