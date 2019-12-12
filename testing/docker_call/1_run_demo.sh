IMAGE="dinglab2/mnp_filter:20191211"
DATD="../demo_data"

# Using python to get absolute path of DATD.  On Linux `readlink -f` works, but on Mac this is not always available
# see https://stackoverflow.com/questions/1055671/how-can-i-get-the-behavior-of-gnus-readlink-f-on-a-mac
ADATD=$(python -c 'import os,sys;print(os.path.realpath(sys.argv[1]))' $DATD)

VCF="/data/merged.filtered_for_test_DNP_TNP_QNP.vcf"
BAM="/data/synthetic.BWA.bam"
OUT="/data/mnp_combined.vcf"

CMD="python /opt/mnp_filter/src/mnp_filter.py --input $VCF --bam $BAM --output $OUT"

docker run -v $ADATD:/data -it $IMAGE $CMD

