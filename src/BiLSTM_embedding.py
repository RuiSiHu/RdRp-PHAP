#!/usr/bin/env python
# _*_coding:utf-8_*_
# @Time : 2024.06.30
# @Author : Rui-Si Hu
# @Email : grishu0707@gmail.com
# @IDE : PyCharm
# @File: BiLSTM_embedding.py

from __future__ import print_function,division
from rich.progress import track
import pandas as pd
import torch
import torch.nn as nn
from src.alphabets import Uniprot21
import warnings

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(DEVICE)
warnings.filterwarnings('ignore')

def unstack_lstm(lstm):
    device = next(iter(lstm.parameters())).device

    in_size = lstm.input_size
    hidden_dim = lstm.hidden_size
    layers = []
    for i in range(lstm.num_layers):
        layer = nn.LSTM(in_size, hidden_dim, batch_first=True, bidirectional=True)
        layer.to(device)

        attributes = ['weight_ih_l', 'weight_hh_l', 'bias_ih_l', 'bias_hh_l']
        for attr in attributes:
            dest = attr + '0'
            src = attr + str(i)
            getattr(layer, dest).data[:] = getattr(lstm, src)

            dest = attr + '0_reverse'
            src = attr + str(i) + '_reverse'
            getattr(layer, dest).data[:] = getattr(lstm, src)

        layer.flatten_parameters()
        layers.append(layer)
        in_size = 2*hidden_dim
    return layers

def embed_stack(x, lm_embed, lstm_stack, proj, include_lm=True, final_only=False):
    zs = []

    x_onehot = x.new(x.size(0),x.size(1), 21).float().zero_()
    x_onehot.scatter_(2,x.unsqueeze(2),1)
    zs.append(x_onehot)

    h = lm_embed(x)
    if include_lm and not final_only:
        zs.append(h)

    if lstm_stack is not None:
        for lstm in lstm_stack:
            h,_ = lstm(h)
            if not final_only:
                zs.append(h)
    if proj is not None:
        h = proj(h.squeeze(0)).unsqueeze(0)
        zs.append(h)

    z = torch.cat(zs, 2)
    return z


def embed_sequence(x, lm_embed, lstm_stack, proj, include_lm=True, final_only=False
                  ,  pool='none', use_cuda=False):

    if len(x) == 0:
        return None

    alphabet = Uniprot21()
    x = x.upper()
    # convert to alphabet index
    x = alphabet.encode(x)
    x = torch.from_numpy(x)
    if use_cuda:
        #x = x.cuda()
        x = x.to(DEVICE)

    # embed the sequence
    with torch.no_grad():
        x = x.long().unsqueeze(0)
        z = embed_stack(x, lm_embed, lstm_stack, proj
                       , include_lm=include_lm, final_only=final_only)
        # pool if needed
        z = z.squeeze(0)
        if pool == 'sum':
            z = z.sum(0)
        elif pool == 'max':
            z,_ = z.max(0)
        elif pool == 'avg':
            z = z.mean(0)
        z = z.cpu().numpy()

    return z


def load_model(path, use_cuda=False):

    encoder = torch.load(path)
    encoder.eval()
    if use_cuda:

        encoder=encoder.to(DEVICE)
    encoder = encoder.embedding

    lm_embed = encoder.embed
    lstm_stack = unstack_lstm(encoder.rnn)
    proj = encoder.proj

    return lm_embed, lstm_stack, proj


def BiLSTM_Embed(fastaFile):
    BiLSTMEMB_=[]
    lm_embed, lstm_stack, proj=load_model("./Models/BiLSTM_embed.model", use_cuda=True)
    proj = None
    for seq in track(fastaFile,"Computing: "):
        sequence = seq

        sequence = sequence.encode("utf-8")

        z = embed_sequence(sequence, lm_embed, lstm_stack, proj
                                  ,  final_only=False,include_lm = True
                                  , pool='avg', use_cuda=True)

        BiLSTMEMB_.append(z)
    bilstm_feature=pd.DataFrame(BiLSTMEMB_)

    return bilstm_feature














