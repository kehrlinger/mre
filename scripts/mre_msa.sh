#!/usr/bin/env bash

INPUT_DIR_MSA="/groups/bi-marvl/klaus/mre/output/sorted_reads"
OUTPUT_DIR_MSA="/groups/bi-marvl/klaus/mre/output/msa"
OUTPUT_DIR_CONS="/groups/bi-marvl/klaus/mre/output/consensus"
SAMPLE_LIST_MSA=$(ls $INPUT_DIR_MSA)

rm $OUTPUT_DIR_CONS/*
touch $OUTPUT_DIR_CONS/placeholder.txt
rm $OUTPUT_DIR_MSA/*
touch $OUTPUT_DIR_CONS/placeholder.txt

for FILE in $SAMPLE_LIST_MSA
do
    FILE_NAME=$(basename ${FILE} .fa)
    muscle -msf -in ${INPUT_DIR_MSA}/${FILE} -out ${OUTPUT_DIR_MSA}/${FILE_NAME}_msa.msf
    em_cons -sequence ${OUTPUT_DIR_MSA}/${FILE_NAME}_msa.msf -datafile 'EDNAFULL' -outseq ${OUTPUT_DIR_CONS}/${FILE_NAME}_cons.fa
done

