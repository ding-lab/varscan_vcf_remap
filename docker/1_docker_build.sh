IMAGE="dinglab2/dnp_filter:20190916"

cd ..
docker build -t $IMAGE -f docker/Dockerfile .
