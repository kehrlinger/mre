#!/usr/bin/env python3
import os
import argparse

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
                    length_of_alignment_to_ROI = ROI_end - ROI_start
                    
                    # Write out the negative and suspiciously long reads:
                    if length_of_alignment_to_ROI < 1000:
                        print(file, read_ID, length_of_alignment_to_ROI)
                    if length_of_alignment_to_ROI > 6100:
                        print(file, read_ID, length_of_alignment_to_ROI)
                    
                    dict_of_lengths[ (sample_ID, gene_name) ][read_ID] = length_of_alignment_to_ROI
            fh_input.close()

    return (dict_of_lengths)

def write_dict_to_file(input_directory, dict_of_lengths):
    output_string = str()

    with open(input_directory + "a_results.txt", "w") as fh_output:
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
    parser = argparse.ArgumentParser(description="input_directory")
    parser.add_argument("input_directory", type=str)
    args = parser.parse_args()
    input_dir = args.input_directory
    file_stats = {}

    # file_stats[ (sample_ID, gene_name) ]:{read_ID: length_of_alignment_to_ROI}
    file_stats = create_stat_dict(input_dir)
    #write_dict_to_file(input_dir, file_stats)
    #print_dict(file_stats)
            
if __name__ == '__main__':
    main()