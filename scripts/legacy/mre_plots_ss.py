#!/usr/bin/env python3

import matplotlib.pyplot as plot

def main():
    fin = open("/groups/bi-marvl/klaus/mre/output/a_results.txt")

    gene_lengths = {}
    ancestry_gene_lengths = {}

    # read sample -> ancestry dict

    for line in fin:
        items = line.strip().split()
        if len(items) != 3:
            continue

        (sample, gene, lengths) = items
        # sample -> ancestry

        lengths = [ int(x) for x in lengths.split(",") ]

        if gene not in gene_lengths:
            gene_lengths[gene] = []

        gene_lengths[gene].extend( lengths )

    fin.close()

    for gene in gene_lengths.keys():
        genedata = gene_lengths[gene]

        histrange = ( min(genedata), max(genedata) )
        histrange = (1000, 6000)

        plot.hist(genedata, bins=100, range=histrange)
        plot.suptitle(gene)
        plot.show()
        # plot.yscale("log")
        #plot.savefig("plot_{}.png".format(gene))
        #plot.close()

if __name__ == "__main__":
    main()

