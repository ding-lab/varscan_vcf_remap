
# Matthew Wyczalkowski
# m.wyczalkowski@wustl.edu
# Washington University School of Medicine

import vcf
import argparse
import pysam
import sys
import os
import collections

# Modify Varscan-generated VCF files to make format of AD field more consistent with other callers.
# Specifically, value of the per-genotype AD field becomes "RD,AD".  The RD field is removed.
# Care is taken to update the meta-information lines to be consistent with FORMAT fields.
#   Modify meta-information lines in vcf_reader object
#   * FORMAT field for RD is removed
#   * FORMAT field for AD is modified to be,
#     ##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths for the ref and alt alleles in the order listed">
#   ##FILTER=<ID=varscan_AD,Description="Modify varscan AD and RD FORMAT field. New AD is 'RD,AD'; RD is removed ">
# Modify genotype data and FORMAT field as,
# * AD_new=RD_old,AD_old
# * RD is removed from the FORMAT field
#
# We assume a particular order and names of the FORMAT fields.  Specifically, assume
# varscan FORMAT field GT:GQ:DP:RD:AD:FREQ:DP4
# This is the output of varscan 2.3.8
# We check for this and error out if does not match.  -w to ignore
# the output FORMAT is then GT:GQ:DP:AD:FREQ:DP4
# 

New_Call = collections.namedtuple('new_call', ["GT", "GQ", "DP", "AD", "FREQ", "DP4"])

def modify_meta_info(vcf_reader):

    del vcf_reader.formats['RD']
# old meta-information
#    ('AD', Format(id='AD', num=1, type='Integer', desc='Depth of variant-supporting bases (reads2)'))
    # based on inspection of /usr/local/lib/python3.8/site-packages/vcf/parser.py
    Format = collections.namedtuple('new_format', ["id", "num", "type", "desc"])
    AD_new=Format("AD", "R", "Integer", "Allelic depths for the ref and alt alleles in the order listed")
    vcf_reader.formats["AD"]= AD_new

    Filter = collections.namedtuple('new_filter', ['id', 'desc'])
    FILTER_new=Filter("varscan_AD", "Modify varscan AD and RD FORMAT fields. New AD is 'RD,AD'; RD is removed")
#   ##FILTER=<ID=varscan_AD,Description="Modify varscan AD and RD FORMAT field. New AD is 'RD,AD'; RD is removed ">
    vcf_reader.filters["varscan_AD"]= FILTER_new

    return vcf_reader

def get_new_call(call_data):
#        CallData(GT=0/0, GQ=None, DP=41, RD=41, AD=0, FREQ=0%, DP4=39,2,0,0)
    AD="{},{}".format(call_data.RD, call_data.AD)
    call=New_Call(call_data.GT, call_data.GQ, call_data.DP, AD, call_data.FREQ, call_data.DP4)
    return call

def remap_vcf(f, o, onlywarn=False):
    vcf_reader = vcf.Reader(fsock=f)

# example VCF line before remapping
# 1	3348577	.	C	T	.	PASS	DP=72;SOMATIC;SS=2;SSC=15;GPV=1.0;SPV=0.030584	GT:GQ:DP:RD:AD:FREQ:DP4	0/0:.:41:41:0:0%:39,2,0,0	0/1:.:31:27:4:12.9%:25,2,3,1
    vcf_reader_mod = modify_meta_info(vcf_reader)
    vcf_writer = vcf.Writer(o, vcf_reader_mod)

# We want to change the value of AD to match that in mutect_vcf.  Specifically, we want,
#     AD_new = RD_old,AD_old
#     RD_new - delete it

    Old_Format = "GT:GQ:DP:RD:AD:FREQ:DP4"
    New_Format = "GT:GQ:DP:AD:FREQ:DP4"
    for record in vcf_reader:

        if (record.FORMAT != Old_Format):
            msg="unexpected record FORMAT field : Expected {}  Observed {}".format(Old_Format, record.FORMAT)
             
            if onlywarn:
                sys.stderr.write("WARNING: " + msg + "\n")
            else:
                raise(Exception(msg)) 

        record.FORMAT=New_Format
        #print(record.genotype("NORMAL").data)
        normal_data=record.genotype("NORMAL").data
        record.genotype("NORMAL").data = get_new_call(normal_data)

        tumor_data=record.genotype("TUMOR").data
        record.genotype("TUMOR").data = get_new_call(tumor_data)

        vcf_writer.write_record(record)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update AD fields in varscan VCF file")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debugging information to stderr")
    parser.add_argument("-i", "--input", default="stdin", dest="infn", help="Input vcf file name")
    parser.add_argument("-o", "--output", default="stdout", dest="outfn", help="Output file name")
    parser.add_argument("-w", "--warn", action="store_true", help="Print warning not error if unexpected value of FORMAT field")

   
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
 
    remap_vcf(f, o, args.warn)

