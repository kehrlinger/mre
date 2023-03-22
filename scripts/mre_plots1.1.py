#!/usr/bin/env python3
import argparse
import matplotlib.pyplot as plt
import time

def make_hist():
    pass

def main():
    """
    Accepts a tab delimited input file as argument which contains:
    sample_name GOI length,length,
    HG00096	ASB1    2437,2437,
    This file is produced by the mre_stats.py script. See this file for further explanation.
    Additionally, a file (ancestries.txt) containing sample_id with corresponding ancestries is accepted as a second argument:
    HG00096	GBR
    HG00098	GBR
    The output of this script are histogram plots showing the length distribution of reads within a single ancestry at a single GOI.
    """
    parser = argparse.ArgumentParser(description="input_file ancestry_table")
    parser.add_argument("input_file", type=str)
    parser.add_argument("ancestry_table", type=str)
    args = parser.parse_args()
    input_file = args.input_file
    ancestry_table = args.ancestry_table
    ancestry_table_content = []
    gene_to_length = {}
    sample_to_gene_to_length = {}
    ancestry_to_gene_to_length = {}
    ancestry_group_to_gene_to_length = {}

    with open(ancestry_table, "r") as fh_input_ancestry:
        for sample_group_ancestry in fh_input_ancestry:
            sample, group_ancestry = sample_group_ancestry.strip().split()
            group, ancestry = group_ancestry.split("_")
            ancestry_table_content.append([sample, group, ancestry])
        fh_input_ancestry.close()

    with open(input_file, "r") as fh_input:
        for sample_gene_lengths in fh_input:
            if len(sample_gene_lengths.split()) != 3:
                continue
            else:
                sample, gene, lengths = sample_gene_lengths.split()
                lengths = [ int(x) for x in lengths.split(",") ]

            for sample_group_ancestry_list in ancestry_table_content:
                sample_placeholder, group, ancestry = sample_group_ancestry_list
                if sample in sample_group_ancestry_list:
                    if sample not in sample_to_gene_to_length:
                        sample_to_gene_to_length[sample] = {}
                    sample_to_gene_to_length[sample] = {gene: lengths}
                    #print(sample_to_gene_to_length)

                    if gene not in gene_to_length:
                        gene_to_length[gene] = lengths
                    gene_to_length[gene].extend(lengths)
                    #print(gene_to_length)

                    if ancestry not in ancestry_to_gene_to_length:
                        ancestry_to_gene_to_length[ancestry] = {}
                    if gene not in ancestry_to_gene_to_length[ancestry]:
                        ancestry_to_gene_to_length[ancestry][gene] = lengths
                    ancestry_to_gene_to_length[ancestry][gene].extend(lengths)
                    #print(ancestry_to_gene_to_length)

                    if group not in ancestry_group_to_gene_to_length:
                        ancestry_group_to_gene_to_length[group] = {}
                    if gene not in ancestry_group_to_gene_to_length[group]:
                        ancestry_group_to_gene_to_length[group][gene] = lengths
                    ancestry_group_to_gene_to_length[group][gene].extend(lengths)
                    #print(ancestry_group_to_gene_to_length)


    # Make necessary subfolders for all the different plot groups needed
    # Construct timestamps
    # Plot
    for ancestry_group, gene_len_dict in ancestry_group_to_gene_to_length.items():
        for gene, lengths in gene_len_dict.items():
            timestamp = time.strftime("%Y%m%d", time.localtime())
            if gene == "FOCAD1":
                plt.hist(lengths, bins=50, range=[1000, 6000])
                plt.savefig("/plots/{fgroup}/{ftime}_{fgroup}_{fgene}.png".format(fgroup=ancestry_group, fgene=gene, ftime=timestamp))
                plt.close()

if __name__ == '__main__':
    main()