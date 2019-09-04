IMAGE="dinglab2/dnp_filter:20190829"

cd ..
docker build -t $IMAGE -f docker/Dockerfile .
