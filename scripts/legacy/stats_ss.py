#!/usr/bin/env python3

import glob
import os

def main():
    output_dir = "/groups/bi-marvl/klaus/mre/output/"
    file_stats = {} # filestats[sample_gene]:(read_id, roi_start, roi_end, length)

    # Loop over all files in the folder, and create dict as values for sample names in the file_stats dict
    for file in glob.glob( os.path.join(output_dir, "*.fa") ):
        (sample, gene, _dummy) = os.path.basename(file).split("_")

        coords = []
        file_stats[ (sample, gene) ] = coords

        # Read from all files in the output folder
        with open(file, "r") as fh_input:
            for line in fh_input.readlines():
                if line.startswith(">"): # or line[0] == ">"
                    id_coordinates = line.split()
                    length = int(id_coordinates[2]) - int(id_coordinates[1])
                    coords.append(length)

            fh_input.close()

    # fh_output = open( os.path.join(output_dir, "results.txt") , "w")
    fh_output = open( "test.txt", "w")

    for key, lengths in file_stats.items():
        (sample, gene) = key
        strlengths = [ str(x) for x in lengths ]
        fh_output.write("{} {} {}\n".format(sample, gene, ",".join(strlengths)))

if __name__ == '__main__':
    main()
