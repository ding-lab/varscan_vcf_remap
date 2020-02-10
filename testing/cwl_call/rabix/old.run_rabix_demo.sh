cd ../..
CWL="cwl/varscan_vcf_remap.cwl"
YAML="testing/cwl_call/demo.yaml"

mkdir -p results
RABIX_ARGS="--basedir results"

rabix $RABIX_ARGS $CWL $YAML
