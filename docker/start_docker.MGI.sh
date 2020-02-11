# Starts docker image and mounts given directory as /data
# This is actually not needed at MGI since it mounts everything, but will be needed for compute1

source docker_image.sh

#DATD="/gscmnt/gc2508/dinglab/mwyczalk/GermlineCaller.Testing/C3L-00001/dat"
#DATD=$1

if [ -z $DATD ]; then
    # Using python to get absolute path of DATD.  On Linux `readlink -f` works, but on Mac this is not always available
    # see https://stackoverflow.com/questions/1055671/how-can-i-get-the-behavior-of-gnus-readlink-f-on-a-mac
    ADATD=$(python -c 'import os,sys;print(os.path.realpath(sys.argv[1]))' $DATD)
    >&2 echo Mounting $ADATD to /data

    MNT="-v $ADATD:/data"

    #docker run $MNT -it $IMAGE /bin/bash
fi

bsub -Is -q research-hpc -a "docker($IMAGE)" /bin/bash

