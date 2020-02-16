
# Matthew Wyczalkowski
# m.wyczalkowski@wustl.edu
# Washington University School of Medicine

import vcf
import argparse
import pysam
import sys
import os
import collections

#
# Germline version of varscan_vcf_remap.py
# Germline calls have different FORMAT fields than somatic
# they also have one sample rather than two
# Code below is specific for germline, but future work should just have a boolean flag
# to indicate which it is.  Currently remapping all samples, so only the testing of 
# FORMAT field and format of calls would need to be specific to germline or somatic

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
# germline varscan FORMAT field GT:GQ:SDP:DP:RD:AD:FREQ:PVAL:RBQ:ABQ:RDF:RDR:ADF:ADR
# ( somatic calling varscan FORMAT field GT:GQ:DP:RD:AD:FREQ:DP4 )
# This is the output of varscan 2.3.8
# We check for this and error out if does not match.  -w to ignore
# the output FORMAT is then GT:GQ:DP:AD:FREQ:DP4
# 

New_Somatic_Call = collections.namedtuple('new_call', ["GT", "GQ", "DP", "AD", "FREQ", "DP4"])
New_Germline_Call = collections.namedtuple('new_call', \
        [ "GT", "GQ", "SDP", "DP", "AD", "FREQ", "PVAL", "RBQ", "ABQ", "RDF", "RDR", "ADF", "ADR"])

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
    vcf_reader.filters["varscan_AD"]= FILTER_new

    return vcf_reader

def get_new_germline_call(call_data):
    AD="{},{}".format(call_data.RD, call_data.AD)
    call=New_Germline_Call(call_data.GT, call_data.GQ, call_data.SDP, call_data.DP, AD, \
                call_data.FREQ, call_data.PVAL, call_data.RBQ, call_data.ABQ, call_data.RDF, \
                call_data.RDR, call_data.ADF, call_data.ADR)
    return call

def get_new_somatic_call(call_data):
#        CallData(GT=0/0, GQ=None, DP=41, RD=41, AD=0, FREQ=0%, DP4=39,2,0,0)
    AD="{},{}".format(call_data.RD, call_data.AD)
    call=New_Somatic_Call(call_data.GT, call_data.GQ, call_data.DP, AD, call_data.FREQ, call_data.DP4)
    return call

def remap_vcf(f, o, is_germline, onlywarn=False):
    vcf_reader = vcf.Reader(filename=f)

# example VCF line before remapping - somatic
# 1	3348577	.	C	T	.	PASS	DP=72;SOMATIC;SS=2;SSC=15;GPV=1.0;SPV=0.030584	GT:GQ:DP:RD:AD:FREQ:DP4	0/0:.:41:41:0:0%:39,2,0,0	0/1:.:31:27:4:12.9%:25,2,3,1
    vcf_reader_mod = modify_meta_info(vcf_reader)
    vcf_writer = vcf.Writer(open(o, "w"), vcf_reader_mod)

# We want to change the value of AD to match that in mutect_vcf.  Specifically, we want,
#     AD_new = RD_old,AD_old
#     RD_new - delete it

    if is_germline:
        Old_Format = "GT:GQ:SDP:DP:RD:AD:FREQ:PVAL:RBQ:ABQ:RDF:RDR:ADF:ADR"
        New_Format = "GT:GQ:SDP:DP:AD:FREQ:PVAL:RBQ:ABQ:RDF:RDR:ADF:ADR"
    else: # these are somatic
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

        # loop over all genotypes so that this code can work for both germline and somatic calls
        for call in record.samples:
            sample_name=call.sample
            sample_data=call.data
            if (is_germline):
                nc = get_new_germline_call(sample_data)
            else:
                nc = get_new_somatic_call(sample_data)
            record.genotype(sample_name).data = nc

        vcf_writer.write_record(record)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update AD fields in varscan VCF file")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debugging information to stderr")
    parser.add_argument("-i", "--input", dest="infn", help="Input vcf file name")
    parser.add_argument("-o", "--output", dest="outfn", help="Output file name")
    parser.add_argument("-w", "--warn", action="store_true", help="Print warning not error if unexpected value of FORMAT field")
    parser.add_argument("-G", "--germline", action="store_true", help="Process as germline rather than somatic VCF")
    # No longer accepting stdin as input so that can deal with compressed data; want to pass filename to Reader 

    args = parser.parse_args()

    print("Input VCF: {}".format(args.infn), file=sys.stderr)
    print("Output VCF: {}".format(args.outfn), file=sys.stderr)

    remap_vcf(args.infn, args.outfn, args.germline, args.warn)

