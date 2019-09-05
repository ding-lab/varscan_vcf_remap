IMAGE="dinglab2/dnp_filter:20190905"

cd ..
docker build -t $IMAGE -f docker/Dockerfile .
