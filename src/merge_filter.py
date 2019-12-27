from __future__ import print_function
import sys
import vcf.filters
import ConfigParser
import os.path

# Based on https://github.com/ding-lab/TinDaisy-Core/blob/master/src/vcf_filters/merge_filter.py

def eprint(*args, **kwargs):
# Portable printing to stderr, from https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python-2
    print(*args, file=sys.stderr, **kwargs)


# filter to include or exclude calls based on their caller, as defined by INFO field "set"
class VarscanVCFFilter(vcf.filters.Base):
    'Filter variant sites by caller, as defined by INFO field "set".'

    name = 'merge'

    @classmethod
    def customize_parser(self, parser):
        parser.add_argument('--debug', action="store_true", default=False, help='Print debugging information to stderr')
        parser.add_argument('--bypass', action="store_true", default=False, help='Bypass filter by retaining all variants')

    def __init__(self, args):

        self.debug = args.debug
        self.bypass = args.bypass

# Want the following field:

##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths for the ref and alt alleles in the order listed">

        # below becomes Description field in VCF
        if self.bypass:
            self.__doc__ = "Bypassing Merge filter, retaining all reads"
        elif self.including:
            self.__doc__ = "Retain calls where 'set' INFO field includes one of " + args.include
        else:
            self.__doc__ = "Exclude calls where 'set' INFO field includes any of " + args.exclude

    def filter_name(self):
        return self.name

    def __call__(self, record):
        # "caller" is defined by "set" info field
        caller = record.INFO['set']

        if self.bypass:
            if (self.debug): eprint("** Bypassing %s filter, retaining read **" % self.name )
            return

        if self.including:
            # keep call only if caller is in callers list
            if caller not in self.callers:
                if (self.debug): eprint("** FAIL: %s not in %s **" % (caller, str(self.callers)))
                return "unknown " + caller
            else:
                if (self.debug): eprint("** PASS: %s in %s **" % (caller, str(self.callers)))
                return
        else:                 
            # keep call only if caller is not in callers list
            if caller in self.callers:
                if (self.debug): eprint("** FAIL: %s is in %s **" % (caller, str(self.callers)))
                return "excluding " + caller
            else:
                if (self.debug): eprint("** PASS: %s not in %s **" % (caller, str(self.callers)))
                return
