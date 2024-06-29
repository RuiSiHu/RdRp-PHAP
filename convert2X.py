#!/usr/bin/env python
# _*_coding:utf-8_*_
# @Time : 2024.06.30
# @Author : Rui-Si Hu
# @Email : grishu0707@gmail.com
# @IDE : PyCharm
# @file: convert2X.py

import argparse

def convert_non_amino_acids_to_X(input_file, output_file):
    valid_amino_acids = set("ACDEFGHIKLMNPQRSTVWY")

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith('>'):
                outfile.write(line)
            else:
                converted_line = ''.join([char if char in valid_amino_acids else 'N' for char in line.strip()])
                outfile.write(converted_line + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert non-amino acid characters in a FASTA file to 'X'.")
    parser.add_argument('input_file', type=str, help="Input FASTA file")
    parser.add_argument('output_file', type=str, help="Output FASTA file")
    
    args = parser.parse_args()
    convert_non_amino_acids_to_X(args.input_file, args.output_file)

