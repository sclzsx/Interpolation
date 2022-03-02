import imp
from pathlib import Path
import os
import json

choose_f = '2780'
choose_p = 19
choose_v = 0


def encode_data():
    in_dir = './data/input'
    gt_dir = './data/gt'

    in_files = os.listdir(in_dir)

    in_data = []
    gt_data = []

    files = [] 

    for in_file in in_files:
        file = in_file[6:10]
        gt_file = 'GBM0MGXRAP_2021' + file + '000_01D_05M_ORB.SP3'

        files.append(file)

        # data = {'file':None, 'PC':None, 'v':None, 'GT':None, 'h':None, 'm':None, 's':None, 'n':None}

        # one_curve = {'file':None, 'PC':None, 'v':None, 'Yin':[], 'Ygt':[]}

        with open(in_dir + '/' + in_file, 'r') as f:
            lines_in = f.readlines()

        with open(gt_dir + '/' + gt_file, 'r') as f:
            lines_gt = f.readlines()

        h, m, s = '0', '0', '0'

        for line in lines_in:

        
            if '*  ' in line and '/*' not in line:
                tmp = line.split(' ')
                # print(tmp)
                date = []
                for t in tmp:
                    if t is not '' and t is not '*':
                        t = t.replace('\n', '')
                        date.append(t)
                    if len(date) == 6:
                        break
                # print(date)
                h, m, s = date[3], date[4], date[5][:2]

            if 'PC' in line and '*' not in line:
                tmp = line.split(' ')
                # print(tmp)
                p = None
                value = []
                for t in tmp:
                    # print()
                    if 'PC' in t:
                        p = t[2:]
                    if t is not '' and 'PC' not in t:
                        value.append(t)
                    if len(value) == 3:
                        break

                for i in range(3):
                    tt = dict()
                    tt.setdefault('file', file)
                    tt.setdefault('PC', int(p))
                    tt.setdefault('v', i)
                    tt.setdefault('GT', 0)
                    tt.setdefault('h', int(h))
                    tt.setdefault('m', int(m))
                    tt.setdefault('s', int(s))
                    tt.setdefault('n', value[i])

                    ## 用这种思路来做!
                    # if tt['PC'] == 19 and tt['n'] is not '0.000000':
                    #     print(tt)

                    in_data.append(tt)

        #############################

        h, m, s = '0', '0', '0'

        for line in lines_gt:

            

            if '*  ' in line and '/*' not in line:
                tmp = line.split(' ')
                date = []
                for t in tmp:
                    if t is not '' and t is not '*':
                        date.append(t)
                    if len(date) == 5:
                        break

                h, m, s = date[3], date[4], '0'

            if 'PC' in line and '*' not in line:
                tmp = line.split(' ')
                # print(tmp)
                p = None
                value = []
                for t in tmp:
                    if 'PC' in t:
                        p = t[2:]

                    if t is not '' and 'PC' not in t:
                        value.append(t)
                    if len(value) == 4:
                        break

                for i in range(3):
                    tt = dict()
                    tt.setdefault('file', file)
                    # print(p)
                    tt.setdefault('PC', int(p))
                    tt.setdefault('v', i)
                    tt.setdefault('GT', 1)
                    tt.setdefault('h', int(h))
                    tt.setdefault('m', int(m))
                    tt.setdefault('s', int(s))
                    tt.setdefault('n', value[i])

                    # print(tt)
                    gt_data.append(tt)



    # print(len(in_data))
    # with open('in_data.json', 'w') as f:
    #     json.dump(in_data, f, indent=2)

    # print(len(gt_data))
    # with open('gt_data.json', 'w') as f:
    #     json.dump(gt_data, f, indent=2)

    return in_data, gt_data, files


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

#################################

if __name__ == '__main__':

    in_data, gt_data, files = encode_data()

    # with open('in_data.json', 'r') as f:
    #     in_data = json.load(f)
    # with open('gt_data.json', 'r') as f:
    #     gt_data = json.load(f)
    
    print(len(in_data), len(gt_data))

    # PCs = ['PC' + str(i) for i in range(19,47)]
    # print(PCs)

    # data = {'date':[], 'h':[], 'm':[], 's':[], 'i':[], 'PC':[]}

    # one_curve = {'file':None, 'PC':None, 'v':None, 'X':[], 'Yin':[], 'Ygt':[]}

    # X = [i for i in range(3600 * 24)]

    # for file in files:
    #     for p in range(19, 47):
    #         for v in range(3):
                
    #             Y_in = []

    #             h, m, s = 0, 0, 0

    #             for t in range(3600*24):
                    
    #                 if s >= 60:
    #                     s = 0
    #                     m = m + 1
                    
    #                 if m >= 60:
    #                     m = 0
    #                     h = h + 1
                    
    #                 assert h <= 24

    #                 # print(h, m, s)

    #                 # n = [i['n'] for i in in_data if i['file'] == file and i['PC'] == p and i['v'] == v and i['h'] == h and i['m'] == m and i['s'] == s]
    #                 # if len(n) > 0:
    #                 #     print(len(n))
                    
    #                 for i in in_data:

    #                     if i['file'] == file and i['PC'] == p and i['v'] == v and i['h'] == h and i['m'] == m and i['s'] == s:
    #                         print(i)

    #                     # if i['file'] == file:
    #                     #     print(i)





    #                 s = s + 1
                
    #             break
            
    #         break
        
    #     break
