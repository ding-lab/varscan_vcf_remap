IMAGE="dinglab2/dnp_filter:20190829"
DATD="../demo_data"

# Using python to get absolute path of DATD.  On Linux `readlink -f` works, but on Mac this is not always available
# see https://stackoverflow.com/questions/1055671/how-can-i-get-the-behavior-of-gnus-readlink-f-on-a-mac
ADATD=$(python -c 'import os,sys;print(os.path.realpath(sys.argv[1]))' $DATD)

VCF="/data/merged.filtered.vcf"
BAM="/data/test.bam"
THRESHOLD=0.5
OUT="/data/DNP_combined.vcf"

CMD="python /opt/dnp_filter/src/DNP_filter_v2.py --input $VCF --bam $BAM --threshold $THRESHOLD --output $OUT"

docker run -v $ADATD:/data -it $IMAGE $CMD

