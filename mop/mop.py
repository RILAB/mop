import argparse
import numpy as np
import os
import re
import io
import subprocess

#from parse_read import parse_read
def main():
    
    prog = 'mop',
    parser = argparse.ArgumentParser(description="Produces bedfile of genomic locations that did or did not map reads sufficiently well. Bed regions are Written to standard out.")

    parser.add_argument("-c", "--single_sites", action='store_true', 
                help = "Output every base separately instead of joining contiguous regions.")

    parser.add_argument("-s", "--bad_sites", action='store_true', 
                help = "Switch to return sites which fail thresholds. Default is to return passing sites.")

    parser.add_argument("-M", "--mean_depth_min", type = int, default=0,
                help = "Minimum mean depth across all individuals.")

    parser.add_argument("-x", "--max_depth", type = float, default = float("inf"),
                help = "Maximum number of bases allowed per individual after accounting for low base and mapping quality. This flag should always be used in conjunction with -m.")

    parser.add_argument("-i", "--min_depth", type = int, default=0, 
                help = "Minimum number of bases required per individual after accounting for low base and mapping quality. This flag should always be used in conjunction with -m.")

    parser.add_argument("-m", "--depth_proportion", type = float, default=0, 
                help = "Minimum proportion of individuals with site counts greater than --min_depth that are required for site to pass. Test is applied after accounting for low base and mapping quality.")

    parser.add_argument("-Q", "--map_quality", type = int, default=0, 
                help = "Minimim mapping quality")

    parser.add_argument("-q", "--base_quality", type = int, default=0, 
                help = "Minimim base quality")

    parser.add_argument('-b', '--bamlist', nargs="?", type=str, required = True,
                help='List of bam files. One per line.')

    #parser.add_argument('-B', '--bedfile', nargs="?", type=argparse.FileType('w'), 
    #		    help='Optional name of the file to write bedfile to.')

    parser.add_argument('-l', '--positions_file', type=str, 
                help='Optional file of reference position to pass to "samtools depth".')

    parser.add_argument('-R', '--positions_string', type=str, 
                help='Optional file of reference position to pass to "samtools depth". Requires input bam files to be indexed.')


    args = parser.parse_args()


    def parse_line(pileup):
        mp = pileup.strip().split("\t")
        chrom, pos, ref = mp[0:3] #site data
        pop_bam = mp[3:]
        idx = list(range(0,len(pop_bam)))
        site_dict = {"chrom": chrom, "ref": ref, "pos": int(pos), "pop_bam": pop_bam, "idx":idx}
        return site_dict

    def qual_check(parse_bam):
        pop_bam = parse_bam['pop_bam']
        idx = parse_bam['idx']
        depth = np.array([int(pop_bam[i]) for i in idx])
        passing = False

        #test total depth
        if np.mean(depth) >= args.mean_depth_min:
            
            #test depth of high-quality bases per individual
            if np.mean(np.logical_and(depth >= args.min_depth, depth <= args.max_depth)) >=  args.depth_proportion:
                passing = True

        return passing

    def printer(chrom, start, end):
        if start > 0 and  end > 0:
            print(f"{chrom}\t{start-1}\t{end}")


    if args.positions_file:	
        cmd = f"samtools depth -q {args.base_quality} -Q {args.map_quality} -aa -b {args.positions_file} -f {args.bamlist}".split()
    elif args.positions_string:
        cmd = f"samtools depth -q {args.base_quality} -Q {args.map_quality} -aa -r {args.positions_string} -f {args.bamlist}".split()
    else:
        cmd = f"samtools depth -q {args.base_quality} -Q {args.map_quality} -aa -f {args.bamlist}".split()

    chrom = ""
    start = -1
    end = -1
    init = True   

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
        line_dict = parse_line(line)
        test = qual_check(line_dict)

        if args.bad_sites:
            if not test:
                if args.single_sites:
                    chrom = line_dict['chrom']
                    start = line_dict['pos']
                    end = line_dict['pos']
                    printer(chrom, start, end)
                else:
                    if line_dict['chrom'] == chrom and line_dict['pos'] == end + 1:
                        end += 1
                        #print('a')
                    else:
                        if not init:
                            printer(chrom, start, end)
                            chrom = line_dict['chrom']
                            start = line_dict['pos']
                            end = line_dict['pos']
                            #print('b')
                        else:
                            chrom = line_dict['chrom']
                            start = line_dict['pos']
                            end = line_dict['pos']
                            #print('c')
                            init = False
        else:
            if test:
                if args.single_sites:
                    chrom = line_dict['chrom']
                    start = line_dict['pos']
                    end = line_dict['pos']
                    printer(chrom, start, end)
                else:
                    if line_dict['chrom'] == chrom and line_dict['pos'] == end + 1:
                        end += 1
                        #print('a')
                    else:
                        if not init:
                            printer(chrom, start, end)
                            chrom = line_dict['chrom']
                            start = line_dict['pos']
                            end = line_dict['pos']
                            #print('b')
                        else:
                            chrom = line_dict['chrom']
                            start = line_dict['pos']
                            end = line_dict['pos']
                            #print('c')
                            init = False
    printer(chrom, start, end)


#main()
