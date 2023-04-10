#!/usr/bin/env python3

import argparse
import os

def main():
    pass
    input_file_path = "/groups/bi-marvl/klaus/mre/output/stats/a_results.txt"
    # input_file_path = "/home/ehrlinger/code/mre/test_data/a_results.txt"
    gene_to_sample_to_length = {}
    with open(input_file_path, "r") as fh_input:
        for line in fh_input:
            if len(line.split()) < 3:
                continue
            sample, gene, length_string = line.strip().split()
            lengths = [int(x) for x in length_string.split(",")]
            for i in lengths:
                if i < 2000:
                    lengths.remove(i)
                if i > 6000:
                    lengths.remove(i)
            try:
                length_average = int(sum(lengths) / len(lengths))
            except:
                continue
            print(gene, length_average, sample, len(lengths), lengths)
            if gene not in gene_to_sample_to_length:
                gene_to_sample_to_length[gene] = {}
            gene_to_sample_to_length[gene] = {sample: length_average}
    """ 
    for gene, s2l in gene_to_sample_to_length.items():
        for s, l in s2l.items():
            print(l, s)
    """
    

if __name__ == "__main__":
    main()