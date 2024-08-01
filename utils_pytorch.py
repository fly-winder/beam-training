import torch
import torch.nn as nn
import scipy.io as sio
import math

# Global Parameters
Nt = 256  # the number of antennas
P = 1   # the normalized transmit power


# Functions
def trans_Vrf(temp):
    # 网络输出的波束赋形矩阵（角度）
    # 根据欧拉公式将其转化为复数形式
    v_real = torch.cos(temp * math.pi)
    v_imag = torch.sin(temp * math.pi)
    vrf = torch.complex(v_real, v_imag)
    return vrf



def Rate_func(h, v, SNR_input):
    # h:最佳csi
    # v：波束赋形
    # SNR_input：噪声
    v = trans_Vrf(v)

    h = h.unsqueeze(1)
    v = v.unsqueeze(2)
    # 矩阵乘法
    hv = torch.bmm(h.to(torch.complex64), v)
    hv = hv.squeeze(dim=-1)
    rate = torch.log2(1 + SNR_input / Nt * torch.pow(torch.abs(hv), 2))
    return -rate


# load the saved .mat files generated by Matlab.
def mat_load(path):
    print('loading data...')
    # load the perfect csi(10,1,40)
    h = sio.loadmat(path + '/pcsi.mat')['pcsi']
    # load the estimated csi(10,1,64)
    h_est = sio.loadmat(path + '/ecsi.mat')['ecsi']
    print('loading complete')
    print('The shape of CSI is: ', h_est.shape)
    return h, h_est