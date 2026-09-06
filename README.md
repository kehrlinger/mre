> **[DEPRECATED]** This repository is no longer maintained here. It has moved to https://forgejo.kehrl.org/Kehrl/mre

# MRE — Nanopore Read-Length Screening for Cloning Candidate Selection

A screening pipeline that uses existing Oxford Nanopore long-read sequencing data from the 1000 Genomes Project to identify samples carrying specific copies of three genes of interest. Work done at the Research Institute of Molecular Pathology (IMP), Vienna, in the group of Moritz Gaidt.

Note: This repo was updated in 2026 with Hermes Agent to test AI-assisted repository maintenance. The original content and structure have been preserved.

## Background

The lab had just completed the Nanopore sequencing effort for the 1000 Genomes Project. The CRAM alignments were fresh and the physical Coriell cell-line samples were still in the freezer. When constructs of ASB1, FOCAD1, and CLASP1 were needed for cloning, the question was: which of these samples carry a homozygous, single-allele version of the target gene?

Heterozygous samples amplify both alleles in a single PCR, producing mixed constructs that must be sorted by colony screening before use. The pipeline screens the existing sequencing data to find homozygous samples instead. Read-length distributions reveal them by their tight, uniform coverage; spread or bimodal patterns flag heterozygosity or structural variation between alleles. Ancestry annotations, inherited from the 1KG metadata, let you optionally select a specific population background for the construct.

## Genes Screened

| Gene | Chromosome | Coordinates (GRCh38) | Window Size |
|------|-----------|----------------------|-------------|
| ASB1  | chr2      | 238,776,000–238,778,000 | ~2 kb |
| FOCAD1 (KIAA1797) | chr9 | 20,972,000–20,976,000 | ~4 kb |
| CLASP1 | chr2    | 121,610,000–121,613,000 | ~3 kb |

## How It Works

### Step 1: Read Extraction

`mre_analysis.py` piles up over a defined genomic window in each sample's CRAM alignment and extracts reads that completely span the region. Output is one FASTA per sample and gene.

```
python3 mre_analysis.py <SAMPLE> <CHR> <START> <END>
```

Each FASTA header records the read's position on the reference and the computed span:

```
>READ_ID ROI_START ROI_END ROI_LENGTH
<sequence>
```

Negative length values appear when pysam reports an incorrect query position at one boundary despite the read spanning the window. These are alignment artifacts and are filtered out downstream.

### Step 2: Read-Length Statistics

`mre_stats.py` parses all FASTA files and collects read-length distributions per sample and gene.

```
python3 mre_stats.py <INPUT_DIR> <OUTPUT_DIR>
```

Output is a tab-separated file:

```
SAMPLE  GENE  CSV_READ_LENGTHS
HG00098 ASB1  1995,2444,2419,2438,2437,1986,1990
```

Reads shorter than 1,000 bp or longer than 6,100 bp are flagged to stderr as alignment artifacts and excluded from candidate lists.

### Step 3: Visualisation

`mre_plots1.3.py` generates read-length histograms per gene, per ancestry group, and per individual ancestry. Clean, tight distributions suggest homozygous samples suitable for cloning.

```
python3 mre_plots1.3.py <STATS_FILE> <ANCESTRY_TABLE>
```

Samples with more than 15 reads are randomly downsampled to 15 before plotting; all histograms are capped at 15 reads per sample-gene pair.

### Step 4: Candidate Selection

`mre_sample_identification.py` reads the stats file and computes average read length per gene per sample, filtering to reads between 2,000 and 6,000 bp. Output in `output/cloning_candidates/` lists samples ranked by average read length and read count.

### Step 5: Haplotype Phasing

`mre_sort_reads.py` takes phased BAM files carrying HP tags and sorts reads into separate FASTA files per haplotype.

```
python3 mre_sort_reads.py <INPUT_DIR_WITH_BAMS>
```

`mre_msa.sh` runs muscle for multiple sequence alignment and EMBOSS `em_cons` to produce a consensus sequence per haplotype.

## Data

1000 Genomes Project samples aligned to GRCh38. CRAM files on the VBC cluster under `/groups/bi-marvl/samples/alignments/GRCh38/`. Physical Coriell samples corresponding to the sequenced lines. Ancestry metadata in `input/ancestries_grouped.txt` (format: `GROUP_ANCESTRY`, e.g. `EUR_Britain`, `AFR_GambianWest`).

## Computing Environment

The pipeline ran on the VBC cluster via SLURM. Scripts contain hardcoded absolute paths and load cluster-specific environment modules. These will not work elsewhere without modification.

## Repository Structure

```
mre/
├── input/                          # Ancestry table and sample list
├── scripts/
│   ├── mre_analysis.py             # CRAM read extraction
│   ├── mre_analysis.sbatch         # SLURM array job
│   ├── mre_stats.py                # Read-length statistics
│   ├── mre_plots1.3.py             # Histogram generation
│   ├── mre_sample_identification.py # Sample lookup utility
│   ├── mre_sort_reads.py           # Haplotype-aware sorting
│   ├── mre_msa.sh                  # MSA + consensus (muscle + emboss)
│   └── legacy/                     # Earlier script versions
├── output/                         # FASTA, stats, plots, MSA, consensus, candidate lists
├── test_data/                      # Small test files used during development
```

## Dependencies

Python 3.10+ with pysam and matplotlib; muscle; EMBOSS.

## License

MIT. See [LICENSE](LICENSE).
