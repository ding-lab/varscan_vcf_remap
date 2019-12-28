# Wrapper script for running varscan_vcf_remap.py from within docker container
#
# Usage:
#   bash run_varscan_vcf_remap.sh [args] input.vcf output.vcf 
# args are zero or more optional arguments:
#   --debug and --debug_merge will print out debug info to STDERR
# If output.vcf is -, write to stdout

VCF=$1; shift
OUT=$1; shift
XARG="$@"  # https://stackoverflow.com/questions/1537673/how-do-i-forward-parameters-to-other-command-in-bash-script

if [ -z $OUT ]; then
    >&2 echo Output VCF not specified.  Quitting.
    exit 1
fi

export PYTHONPATH="/opt/varscan_vcf_remap/src:$PYTHONPATH"

MERGE_FILTER="vcf_filter.py --no-filtered --local-script varscan_vcf_remap.py"  # filter module

# exclude variants reported by just one caller
MERGE_FILTER_ARGS="$XARG" 

if [ $OUT == '-' ]; then
    $MERGE_FILTER $VCF $MERGE_FILTER_ARGS 
else
    $MERGE_FILTER $VCF $MERGE_FILTER_ARGS > $OUT
fi

# Evaluate return value for chain of pipes; see https://stackoverflow.com/questions/90418/exit-shell-script-based-on-process-exit-code
rcs=${PIPESTATUS[*]};
for rc in ${rcs}; do
    if [[ $rc != 0 ]]; then
        >&2 echo Fatal error.  Exiting.
        exit $rc;
    fi;
done

>&2 echo Written to $OUT

