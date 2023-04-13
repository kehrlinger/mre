#!/usr/bin/env python3

"""
Usage example:
rm -r output/sorted_reads/*.fa                                  # Clear up old output to prevent appending on existing files
&& time                                                         # Measure time of script
python3 /groups/bi-marvl/klaus/mre/scripts/mre_phase_reads.py /groups/bi-marvl/klaus/mre/input/phase/tagged 
> /groups/bi-marvl/klaus/mre/output/sorted_reads/debug.txt      # Write debug output to a file
&& ls output/sorted_reads/ | wc -l                              # Count the number of generated files as a sanity check

"""

import argparse
import os
import pysam
import time

def main():
    # Define Variables
    parser = argparse.ArgumentParser(description="input_path_without_slash_at_the_end")
    parser.add_argument("path_to_input_files", type=str)
    args = parser.parse_args()
    path_to_input_files = args.path_to_input_files
    path_to_work_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # /groups/bi-marvl/klaus/mre
    timestamp = time.strftime("%Y%m%d", time.localtime()) # For file names
    input_files = []

    # Collect list of .bam files in folder
    for file in os.popen("ls " + path_to_input_files, "r"):
          file = file.strip()
          if file.endswith(".bam"):
                input_files.append(file)
    
    # Sort reads by haplotype for every .bam file
    for bam_file_in_folder in input_files:
        sample_chr_start_end = bam_file_in_folder[:-4]
        sample, chr, start, end = sample_chr_start_end.split("_")
        start = int(start)
        end = int(end)
        reads = {}
        debug_reads = {}
        print(sample, chr, start, end) # For debugging file
        bam_file = pysam.AlignmentFile(path_to_input_files + "/" + bam_file_in_folder, "rb")
        
        for pileupcolumn in bam_file.pileup(chr, start, end+1, truncate=True, stepper="all"):
            for pileupread in pileupcolumn.pileups:

                # Skip reads that have no HP tag or are supplementary reads
                if pileupread.alignment.is_supplementary == True:
                    continue
                if pileupread.alignment.has_tag("HP") == False:
                    continue
                
                # Collect info in dict 
                if pileupcolumn.pos == start:
                    reads[pileupread.alignment.query_name] = [pileupread.query_position_or_next, None, None, None, None] # start, end, length_on_ROI, haplotype, sequence

                if pileupcolumn.pos == end:
                    try:
                        reads[pileupread.alignment.query_name][1] = pileupread.query_position_or_next
                        reads[pileupread.alignment.query_name][2] = pileupread.query_position_or_next - reads[pileupread.alignment.query_name][0]
                        reads[pileupread.alignment.query_name][3] = pileupread.alignment.get_tag("HP")
                        reads[pileupread.alignment.query_name][4] = \
                pileupread.alignment.query_sequence[reads[pileupread.alignment.query_name][0]:reads[pileupread.alignment.query_name][1]]
                    except:
                         continue
            
            # Write the sorted reads of each haplotype in separate files
            for read_id, ROIstart_ROIend_length_haplotype_sequence in reads.items():

                # Define needed variables, and construct the output file name
                start_of_ROI, end_of_ROI, length_on_ROI, haplotype, sequence = ROIstart_ROIend_length_haplotype_sequence
                path_to_output_file = f"{path_to_work_dir}/output/sorted_reads/{timestamp}_{sample}_{chr}_{start}_{end}_{haplotype}.fa"

                # Collect the reads with missing info
                if None in ROIstart_ROIend_length_haplotype_sequence:
                    if read_id not in debug_reads:
                         debug_reads[read_id] = [start_of_ROI, end_of_ROI, length_on_ROI, haplotype]
                    debug_reads[read_id] = [start_of_ROI, end_of_ROI, length_on_ROI, haplotype]
                    continue
                
                # Write to file
                with open(path_to_output_file, "a") as fh_output:
                    fh_output.write(f">{read_id} {start_of_ROI} {end_of_ROI} {length_on_ROI} {haplotype}\n{sequence}\n")
        
        # Print out the faulty reads
        for read_id, read_values in debug_reads.items():
             print(read_id, read_values)

if __name__ == "__main__":
        main()