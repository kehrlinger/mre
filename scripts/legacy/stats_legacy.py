import os

def main():
    output_dir = "/groups/bi-marvl/klaus/mre/output_original/"
    file_list = []
    file_stats = {} # filestats[sample_gene]:{read_id: length}
    progress_bar = 0
    output_string = str()

    for dir in os.listdir(output_dir):
        file_list.append(dir)

    # Loop over all files in the folder, and create dict as values for sample names in the file_stats dict
    for file in file_list:
        if ".fa" not in file and ".fasta" not in file:
            continue
        sample_and_gene_name = file[:-10]
        file_stats[sample_and_gene_name] = {}

        # Read from all files in the output folder
        with open(output_dir +  file, "r") as fh_input:
            for line in fh_input.readlines():
                if ">" in line:
                    id_coordinates = line.split()
                    length = int(id_coordinates[2]) - int(id_coordinates[1])
                    id_coordinates.append(length)
                    file_stats[sample_and_gene_name][id_coordinates[0]] = id_coordinates[-1]
            fh_input.close()
        progress_bar += 1
        
        # "Progress bar"
        if progress_bar % 100 == False:
            print(progress_bar)

    with open(output_dir + "a_results.txt", "w") as fh_output:
        for sample, dict in file_stats.items():
            output_string = str(sample) + "\t"
            for length in dict:
                output_string += str(dict[length])
                output_string += ","
            output_string = output_string[:-1]
            output_string += '\n'
            fh_output.write(output_string)

    # Print nicely formatted output
    #for sample, dict in file_stats.items():
    #    print("\n" + sample)
    #    for key in dict:
    #        print(key, dict[key])
            
if __name__ == '__main__':
    main()