IMAGE="mwyczalkowski/varscan_vcf_remap"

cd ..
docker build -t $IMAGE -f docker/Dockerfile .
