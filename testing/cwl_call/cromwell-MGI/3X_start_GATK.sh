# Usage: bash 3X_start_run.sh YAML

YAML=$1

if [ -z $YAML ]; then
    >&2 echo ERROR: please pass YAML file
    exit 1
fi
if [ ! -e $YAML ]; then
    >&2 echo ERROR: $YAML does not exist
    exit 1
fi

# This file below is for MGI
source /opt/lsf9/conf/lsf.conf

ARGS="-Xmx10g"
DB_ARGS="-Djavax.net.ssl.trustStorePassword=changeit -Djavax.net.ssl.trustStore=/home/m.wyczalkowski/lib/cromwell-jar/cromwell.truststore"
CROMWELL_JAR="/usr/local/cromwell/cromwell-47.jar"  # this is in CromwellRunner container
CWL="../../../cwl/GATK_GermlineCaller.cwl"
CONFIG="-Dconfig.file=dat/cromwell-config-db.dat"

/usr/bin/java $ARGS $CONFIG $DB_ARGS -jar $CROMWELL_JAR run -t cwl -i $YAML $CWL

