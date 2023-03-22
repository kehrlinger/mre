import pysam
import argparse

def main():
    
    parser = argparse.ArgumentParser(description="sample chromosome start end")
    parser.add_argument("sample", type=str)
    parser.add_argument("chromosome", type=str)
    parser.add_argument("start", type=int)
    parser.add_argument("end", type=int)
    args = parser.parse_args()
    sample = args.sample
    chromosome = args.chromosome
    start_arg = args.start
    end_arg = args.end

    filepath = "/groups/bi-marvl/samples/alignments/GRCh38/"
    reference_path = "/groups/bi-marvl/reference/GCA_000001405.15_GRCh38_no_alt_analysis_set_maskedGRC_exclusions_v2.fasta"
    samfile = pysam.AlignmentFile(filepath + sample + "/alignments/" + sample + ".cram", "rc", reference_filename=reference_path)
    reads = {}

    if start_arg > end_arg:
        start = end_arg
        end = start_arg
    else:
        start = start_arg
        end = end_arg
    
    # Iterate over every read in every pileup comlumn in the region of interest.
    # truncate=True looks only for columns in the ROI. stepper="all" should filter secondary alignments.
    for pileupcolumn in samfile.pileup(chromosome, start, end+1, truncate=True, stepper="all"):
        for pileupread in pileupcolumn.pileups:
            if pileupread.alignment.is_supplementary == True:
                continue
            # Extract reads that span the beginning of the ROI.
            if pileupcolumn.pos == start:
                reads[pileupread.alignment.query_name] = [pileupread.query_position_or_next, None, pileupread.alignment.query_sequence]
                # pileupread.alignment.query_alignment_sequence would give only the aligned part of the read (in the ROI?)
            # Extract reads that span the ending of the ROI. Reads that do not span the beginning of the ROI give key errors.
            if pileupcolumn.pos == end:
                try:
                    reads[pileupread.alignment.query_name][1] = pileupread.query_position_or_next
                except:
                    continue
    # Filter reads that do not completely span the ROI
    todelete = set()   
    for read in reads:
        if reads[read][1] == None:
            todelete.add(read)
    for r in todelete:
        del reads[r]

    for read in reads:
        print(">%s %s %s\n%s" % (read, reads[read][0], reads[read][1], reads[read][2]))

if __name__ == '__main__':
    main()