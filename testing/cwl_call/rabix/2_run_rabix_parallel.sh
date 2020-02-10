cd ../../..
CWL="cwl/GATK_GermlineCaller.cwl"
YAML="testing/cwl_call/demo_parallel.yaml"

mkdir -p results
RABIX_ARGS="--basedir results"

rabix $RABIX_ARGS $CWL $YAML
