class: CommandLineTool
cwlVersion: v1.0
id: varscan_vcf_remap
baseCommand:
  - /bin/bash
  - /opt/varscan_vcf_remap/src/run_varscan_vcf_remap.sh
inputs:
  - id: input
    type: File
    inputBinding:
      position: 1
    label: VCF file
  - id: germline
    type: boolean?
    inputBinding:
      position: 99
      prefix: '--germline'
    label: germline
    doc: Process germline varscan calls.  Default somatic calls
outputs:
  - id: remapped_VCF
    type: File
    outputBinding:
      glob: varscan-remapped.vcf
label: varscan_vcf_remap
arguments:
  - position: 2
    valueFrom: varscan-remapped.vcf
requirements:
  - class: DockerRequirement
    dockerPull: 'mwyczalkowski/varscan_vcf_remap:20200610'
  - class: InlineJavascriptRequirement
  - class: ResourceRequirement
    ramMin: 2000

