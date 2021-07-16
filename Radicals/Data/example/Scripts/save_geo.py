import os
from shutil import copy

import os
path = r'optimize/'
file_all = []
for filename in os.listdir(path):
    file_all.append(os.path.join(filename))

jishufu=0

for i in range(0,len(file_all)):
    if jishufu == 0:
        file_shuchu='tuningw/'+str(file_all[i])
        file = open('optimize/'+str(file_all[i])+'/'+str(file_all[i])+'.out')
        w_intial = 220
        
        mol_geo = []
        jishu_1=0
        jishu_2=0
        for line in file:
            if 'Q-Chem fatal error occurred' in line:
                jishu_2=10
            if 'Z-matrix Print:' in line:
                jishu_1+=1
            if jishu_1 ==2:
                mol_geo.append(line.strip('\n'))
            if 'OPTIMIZATION CONVERGED' in line:
                jishu_1+=1
            if jishu_1==1:
                if 'ATOM                X               Y               Z' in line:
                    jishu_1+=1
        file.close()

        if len(mol_geo)<1:
            jishu_2+=1

        if jishu_2 == 0:
    
            atom_num = 0

            for q in mol_geo:
                if len(q) >0:
                    #print(q.strip(' ').split(' ')[2:])
                    atom_num+=1

            qchem_xyz = open('structure/'+str(file_all[i])+'.xyz','w')
            qchem_xyz.write(str(atom_num))
            qchem_xyz.write('\n\n')
            for q in mol_geo:
                if len(q) >0:
                    for print_line in q.strip(' ').split(' ')[2:]:
                        qchem_xyz.write(print_line)
                        qchem_xyz.write(' ')
                    qchem_xyz.write('\n')
            qchem_xyz.close()

        elif jishu_2==1:
            print(file_all[i],'need continue')
        elif jishu_2==10:
            print(file_all[i],'error!')
        elif jishu_2==11:
            print(file_all[i],'error!')





            
