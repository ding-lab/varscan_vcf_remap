
# Matthew Wyczalkowski
# m.wyczalkowski@wustl.edu
# Washington University School of Medicine

import vcf
import argparse
import pysam
import sys
import os
import collections

from pprint import pprint

# Modify meta-information lines in vcf_reader object
# * FORMAT field for RD is removed
# * FORMAT field for AD is modified to be,
#    ##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths for the ref and alt alleles in the order listed">

def modify_headers(vcf_reader):

    del vcf_reader.formats['RD']

    # Currently:
#    ('AD', Format(id='AD', num=1, type='Integer', desc='Depth of variant-supporting bases (reads2)'))
    # based on inspection of /usr/local/lib/python3.8/site-packages/vcf/parser.py
    Format = collections.namedtuple('new_format', ["id", "num", "type", "desc"])
    AD_new=Format("AD", "R", "Integer", "Allelic depths for the ref and alt alleles in the order listed")
    vcf_reader.formats["AD"]= AD_new

    return vcf_reader


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update AD fields in varscan VCF file")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debugging information to stderr")
    parser.add_argument("-i", "--input", default="stdin", dest="infn", help="Input vcf file name")
    parser.add_argument("-o", "--output", default="stdout", dest="outfn", help="Output file name")
   
    args = parser.parse_args()

    print("Input VCF: {}".format(args.infn), file=sys.stderr)
    print("Output VCF: {}".format(args.outfn), file=sys.stderr)

    if args.infn == "stdin":
        f = sys.stdin
    else:
        f = open(args.infn, 'r')
    if args.outfn == "stdout":
        o = sys.stdout
    else:
        o = open(args.outfn, "w")
 
    vcf_reader = vcf.Reader(fsock=f)
    vcf_reader_mod = modify_headers(vcf_reader)
    # 1	3348577	.	C	T	.	PASS	DP=72;SOMATIC;SS=2;SSC=15;GPV=1.0;SPV=0.030584	GT:GQ:DP:RD:AD:FREQ:DP4	0/0:.:41:41:0:0%:39,2,0,0	0/1:.:31:27:4:12.9%:25,2,3,1

    vcf_writer = vcf.Writer(o, vcf_reader_mod)
    New_Call = collections.namedtuple('new_call', ["GT", "GQ", "DP", "AD", "FREQ", "DP4"])
    for record in vcf_reader:
        record.FORMAT="abcde"
        #print(record.genotype("NORMAL").data)
        data=record.genotype("NORMAL").data
#        CallData(GT=0/0, GQ=None, DP=41, RD=41, AD=0, FREQ=0%, DP4=39,2,0,0)
        AD=
        call=New_Call(data.GT, data.GQ, data.DP, "GH", "IJ", "KL")
        record.genotype("NORMAL").data = call
        vcf_writer.write_record(record)
        sys.exit()

