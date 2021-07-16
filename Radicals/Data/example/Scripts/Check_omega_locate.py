from shutil import copy

import os
path = r'optimize/'
file_all = []
for filename in os.listdir(path):
    file_all.append(os.path.join(filename))

for i in range(0,len(file_all)):
    
    jobname = str(file_all[i])

    omega = []

    file_shuchu = 'tuningw/'+str(file_all[i])+'/'+str(file_all[i])+'.out'
    
    file_optw_shuchu = open(file_shuchu,'r')
    lines=[]
    for line in file_optw_shuchu:
        lines.append(line)
    file_optw_shuchu.close()
    try:
        jishu = 0
        for line_num in range(0,100):
            if 'gamma optimal:' in lines[len(lines)-line_num-1]:
                jishu = 1
                omega.append(lines[len(lines)-line_num-1].split(':')[-1])
        
        if jishu ==0:
            print(file_all[i],'fail')
        
        if jishu==1:
            print(file_all[i],omega[0].strip('\n'))
    except:
        print(file_all[i],'not finish')
