# Basic script to start docker container

source docker_image.sh

DATD=$1

if [ "$DATD" ]; then
    # Using python to get absolute path of DATD.  On Linux `readlink -f` works, but on Mac this is not always available
    # see https://stackoverflow.com/questions/1055671/how-can-i-get-the-behavior-of-gnus-readlink-f-on-a-mac
    ADATD=$(python -c 'import os,sys;print(os.path.realpath(sys.argv[1]))' $DATD)
    >&2 echo Mounting $ADATD to /data

    MNT="-v $ADATD:/data"
fi

# Starting with no mounted volumes:
CMD="docker run $MNT -it $IMAGE /bin/bash"
>&2 echo Running $CMD
eval $CMD
