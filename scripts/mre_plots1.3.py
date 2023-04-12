#!/usr/bin/env python3
import argparse
import os
import time
import matplotlib.pyplot as plt
import random

def make_hist():
    pass

def set_plot_fonts():
    SMALL_SIZE = 8
    MEDIUM_SIZE = 10
    BIGGER_SIZE = 12

    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

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
    workdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ancestry_table_content = []
    gene_to_length = {}
    ancestry_to_gene_to_length = {}
    ancestry_group_to_gene_to_length = {}
    print(workdir)

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
                lengths = [ int(x) for x in lengths.split(",") ] # not needed?
                if len(lengths) > 15:
                    lengths = random.sample(lengths, 15)

            for sample_group_ancestry_list in ancestry_table_content:
                sample_placeholder, group, ancestry = sample_group_ancestry_list
                group_plus_ancestry = group + "_" + ancestry
                if sample in sample_group_ancestry_list:
                    if gene not in gene_to_length:
                        gene_to_length[gene] = []
                    gene_to_length[gene].extend(lengths)
                    #print(gene_to_length)

                    if group_plus_ancestry not in ancestry_to_gene_to_length:
                        ancestry_to_gene_to_length[group_plus_ancestry] = {}
                    if gene not in ancestry_to_gene_to_length[group_plus_ancestry]:
                        ancestry_to_gene_to_length[group_plus_ancestry][gene] = []
                    ancestry_to_gene_to_length[group_plus_ancestry][gene].extend(lengths)
                    #print(ancestry_to_gene_to_length)

                    if group not in ancestry_group_to_gene_to_length:
                        ancestry_group_to_gene_to_length[group] = {}
                    if gene not in ancestry_group_to_gene_to_length[group]:
                        ancestry_group_to_gene_to_length[group][gene] = []
                    ancestry_group_to_gene_to_length[group][gene].extend(lengths)
                    #print(ancestry_group_to_gene_to_length)

    # TODO format everything
    # TODO integrate all three scripts in a single script
    # TODO debug: negativ values?
    # Plot
    
    timestamp = time.strftime("%Y%m%d", time.localtime())   # used for plotnames
    gene_to_range = {}
    for gene in gene_to_length.keys():
        gene_to_range[gene] = ( min(gene_to_length[gene]), max(gene_to_length[gene]) )
    gene_to_range["FOCAD1"] = (3000, 4800)
    gene_to_range["ASB1"] = (1500, 4500)
    gene_to_range["CLASP1"] = (2000, 3500)
    set_plot_fonts()

    # Plot gene plots
    figure, histograms = plt.subplots(nrows=2, ncols=2)
    figure.set_figwidth(10)
    figure.set_figheight(10)
    figure.suptitle("Genes")
    r = 0
    c = 0
    for gene, lengths in sorted(gene_to_length.items()):
        plt.hist(lengths, bins=250, range=gene_to_range[gene])
        plt.savefig(workdir + "/output/plots/genes/singles/{ftime}_{fgene}.png".format(ftime=timestamp, fgene=gene))
        plt.close()
        length_of_gene = gene_to_range[gene][1] - gene_to_range[gene][0]
        number_of_bins = int(length_of_gene / 100)
        histograms[c][r].set_title(gene)
        histograms[c][r].hist(lengths, bins=250, range=gene_to_range[gene])
        c += 1
        mod = c % 2
        if mod == 0:
            r += 1
            c = 0
    figure.savefig(workdir + "/output/plots/genes/{ftime}_genes.png".format(ftime=timestamp))
    plt.close()

    # Plot ancestry_group plots
    for gene in gene_to_length.keys():
        figure, histograms = plt.subplots(nrows=2, ncols=3)
        figure.suptitle(gene)
        figure.set_figheight(8)
        figure.set_figwidth(12)
        length_of_gene = gene_to_range[gene][1] - gene_to_range[gene][0]
        number_of_bins = int(length_of_gene / 100)
        c = 0
        r = 0
        for ancestry_group, gene_len_dict in sorted(ancestry_group_to_gene_to_length.items()):
            plt.hist(gene_len_dict[gene], bins=250, range=gene_to_range[gene])
            plt.savefig(workdir + "/output/plots/groups/singles/{ftime}_{fgene}_{fancestrygroup}.png".format(ftime=timestamp, fgene=gene, fancestrygroup=ancestry_group))
            plt.close()
            histograms[r][c].set_title(ancestry_group)
            histograms[r][c].hist(gene_len_dict[gene], bins=250, range=gene_to_range[gene])
            c += 1
            mod = c % 3
            if mod == 0:
                r += 1
                c = 0
        figure.savefig(workdir + "/output/plots/groups/{ftime}_{fgene}_groups.png".format(ftime=timestamp, fgene=gene))
        plt.close()

    # Plot ancestry plots
    for gene in gene_to_length.keys():
        figure, histograms = plt.subplots( ncols=4, nrows=7 )
        figure.set_figheight(24)
        figure.set_figwidth(24)
        figure.suptitle(gene)
        length_of_gene = gene_to_range[gene][1] - gene_to_range[gene][0]
        number_of_bins = int(length_of_gene / 100)
        r = 0
        c = 0
        for ancestry, gene_len_dict in sorted(ancestry_to_gene_to_length.items()):
            plt.hist(gene_len_dict[gene], bins=250, range=gene_to_range[gene])
            plt.savefig(workdir + "/output/plots/ancestries/singles/{ftime}_{fgene}_{fancestry}.png".format(ftime=timestamp, fgene=gene, fancestry=ancestry))
            plt.close()
            histograms[r][c].set_title(ancestry)
            histograms[r][c].hist(gene_len_dict[gene], bins=250, range=gene_to_range[gene])
            c += 1
            mod = c % 4
            if mod == 0:
                r += 1
                c = 0
        figure.savefig(workdir + "/output/plots/ancestries/{ftime}_{fgene}_ancestries.png".format(ftime=timestamp, fgene=gene))
        plt.close()
        
if __name__ == '__main__':
    main()