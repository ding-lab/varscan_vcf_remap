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

function test_exit_status {
    # Evaluate return value for chain of pipes; see https://stackoverflow.com/questions/90418/exit-shell-script-based-on-process-exit-code
    rcs=${PIPESTATUS[*]};
    for rc in ${rcs}; do
        if [[ $rc != 0 ]]; then
            >&2 echo Fatal error.  Exiting.
            exit $rc;
        fi;
    done
}


if [ -z $OUT ]; then
    >&2 echo Output VCF not specified.  Quitting.
    exit 1
fi

OUTD=$(dirname $OUT)
CMD="mkdir -p $OUTD"
>&2 echo Running: $CMD
eval $CMD
test_exit_status

export PYTHONPATH="/opt/varscan_vcf_remap/src:$PYTHONPATH"

MERGE_FILTER="vcf_filter.py --no-filtered --local-script varscan_vcf_remap.py"  # filter module

# exclude variants reported by just one caller
MERGE_FILTER_ARGS="$XARG" 

CMD="$MERGE_FILTER $VCF $MERGE_FILTER_ARGS"

if [ $OUT != '-' ]; then
    CMD="$CMD > $OUT"
fi

>&2 echo Running: $CMD
eval $CMD
test_exit_status

>&2 echo Written to $OUT

