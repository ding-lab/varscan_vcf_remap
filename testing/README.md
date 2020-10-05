Several levels of calls available for testing

- direct\_call: Calling directly from within container
- docker\_call: Instantiate docker container and call scripts within it
- cwl\_call: Run rabix or Cromwell workflow manager to call CWL workflow

# Test data
Testing calls with real data which is not distributed as part of this filter

# Test data

Some somatic calls in demo_data/varscan_indel_vcf.vcf

## Somatic
For Somatic calls, testing at this point C3L-00908, with the specific SNP and indel files:

* /data/call-parse_varscan_indel/execution/results/varscan/filter_indel_out/varscan.out.som_indel.Somatic.hc.vcf
* /data/call-parse_varscan_snv/execution/results/varscan/filter_snv_out/varscan.out.som_snv.Somatic.hc.somfilter_pass.vcf

On katmai, data root is copied to 
    /home/mwyczalk_test/Projects/TinDaisy/testing/C3L-00908-data/dat
See there for more details about C3L-00908

## Germline

On MGI, data source apparently here:
    DATA_ROOT="/gscmnt/gc2508/dinglab/mwyczalk/GermlineCaller.Testing/C3L-00001"


