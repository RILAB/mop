# mop
Simple tool for capturing alignment regions with sufficient quality for genotyping.

This script has only been tested on Linux systems.

Requires Python3 with libraries: `argparse`, `numpy` `os`, `re`, `io`, `subprocess`.
Requires fully installed version of `samtools` with `mpileup`.

Run the following command to see usage options:

`$ python mop.py -h`

Assumes all input bam files in the required bamlist were aligned to the same reference genome. 
