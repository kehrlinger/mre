#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import random

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
    parser = argparse.ArgumentParser(description="input_file ancestry_table")
    parser.add_argument("input_file", type=str)
    parser.add_argument("ancestry_table", type=str)
    args = parser.parse_args()

    input_file = args.input_file
    ancestry_table = args.ancestry_table

    sample_to_ancestry = {}           # { sample -> ancestry }
    ancestries_regions_lengths = {}   # { ancestry -> { region -> [ lengths ] } }
    regions_lengths = {}              # { region -> [ lengths ] }

    # populate sample_to_ancestry
    # and initialize first level of ancestries_regions_lengths

    with open(ancestry_table, "r") as fh_input_ancestry:
        for line in fh_input_ancestry:
            (sample, ancestry) = line.strip().split()
            sample_to_ancestry[sample] = ancestry
            ancestries_regions_lengths[ancestry] = {}

        fh_input_ancestry.close()

    ### down/up sample the read lengths so we have an equal number in each sample

    # read data from file and break it down by sample/region/lengths

    samples_regions_lengths = {}

    with open(input_file, "r") as fh_input:
        for line in fh_input:
            items = line.strip().split()
            if len(items) != 3:
                continue

            (sample, region, length) = items
            length = int(length)

            if sample not in samples_regions_lengths:
                samples_regions_lengths[sample] = {}

            if region not in samples_regions_lengths[sample]:
                samples_regions_lengths[sample][region] = []

            samples_regions_lengths[sample][region].append(length)

    # populate regions_lengths and ancestries_regions_lengths

    for (sample, r2l) in samples_regions_lengths.items():
        for (region, lengths) in r2l.items():
            if len(lengths) > 15:
                lengths = random.sample(lengths, 15)

            ancestry = sample_to_ancestry[sample]

            # add to regions_lengths
            if region not in regions_lengths:
                regions_lengths[region] = []

            regions_lengths[region].extend(lengths)

            # add to ancestries_regions_lengths
            if region not in ancestries_regions_lengths[ancestry]:
                ancestries_regions_lengths[ancestry][region] = []

            ancestries_regions_lengths[ancestry][region].extend(lengths)

        fh_input.close()

    ### plot

    # consistent x-axis ranges for the regions

    regions_to_range = {}
    for (region, lengths) in regions_lengths.items():
        regions_to_range[region] = ( min(lengths), max(lengths) )

    regions_to_range["ASB1"] = (1500, 4500)
    regions_to_range["CLASP1"] = (2500, 3500)
    regions_to_range["FOCAD"] = (3500, 4700)

    set_plot_fonts()

    # overall plots for each region

    fig, axes = plt.subplots(nrows=2, ncols=2)
    r = c = 0

    fig.set_figwidth(12)
    fig.set_figheight(6)

    for (region, lengths) in regions_lengths.items():
        axes[r][c].set_title(region)
        axes[r][c].hist( lengths, bins = 100, range = regions_to_range[region] )
        c = (c + 1) % 2
        if c == 0:
            r += 1

    fig.tight_layout()
    fig.savefig(f"plot_overall.png") # why f?

    # ancestry plots for each region

    for region in regions_lengths.keys():
        fig, axes = plt.subplots(nrows=7, ncols=4)
        r = c = 0

        fig.set_figwidth(12)
        fig.set_figheight(12)
        fig.suptitle(region)

        for (ancestry, regions) in sorted( ancestries_regions_lengths.items() ):
            lengths = regions[region]

            # axes[r][c].set_ylim(top = 300)
            axes[r][c].set_title(ancestry)

            rnge = regions_to_range[region]
            # nbins = ( rnge[1] - rnge[0] ) // 50
            nbins = 50

            axes[r][c].hist( lengths, bins = nbins, range = rnge )
            c = (c + 1) % 4
            if c == 0:
                r += 1

        fig.tight_layout()
        fig.savefig(f"plot_{region}.png")

if __name__ == '__main__':
    main()

