#!/bin/sh
# Begin SLURM directives
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=1:00:00
#SBATCH --qos=rapid
#SBATCH --output=/users/klaus.ehrlinger/mre_analysis/logs/mre_analysis_output_%A_%a.log
#SBATCH --error=/users/klaus.ehrlinger/mre_analysis/logs/mre_analysis_error_%A_%a.err
#SBATCH --mail-type=ALL
#SBATCH --array=1-150
# End SLURM directives

WORKDIR=/users/klaus.ehrlinger/mre
SAMPLE=$(tail -$SLURM_ARRAY_TASK_ID ${WORKDIR}/input/mre_analysis_samples.txt | head -1)
OUTDIR=/users/klaus.ehrlinger/mre/test_data/

ARG1="chr9 20972000 20976000"
ARG2="chr2 238776000 238778000"
ARG3="chr2 121610000 121613000"

ml build-env/f2022
ml python/3.10.8-gcccore-12.2.0-bare

echo $SAMPLE
python3 $WORKDIR/scripts/mre_analysis.py $SAMPLE $ARG1 > ${OUTDIR}${SAMPLE}_FOCAD1_output.fa
python3 $WORKDIR/scripts/mre_analysis.py $SAMPLE $ARG2 > ${OUTDIR}${SAMPLE}_ASB1_output.fa
python3 $WORKDIR/scripts/mre_analysis.py $SAMPLE $ARG3 > ${OUTDIR}${SAMPLE}_CLASP1_output.fa
