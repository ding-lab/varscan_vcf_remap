# Be sure this is running within cromwell-compatible docker at MGI with,
# 0_start_docker-MGI_cromwell.sh

source /opt/ibm/lsfsuite/lsf/conf/lsf.conf

CONFIG="cromwell-config-db.compute1.dat"

CWL="../../cwl/SomaticSV.cwl"
YAML="cwl-yaml/SomaticSV_demo.yaml"


CROMWELL="/usr/local/cromwell/cromwell-47.jar"

ARGS="-Xmx10g"
DB_ARGS="-Djavax.net.ssl.trustStorePassword=changeit -Djavax.net.ssl.trustStore=/home/m.wyczalkowski/lib/cromwell-jar/cromwell.truststore"

# alternative: /storage1/fs1/bga/Active/gmsroot/gc2560/core/genome/cromwell/cromwell.truststore

# from https://confluence.ris.wustl.edu/pages/viewpage.action?spaceKey=CI&title=Cromwell#Cromwell-ConnectingtotheDatabase
# Connecting to the database section
# Note also database section in config fil
CMD="/usr/bin/java $ARGS -Dconfig.file=$CONFIG $DB_ARGS -jar $CROMWELL run -t cwl -i $YAML $CWL"

echo Running: $CMD
eval $CMD

rc=$?
if [[ $rc != 0 ]]; then
    >&2 echo Fatal error $rc: $!.  Exiting.
    exit $rc;
fi


