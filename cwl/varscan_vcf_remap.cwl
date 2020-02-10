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
  - id: output
    type: string
    inputBinding:
      position: 2
    label: output VCF file name
outputs:
  - id: remapped_VCF
    type: File
    outputBinding:
      glob: $(inputs.output)
label: varscan_vcf_remap
requirements:
  - class: DockerRequirement
    dockerPull: 'mwyczalkowski/varscan_vcf_remap:20200210'
  - class: InlineJavascriptRequirement
  - class: ResourceRequirement
    ramMin: 2000

