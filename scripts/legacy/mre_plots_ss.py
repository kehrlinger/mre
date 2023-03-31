#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt

def make_hist(data, title, filename):
    pass

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

    # read length data, populate regions_lengths
    # and ancestries_regions_lengths

    with open(input_file, "r") as fh_input:
        for line in fh_input:
            items = line.strip().split()
            if len(items) != 3:
                continue

            (sample, region, lengths) = items
            lengths = [ int(x) for x in lengths.split(",") ]
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

    # plot

    for (region, lengths) in regions_lengths.items():
        # NOTE: f"plot_{region}.png" is the same as "plot_{}.png".format(region)
        make_hist(lengths, region, f"plot_{region}.png")

    for (ancestry, regions) in ancestries_regions_lengths.items():
        for (region, lengths) in regions.items():
            make_hist(lengths, f"{ancestry} {region}", f"plot_{ancestry}_{region}.png")

if __name__ == '__main__':
    main()
