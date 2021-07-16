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
            try:
                os.mkdir(file_shuchu)
            except:
                jishu_2=0
                #print('except')
            
            copy('OptOmegaIPEA.pl',file_shuchu)
            
            file_optw = open('tuningw/'+str(file_all[i])+'/OptOmegaIPEA.pl','r')
            lines=[]
            for line in file_optw:
                if '$jobid="oligomer";' in line:
                    lines.append('$jobid="tuningw'+str(file_all[i])+'";\n')
                else:
                    lines.append(line)
            file_optw.close()
            
            file_new= open('tuningw/'+str(file_all[i])+'/OptOmegaIPEA.pl','w')
            for i in range(0,len(lines)):
                file_new.write(lines[i])
            file_new.close()
            


            atom_num = 0

            for q in mol_geo:
                if len(q) >0:
                    #print(q.strip(' ').split(' ')[2:])
                    atom_num+=1


            qchem_xyz = open(file_shuchu+'/structure.xyz','w')
            qchem_xyz.write(str(atom_num))
            qchem_xyz.write('\n\n')
            for q in mol_geo:
                if len(q) >0:
                    for print_line in q.strip(' ').split(' ')[2:]:
                        qchem_xyz.write(print_line)
                        qchem_xyz.write(' ')
                    qchem_xyz.write('\n')
            qchem_xyz.close()


            qchemIN_N =  open(file_shuchu+'/N.in','w')
            qchemIN_N.write('$molecule\n'+'0 1\n')
            for q in mol_geo:
                if len(q) >0:
                    for print_line in q.strip(' ').split(' ')[2:]:
                        qchemIN_N.write(print_line)
                        qchemIN_N.write(' ')
                    qchemIN_N.write('\n')
            qchemIN_N.write('$end\n$rem\njobtype sp\nexchange general\nomega '+str(w_intial)+'\nlrc_dft true\nbasis 6-31g*\nscf_final_print 1\nscf_convergence 7\nscf_guess read\ngen_scfman false\n$end\n$xc_functional\nX wPBE 1.0\nC PBE 1.0\n$end\n')
            qchemIN_N.close()

            qchemIN_M =  open(file_shuchu+'/M.in','w')
            qchemIN_M.write('$molecule\n'+'-1 2\n')
            for q in mol_geo:
                if len(q) >0:
                    for print_line in q.strip(' ').split(' ')[2:]:
                        qchemIN_M.write(print_line)
                        qchemIN_M.write(' ')
                    qchemIN_M.write('\n')
            qchemIN_M.write('$end\n$rem\njobtype sp\nexchange general\nomega '+str(w_intial)+'\nlrc_dft true\nbasis 6-31g*\nscf_final_print 1\nscf_convergence 7\nscf_guess read\ngen_scfman false\n$end\n$xc_functional\nX wPBE 1.0\nC PBE 1.0\n$end\n')
            qchemIN_M.close()

            qchemIN_P =  open(file_shuchu+'/P.in','w')
            qchemIN_P.write('$molecule\n'+'1 2\n')
            for q in mol_geo:
                if len(q) >0:
                    for print_line in q.strip(' ').split(' ')[2:]:
                        qchemIN_P.write(print_line)
                        qchemIN_P.write(' ')
                    qchemIN_P.write('\n')
            qchemIN_P.write('$end\n$rem\njobtype sp\nexchange general\nomega '+str(w_intial)+'\nlrc_dft true\nbasis 6-31g*\nscf_final_print 1\nscf_convergence 7\nscf_guess read\ngen_scfman false\n$end\n$xc_functional\nX wPBE 1.0\nC PBE 1.0\n$end\n')
            qchemIN_P.close()
        elif jishu_2==1:
            print(file_all[i],'need continue')
        elif jishu_2==10:
            print(file_all[i],'error!')
        elif jishu_2==11:
            print(file_all[i],'error!')





            
