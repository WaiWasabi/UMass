import os

import os
path = r'optimize/'
file_all = []
for filename in os.listdir(path):
    file_all.append(os.path.join(filename))

for i in range(0,len(file_all)):
    
    jobname = str(file_all[i])
    
    scripts_out='optimize/'+str(file_all[i]) + '/bsub.sh'
    
    jiaoben = open(scripts_out, 'w')
    jiaoben.write('#!/bin/bash\n#BSUB -J '+str(jobname) + ' #Job name')
    jiaoben.write('\n#BSUB -q long #Computing queue to submit your job to, including long, long, interactive, parallel, and GPC')
    jiaoben.write('\n#BSUB -W 168:00 #Time limit')
    jiaoben.write('\n#BSUB -n 12 #Number of cores in total')
    jiaoben.write('\n#BSUB -R span[hosts=1] #Number of nodes where we want the cores to belong. Usually it is 1.')
    jiaoben.write('\n#BSUB -R rusage[mem=4000] #Memory required by each core')
    jiaoben.write('\n#BSUB -oo '+str(jobname) + '.log #Log file')
    jiaoben.write('\n#BSUB -eo '+str(jobname) + '.err #Error file')
    jiaoben.write('\n\nexport NL=/nl/uma_zhou_lin/packages/Q-Chem_5.3/development #Q-Chem source codes in the nearline directory.')
    jiaoben.write('\nexport QCROOT=/home/zl53a/Q-Chem_5.3 #Root directory for Q-Chem in my home directory.')
    jiaoben.write('\nexport QC=$QCROOT/development #If you prefer the commercial version please set export QC=$QCROOT/commercial')
    jiaoben.write('\nexport QCSRC=$NL #Q-Chem source files')
    jiaoben.write('\nexport QCAUX=$QC/qcaux #Q-Chem auxiliary files')
    jiaoben.write('\nexport QCBIN=$QC/bin #Q-Chem binary files')
    jiaoben.write('\nexport QCHEM=$QCBIN/qchem #Q-Chem running script shell')
    jiaoben.write('\nexport QCSCRATCH=/tmp/$USER #Local scratch folder under your username, located on the computing node.')
    jiaoben.write('\nexport MYSCRATCH=/home/$USER/scratch #Global scratch folder in your home directory. This is subject to change.')
    jiaoben.write('\nunset QCLOCALSCR #Make sure this is unset. Q-Chem has a bug there.')
    jiaoben.write('\nexport JOBID='+str(jobname) + ' #Job ID. This is subject to change.')
    jiaoben.write('\n')
    jiaoben.write('\n')
    jiaoben.write('#If the environemntal varaibles are not specified.\n')
    jiaoben.write('if [ -e $QCBIN/qchem.setup.sh ]\n')
    jiaoben.write('then\n')
    jiaoben.write('  $QCBIN/qchem.setup.sh\n')
    jiaoben.write('fi\n')
    jiaoben.write('\n')
    jiaoben.write('#If the local scratch folder does not exist\n')
    jiaoben.write('if [ ! -e $QCSCRATCH ]\n')
    jiaoben.write('then\n')
    jiaoben.write('  mkdir $QCSCRATCH\n')
    jiaoben.write('fi\n')
    jiaoben.write('\n')
    jiaoben.write('#If the global scratch folder does not exist\n')
    jiaoben.write('if [ ! -e $MYSCRATCH ]\n')
    jiaoben.write('then\n')
    jiaoben.write('  mkdir $MYSCRATCH\n')
    jiaoben.write('fi\n')
    jiaoben.write('\n')
    jiaoben.write('$QCHEM -save -nt 12 $JOBID.in $JOBID.out $JOBID #Run Q-Chem over x (subject to change) core and save the scratch files. $JOBID.in $JOBID.out $JOBID represents the input file, output file, and the scratch folder name. They are all subject to change.\n')
    #jiaoben.write('cp -r $QCSCRATCH/$JOBID/ $MYSCRATCH/ #Copy the scratch file from the computing node to your home directory. This is optional.\n')
    jiaoben.write('rm -rf $QCSCRATCH/$JOBID/ #Delete the scratch folder from the computing node. This is optional.\n')

    jiaoben.close()
    
    
