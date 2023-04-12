#!/usr/bin/env python3

"""
Usage example:
time python3 /groups/bi-marvl/klaus/mre/scripts/mre_stats.py /groups/bi-marvl/klaus/mre/output/analysis/ /groups/bi-marvl/klaus/mre/output/stats/ 
This script goes over the fasta files produced by the mre_analysis.py script, and extracts read lengths from it in form of:
    SAMPLE  REGION  CSV_READ_LENGTHS
    HG00098	ASB1	1995,2444,2419,2438,2437,1986,1990
Additionally, this script will print:
    SAMPLE_REGION_output.fa >READ_ID READ_LENGTH
    NA19331_FOCAD1_output.fa >13458565-ac30-44e3-814d-4bb61a460810 525
for reads that are shorter than 1000 and longer than 6100 bp. Pipe to debugging file for troubleshooting.
"""

import os
import argparse
import time

def create_stat_dict(input_directory):
    dict_of_lengths = {}
    list_of_samples_and_ROI = []

    for sample_and_ROI in os.listdir(input_directory):
        list_of_samples_and_ROI.append(sample_and_ROI)

    # Loop over all files in the folder.
    # Create a nested dictionary:
    # dict_of_lengths[ (sample_ID, gene_name) ]:{read_ID: length_of_alignment_to_ROI}
    for file in list_of_samples_and_ROI:
        if ".fa" not in file and ".fasta" not in file:
            continue
        sample_ID = file[:-10].split("_")[0]
        gene_name = file[:-10].split("_")[1]
        dict_of_lengths[ (sample_ID, gene_name) ] = {}

        # Read from all files in the output folder
        with open(input_directory +  file, "r") as fh_input:
            for line in fh_input.readlines():
                if ">" in line:
                    read_id_and_ROI_coordinates = line.split()
                    read_ID = read_id_and_ROI_coordinates[0]
                    ROI_start = int(read_id_and_ROI_coordinates[1])
                    ROI_end = int(read_id_and_ROI_coordinates[2])
                    length_of_alignment_to_ROI = int(read_id_and_ROI_coordinates[3])
                    
                    # Write out the negative and suspiciously long reads:
                    if length_of_alignment_to_ROI < 1000:
                        print(file, read_ID, length_of_alignment_to_ROI)
                    if length_of_alignment_to_ROI > 6100:
                        print(file, read_ID, length_of_alignment_to_ROI)
                    
                    dict_of_lengths[ (sample_ID, gene_name) ][read_ID] = length_of_alignment_to_ROI
            fh_input.close()

    return (dict_of_lengths)

def write_dict_to_file(output_directory, dict_of_lengths):
    output_string = str()
    timestamp = time.strftime("%Y%m%d", time.localtime())

    with open(output_directory + timestamp + "_results.txt", "w") as fh_output:
        
        # sample == (sample_ID, gene_name)
        for sample, dict in dict_of_lengths.items():
            output_string = str(sample[0]) + "\t" + str(sample[1] + "\t") # testcomment for git
            
            for read in dict:
                alignment_length = str(dict[read])
                output_string += alignment_length
                output_string += ","
            
            output_string = output_string[:-1]
            output_string += '\n'
            fh_output.write(output_string)

def print_dict(dict_of_lengths):
    for sample, dict in dict_of_lengths.items():
        print("\n" + sample[0])
        
        for read in dict:
            print(read, dict[read])

def main():
    parser = argparse.ArgumentParser(description="input_directory output_directory")
    parser.add_argument("input_directory", type=str)
    parser.add_argument("output_directory", type=str)
    args = parser.parse_args()
    input_dir = args.input_directory
    output_dir = args.output_directory
    file_stats = {}

    # file_stats[ (sample_ID, gene_name) ]:{read_ID: length_of_alignment_to_ROI}
    file_stats = create_stat_dict(input_dir)
    write_dict_to_file(output_dir, file_stats)
    #print_dict(file_stats)
            
if __name__ == '__main__':
    main()