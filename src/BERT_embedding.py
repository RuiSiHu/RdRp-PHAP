#!/usr/bin/env python
# _*_coding:utf-8_*_
# @Time : 2024.06.30
# @Author : Rui-Si Hu
# @Email : grishu0707@gmail.com
# @IDE : PyCharm
# @File: BERT_embedding.py


from __future__ import print_function, division
import sys
import os
sys.path.append(os.pardir)
sys.path.append(os.path.join(os.pardir, os.pardir))
import time
from rich.progress import track
import numpy as np
import pandas as pd
import torch
import warnings
warnings.filterwarnings('ignore')
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
from tape import ProteinBertModel, TAPETokenizer


def BERT_Embed(fastaFile):
    TAPEEMB_ = []
    model = ProteinBertModel.from_pretrained('bert-base')
    model = model.to(DEVICE)
    tokenizer = TAPETokenizer(vocab='iupac')

    for sequence in track(fastaFile, "Computing: "):
        with torch.no_grad():
            token_ids = torch.tensor([tokenizer.encode(sequence)])
            token_ids = token_ids.to(DEVICE)
            output = model(token_ids)
            bert_output = output[0]
            bert_output = torch.squeeze(bert_output)
            bert_output = bert_output.mean(0)
            bert_output = bert_output.cpu().numpy()
            TAPEEMB_.append(bert_output.tolist())

    bert_feature = pd.DataFrame(TAPEEMB_)
    return bert_feature

