#!/usr/bin/env python3
import argparse
import matplotlib.pyplot as plt

def make_hist():
    pass

def main():
    parser = argparse.ArgumentParser(description="input_file ancestry_table")
    parser.add_argument("input_file", type=str)
    parser.add_argument("ancestry_table", type=str)
    args = parser.parse_args()
    input_file = args.input_file
    ancestry_table = args.ancestry_table
    ancestry_table_content = []
    master_dict = {}

    with open(ancestry_table, "r") as fh_input_ancestry:
        for line in fh_input_ancestry:
            ancestry_table_content.append(line)
        fh_input_ancestry.close()

    with open(input_file, "r") as fh_input:
        for line in fh_input:
            if len(line.split()) != 3:
                continue
            else:
                line_content = line.strip().split()

            for aline in ancestry_table_content:
                line_list = aline.split()
                if line_content[0] in line_list:
                    line_content.insert(0, line_list[1])
                    break

            if line_content[0] not in master_dict:
                master_dict[line_content[0]] = {line_content[1]: {line_content[2]: line_content[3]}}
            elif line_content[1] not in master_dict[line_content[0]]:
                master_dict[line_content[0]][line_content[1]] = {line_content[2]: line_content[3]}
            elif line_content[2] not in master_dict[line_content[0]][line_content[1]]:
                master_dict[line_content[0]][line_content[1]][line_content[2]] = line_content[3]
        fh_input.close()
        
        fig, axs = plt.subplots(2, 2, figsize=(4, 3), layout="constrained")
        
        for ancestry, dict1 in master_dict.items():
            plot_dict = {}
            for sample, dict2 in dict1.items():
                for gene in dict2.keys():
                    if gene not in plot_dict:
                        plot_dict[gene] = []
                    y = [int(x) for x in dict2[gene].split(",")]     
                    plot_dict[gene].extend(y)
            for goi in plot_dict.keys():
                print(ancestry, goi)
                fig, ax = plt.subplots(figsize = (10, 7))
                ax.hist(plot_dict[goi], bins=25, range=(1000, 6000))
                plt.savefig("/groups/bi-marvl/klaus/mre/plots/plot_%s_%s.png" % (ancestry, goi))

        #histrange = (1000, 6000)
        #plt.hist(master_dict, bins=100, range=histrange)
        #plt.show()

if __name__ == '__main__':
    main()