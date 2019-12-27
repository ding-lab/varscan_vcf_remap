
# Matthew Wyczalkowski
# m.wyczalkowski@wustl.edu
# Washington University School of Medicine

import vcf
import argparse
import pysam
import sys
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update AD fields in varscan VCF file")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debugging information to stderr")
    parser.add_argument("-i", "--input", default="stdin", dest="vcf_file", help="Input vcf file name")
    parser.add_argument("-o", "--output", default="stdout", dest="output_file", help="Output file name")
   
    args = parser.parse_args()

    print("Input VCF: {}".format(abs_path_vcf), file=sys.stderr)
    print("Output VCF: {}".format(abs_path_output), file=sys.stderr)

   if options.infn == "stdin":
        f = sys.stdin
    else:
        f = open(options.infn, 'r')
    if options.outfn == "stdout":
        o = sys.stdout
    else:
        o = open(options.outfn, "w")
 

