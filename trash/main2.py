import imp
from pathlib import Path
import os
import json
from scipy import interpolate

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange

import numpy as np
import matplotlib.pyplot as plt
import math


def Lagrange(arr_x, arr_y, _x):
    l = [0 for j in range(len(arr_x))]
    result = 0
    for i in range(0, len(arr_x)):
        denominator = 1
        molecular = 1
        for j in range(0, len(arr_x)):
            if i != j:
                denominator = denominator * (arr_x[i] - arr_x[j])
                molecular = molecular * (_x - arr_x[j])
        l[i] = molecular / denominator
        result = result + l[i] * arr_y[i]
    return result


def norm_list(list_):
    list_ = np.array(list_)
    min_ = min(list_)
    max_ = max(list_)
    return ((list_ - min_) / (max_ - min_)).tolist()

choose_f = '2880'
choose_p = 36
choose_v = 1

in_dir = './data/input'
gt_dir = './data/gt'
in_files = os.listdir(in_dir)

for in_file in in_files:
    file = in_file[6:10]

    if file != choose_f:
        continue

    gt_file = 'GBM0MGXRAP_2021' + file + '000_01D_05M_ORB.SP3'

    with open(in_dir + '/' + in_file, 'r') as f:
        lines_in = f.readlines()

    with open(gt_dir + '/' + gt_file, 'r') as f:
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
            if file == choose_f and p == choose_p:
                y = float(value[choose_v])
                x = h * 3600 + m * 60 + s
                Xgt.append(x)
                Ygt.append(y)
    print('Xgt len:{}, min:{}, max:{}'.format(len(Xgt), min(Xgt), max(Xgt)))
    print('Ygt len:{}, min:{}, max:{}'.format(len(Ygt), min(Ygt), max(Ygt)))
    # print(Xgt)
    # print(Ygt)
    # print()
    plt.subplot(2, 2, 1)
    plt.title('file' + str(choose_f) + '_PC' + str(choose_p) + '_V' + str(choose_v))
    plt.plot(Xgt, Ygt, color='green', label='GT')
    plt.legend()
    plt.xlabel('time')
    plt.ylabel('position')
    # plt.show()

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
            if file == choose_f and p == choose_p:
                y = float(value[choose_v])
                x = h * 3600 + m * 60 + s
                Xin.append(x)
                Yin.append(y)
    print('Xin len:{}, min:{}, max:{}'.format(len(Xin), min(Xin), max(Xin)))
    print('Yin len:{}, min:{}, max:{}'.format(len(Yin), min(Yin), max(Yin)))
    # print(Xin)
    # print(Yin)
    # print()
    plt.subplot(2, 2, 2)
    plt.title('file' + str(choose_f) + '_PC' + str(choose_p) + '_V' + str(choose_v))
    plt.plot(Xin, Yin, color='red', label='input')
    plt.legend()
    plt.xlabel('time')
    plt.ylabel('position')
    # plt.show()

    ############################
    # f = interpolate.interp1d(Xin, Yin, kind="cubic")
    # f = lagrange(Xin, Yin)
    Xin2 = [i for i in range(3600 * 24)]
    # Yin2 = f(Xin2)

    ############################
    Yin2 = []
    for i in range(len(Xin2)):
        Yin2.append(Lagrange(Xin, Yin, Xin2[i]))

    ############################
    Xin3 = []
    Yin3 = []
    assert len(Xin2) == len(Yin2)
    for idx, x in enumerate(Xin2):
        if x in Xgt:
            Xin3.append(x)
            Yin3.append(Yin2[idx])
    assert Xin3 == Xgt
    assert len(Yin3) == len(Ygt)
    print('Xin3 len:{}, min:{}, max:{}'.format(len(Xin3), min(Xin3), max(Xin3)))
    print('Yin3 len:{}, min:{}, max:{}'.format(len(Yin3), min(Yin3), max(Yin3)))

    plt.subplot(2, 2, 3)
    plt.title('file' + str(choose_f) + '_PC' + str(choose_p) + '_V' + str(choose_v))
    plt.plot(Xin3, Yin3, color='blue', label='interp')
    plt.legend()
    plt.xlabel('time')
    plt.ylabel('position')
    # plt.show()

    ############################
    plt.subplot(2, 2, 4)
    plt.title('file' + str(choose_f) + '_PC' + str(choose_p) + '_V' + str(choose_v))
    plt.plot(Xgt, Ygt, color='green', label='GT')
    plt.plot(Xin3, Yin3, color='blue', label='interp')
    plt.legend()
    plt.xlabel('time')
    plt.ylabel('position')
    plt.show()
