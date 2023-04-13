#!/usr/bin/env bash

INPUT_DIR="/groups/bi-marvl/klaus/mre/output/sorted_reads"
OUTPUT_DIR="/groups/bi-marvl/klaus/mre/output/msa"
SAMPLE_LIST=$(ls $INPUT_DIR)
#echo $SAMPLE_LIST
for FILE in $SAMPLE_LIST
do
    clustalo-1.2.4 --force -i /groups/bi-marvl/klaus/mre/output/sorted_reads/${FILE} -o /groups/bi-marvl/klaus/mre/output/msa/${FILE}_msa.fa
done