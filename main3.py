import imp
from pathlib import Path
import os
import json
from scipy import interpolate
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange

import numpy as np
import matplotlib.pyplot as plt
import math
import xlwt

def get_rms(records):
    return math.sqrt(sum([x ** 2 for x in records]) / len(records))

def run_single_curve(choose_f, choose_p, choose_v, method="cubic"):
    save_tag = str(choose_f) + '_PC' + str(choose_p) + '_V' + str(choose_v)
    save_dir = './' + method + '/'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    in_dir = './data/input/'
    gt_dir = './data/gt/'
    in_file = 'b2bppp' + choose_f + '.sp3'
    gt_file = 'GBM0MGXRAP_2021' + choose_f + '000_01D_05M_ORB.SP3'
    with open(in_dir + in_file, 'r') as f:
        lines_in = f.readlines()
    with open(gt_dir + gt_file, 'r') as f:
        lines_gt = f.readlines()

    #############################
    Xgt = []
    Ygt = []
    h, m, s = 0, 0, 0
    for line in lines_gt:
        if '*  ' in line and '/*' not in line:
            tmp = line.split(' ')
            date = []
            for t in tmp:
                if t is not '' and t is not '*':
                    date.append(t)
                if len(date) == 5:
                    break
            h, m, s = int(date[3]), int(date[4]), 0
        if 'PC' in line and '*' not in line:
            tmp = line.split(' ')
            p = 16
            value = []
            for t in tmp:
                if 'PC' in t:
                    p = int(t[2:])
                if t is not '' and 'PC' not in t:
                    value.append(t)
                if len(value) == 4:
                    break
            if p == choose_p:
                y = float(value[choose_v])
                x = h * 3600 + m * 60 + s
                if x not in Xgt and y != 0:
                    Xgt.append(x)
                    Ygt.append(y)
    for k in range(len(Xgt) - 1):
        if not Xgt[k] < Xgt[k+1]:
            print('Xin Error', Xgt[k], Xgt[k+1])

    #############################
    Xin = []
    Yin = []
    h, m, s = 0, 0, 0
    for line in lines_in:
        if '*  ' in line and '/*' not in line:
            tmp = line.split(' ')
            date = []
            for t in tmp:
                if t is not '' and t is not '*':
                    t = t.replace('\n', '')
                    date.append(t)
                if len(date) == 6:
                    break
            h, m, s = int(date[3]), int(date[4]), int(date[5][:2])
        if 'PC' in line and '*' not in line:
            tmp = line.split(' ')
            p = 16
            value = []
            for t in tmp:
                if 'PC' in t:
                    p = int(t[2:])
                if t is not '' and 'PC' not in t:
                    value.append(t)
                if len(value) == 3:
                    break
            if p == choose_p:
                y = float(value[choose_v])
                x = h * 3600 + m * 60 + s
                if x not in Xin and y != 0:
                    Xin.append(x)
                    Yin.append(y)
    for k in range(len(Xin) - 1):
        if not Xin[k] < Xin[k+1]:
            print('Xin Error', Xin[k], Xin[k+1])

    # 一方面,原本Xgt范围远大于Xin,有无用区间,所以对Xgt在Xin附近截取;
    # 另一方面,Xgt应该在Xin范围内,才能做插值,尤其边界部分不会出错,所以向内取整
    Xin_max, Xin_min = max(Xin), min(Xin)
    Xgt_max = int((Xin_max // 300) * 300) # 向内取整,为5分钟即300秒的整数倍
    Xgt_min = int((Xin_min // 300 + 1) * 300) # 向外取整,为5分钟即300秒的整数倍
    assert Xgt_max in Xgt and Xgt_min in Xgt
    idx_min = Xgt.index(Xgt_min)
    idx_max = Xgt.index(Xgt_max)
    Xgt = Xgt[idx_min:idx_max + 1]
    Ygt = Ygt[idx_min:idx_max + 1]

    ############################
    f = interpolate.interp1d(Xin, Yin, kind=method)
    Yout = f(Xgt)
    Ydiff = np.array(Yout) - np.array(Ygt)
    Ydiff = Ydiff * 1000 * 100
    rms = get_rms(Ydiff)

    if rms > 1000:
        print('PASS! Some unexpected errors happen to File{} PC{} V{}'.format(choose_f, choose_p, choose_v))
        return -1

    print(save_tag,'RMS:', rms)

    ############################
    fig = plt.figure(figsize=(10, 6))
    plt.subplot(2, 2, 1)
    plt.plot(Xin, Yin, color='red', label='input')
    plt.legend(loc=0,ncol=1)
    plt.subplot(2, 2, 2)
    plt.plot(Xgt, Ygt, color='green', label='gt')
    plt.legend(loc=0,ncol=1)
    plt.subplot(2, 2, 3)
    plt.plot(Xgt, Yout, color='blue', label='interp')
    plt.legend(loc=0,ncol=1)
    plt.subplot(2, 2, 4)
    plt.plot(Xgt, Ydiff, color='red', label='diff')
    plt.legend(loc=0,ncol=1)
    plt.savefig(save_dir + save_tag + '.png')
    plt.cla()

    ############################
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('sheet', cell_overwrite_ok=False)
    sheet.write(0, 0, 'Xin')
    sheet.write(0, 1, 'Yin')
    sheet.write(0, 2, 'Xgt')
    sheet.write(0, 3, 'Ygt')
    sheet.write(0, 4, 'Yout')
    sheet.write(0, 5, 'Ydiff')
    for i in range(len(Xin)):
        sheet.write(i+1, 0, Xin[i])
        sheet.write(i+1, 1, Yin[i])
    for i in range(len(Xgt)):
        sheet.write(i+1, 2, Xgt[i])
        sheet.write(i+1, 3, Ygt[i])
        sheet.write(i+1, 4, Yout[i])
        sheet.write(i+1, 5, Ydiff[i])

    book.save(save_dir + save_tag + '.xls')

    return rms

if __name__ == '__main__':
    files = [str(2780 + i*10) for i in range(0, 15)]
    PCs = [i for i in range(19,47)]
    Vs = [i for i in range(3)]

    RMSs = []
    for f in files:
        RMS_PCs = []
        for p in PCs:
            RMS_Vs = []
            for v in Vs:
                
                try:
                    rms = run_single_curve(f, p, v)
                except:
                    print('PASS! Some unexpected errors happen to File{} PC{} V{}'.format(f, p, v))

    #             RMS_Vs.append(rms)
    #         RMS_PCs.append(RMS_Vs)
    #     RMSs.append(RMS_PCs)
    # RMSs = np.array(RMSs)
    # print(RMSs.shape)


