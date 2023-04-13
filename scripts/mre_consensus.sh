#!/usr/bin/env bash

INPUT_DIR="/groups/bi-marvl/klaus/mre/output/msa"
OUTPUT_DIR="/groups/bi-marvl/klaus/mre/output/consensus"
SAMPLE_LIST=$(ls $INPUT_DIR)
#echo $SAMPLE_LIST
for FILE in $SAMPLE_LIST
do
    em_cons -sequence ${INPUT_DIR}/${FILE} -datafile 'EDNAFULL' -outseq ${OUTPUT_DIR}/${FILE}_cons.fa
done