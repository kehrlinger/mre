#!/usr/bin/env python3

def main():
    ancestry_dict = {"AFR_": ["ACB", "ASW", "ESN", "GWD", "LWK", "MSL", "YRI"],\
                     "IND_": ["BEB", "ITU", "PJL", "STU"],\
                     "ASN_": ["CDX", "CHB", "CHS", "JPT", "KHV"],\
                     "SAM_": ["CLM", "MXL", "PEL", "PUR"],\
                     "EUR_": ["CEU", "FIN", "GBR", "IBS", "TSI"],\
                     "NAT_": ["GIH"]}
    output = []
    with open("./ancestries.txt", "r") as fh_input:
        for sample_ancestry in fh_input.readlines():
            [ sample, ancestry ] = sample_ancestry.strip().split()
            for key, value in ancestry_dict.items():
                if ancestry in value:
                    ancestry = key + ancestry
            output_string = sample + "\t" + ancestry + "\n"
            output.append(output_string)
        fh_input.close()

    with open("ancestries_grouped.txt", "w") as fh_output:
        for output_line in output:
            fh_output.write(output_line)
        fh_output.close()
        

if __name__ == "__main__":
    main()