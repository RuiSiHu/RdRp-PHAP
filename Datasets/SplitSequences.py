#!/usr/bin/env python
# _*_coding:utf-8_*_
# @Time : 2024.06.18
# @Author : Rui-Si Hu
# @Email : grishu0707@gmail.com
# @IDE : PyCharm
# @File : RdRp_PHAP.py

import argparse
import random
from Bio import SeqIO

def split_sequences(input_file, mode):
    records = list(SeqIO.parse(input_file, "fasta"))

    num_sequences = len(records)
    num_80_percent = int(num_sequences * 0.8)

    random.shuffle(records)

    selected_80_percent = records[:num_80_percent]
    remaining_20_percent = records[num_80_percent:]

    for i, record in enumerate(selected_80_percent, start=1):
        record.id = f"Seq{i}|{mode}"
        record.description = ""

    output_file_80_percent = input_file.split(".")[0] + f"_selected_80_percent_{mode}.fasta"
    SeqIO.write(selected_80_percent, output_file_80_percent, "fasta")

    for i, record in enumerate(remaining_20_percent, start=1):
        record.id = f"Seq{i}|{mode}"
        record.description = ""

    output_file_20_percent = input_file.split(".")[0] + f"_remaining_20_percent_{mode}.fasta"
    SeqIO.write(remaining_20_percent, output_file_20_percent, "fasta")

def main():
    parser = argparse.ArgumentParser(description='Split sequences from a FASTA file into 80% and 20%')
    parser.add_argument('-i', '--input', type=str, help='Input FASTA file', required=True)
    parser.add_argument('-m', '--mode', type=int, help='Mode: 0 or 1', choices=[0, 1], default=0)

    args = parser.parse_args()
    split_sequences(args.input, args.mode)

if __name__ == "__main__":
    main()
