import imp
from pathlib import Path
import os

in_dir = './data/input'
gt_dir = './data/gt'

in_files = os.listdir(in_dir)
gt_files = os.listdir(gt_dir)

PCs = ['PC' + str(i) for i in range(19,47)]

# print(PCs)

# data = {'date':[], 'h':[], 'm':[], 's':[], 'i':[], 'PC':[]}

one_curve = {'day':None, 'PC':None, 'v':None, 'data':[]}


for in_file in in_files:
    id = in_file[6:10]
    gt_file = 'GBM0MGXRAP_2021' + id + '000_01D_05M_ORB.SP3'

    in_info = []

    h, m, s = 0, 0, 0
    v1, v2, v3 = 0, 0, 0


    with open(in_dir + '/' + in_file, 'r') as f:
        lines = f.readlines()

        for line in lines:
            
            

            if '*  ' in line and '/*' not in line:
                tmp = line.split(' ')
                date = []
                for t in tmp:
                    if t is not '' and t is not '*':
                        date.append(t)
                    if len(date) == 5:
                        break

                # print(date)

                h, m, s = date[3], date[4], 0

            for PC in PCs:

                if PC in line:

                    tmp = line.split(' ')
                    value = []
                    for t in tmp:
                        if t is not '':
                            value.append(t)
                        if len(value) == 4:
                            break
                    
                    v1, v2, v3 = value[0], value[1], value[2]


            # print(value)
                    info = [h, m, s]
                # in_info.append(date)

    # gt_info = []

    # with open(gt_dir + '/' + gt_file, 'r') as f:
    #     lines = f.readlines()

    #     for line in lines:
            
    #         if '*  ' in line and '/*' not in line:
    #             tmp = line.split(' ')
    #             date = []
    #             for t in tmp:
    #                 if t is not '' and t is not '*':
    #                     date.append(t)
    #                 if len(date) == 5:
    #                     break

    #             gt_info.append(date)

                # print(date)

    # print(len(in_info), len(gt_info))

    # print()

    break


#############################

# h, m, s = 0, 0, 0

# for i in range(3600*24):
    
#     if s >= 60:
#         s = 0
#         m = m + 1
    
#     if m >= 60:
#         m = 0
#         h = h + 1
    
#     assert h <= 24

#     print(h, m, s)

#     s = s + 1