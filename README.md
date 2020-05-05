# mop
Simple tool for capturing alignment regions with sufficient quality for genotyping.

This script has only been tested on Linux systems.

Requires Python3 with libraries: `argparse`, `numpy` `os`, `re`, `io`, `subprocess`.
Requires fully installed version of `samtools` with `mpileup`.

Assumes all input bam files in the required bamlist were aligned to the same reference genome. 

Run the following command to see usage options:

`$ python mop.py -h`

which returns:

```
usage: mop.py [-h] [-c] [-s] [-M MEAN_DEPTH_MIN] [-i MIN_DEPTH]
              [-m DEPTH_PROPORTION] [-Q MAP_QUALITY] [-q BASE_QUALITY] -b
              [BAMLIST] [-B [BEDFILE]] [-l POSITIONS_FILE]

Produces bedfile of genomic locations that did or did not map reads
sufficiently well.

optional arguments:
  -h, --help            show this help message and exit
  -c, --single_sites    Output every base separately instead of joining
                        contiguous regions.
  -s, --bad_sites       Switch to return sites which fail thresholds. Default
                        is to return passing sites.
  -M MEAN_DEPTH_MIN, --mean_depth_min MEAN_DEPTH_MIN
                        Minium mean depth across all individuals.
  -i MIN_DEPTH, --min_depth MIN_DEPTH
                        Minimum number of bases required per individual after
                        accounting for low base and mapping quality.
  -m DEPTH_PROPORTION, --depth_proportion DEPTH_PROPORTION
                        Minimum proportion of individuals with site counts
                        greater than --min_depth that are required for site to
                        pass. Test is applied after accounting for low base
                        and mapping quality.
  -Q MAP_QUALITY, --map_quality MAP_QUALITY
                        Minimim mapping quality
  -q BASE_QUALITY, --base_quality BASE_QUALITY
                        Minimim base quality
  -b [BAMLIST], --bamlist [BAMLIST]
                        List of bam files. One per line.
  -B [BEDFILE], --bedfile [BEDFILE]
                        Optional name of the file to write bedfile to.
  -l POSITIONS_FILE, --positions_file POSITIONS_FILE
                        Optional file of reference position to pass to
                        samtools mpileup.
```
