#!/usr/bin/env python
# _*_coding:utf-8_*_
# @Time : 2024.06.30
# @Author : Rui-Si Hu
# @Email : grishu0707@gmail.com
# @IDE : PyCharm
# @File: features.py

from src.BERT_embedding import BERT_Embed
from src.BiLSTM_embedding import BiLSTM_Embed
from src.DPC import get_DPC
from src.DDE import get_DDE
import pandas as pd
import numpy as np

def select_features(allfeatures,feature_index):
    new_features = []
    orignal_data = pd.DataFrame(allfeatures)
    for i in list(feature_index):
        new_features.append(orignal_data[int(i)])
    features = np.array(new_features).T
    return features

def get_feature(fastas):
    encoding = []
    feature_index = pd.read_csv(r"feature_index.csv", header=None)

    DDE_features = get_DDE(fastas)
    new_DDE_feature = select_features(DDE_features, feature_index.iloc[0, :200])
    encoding.append(new_DDE_feature)

    BiLSTM_features = BiLSTM_Embed(fastas)
    new_BiLSTM_features = select_features(BiLSTM_features, feature_index.iloc[1, :200].values)
    encoding.append(new_BiLSTM_features)

    DPC_features = get_DPC(fastas)
    new_DPC_feature = select_features(DPC_features, feature_index.iloc[2, :200].values)
    encoding.append(new_DPC_feature)

    BERT_features = BERT_Embed(fastas)
    new_BERT_features = select_features(BERT_features, feature_index.iloc[3, :200].values)
    encoding.append(new_BERT_features)

    encoding = np.column_stack(encoding)
    new_encoding = select_features(encoding, feature_index.iloc[4, :27].values)

    return new_encoding

