class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: mnp_filter
baseCommand:
  - python
  - /opt/mnp_filter/src/mnp_filter.py
inputs:
  - id: input
    type: File
    inputBinding:
      position: 0
      prefix: '--input'
    label: VCF file
  - id: bam
    type: File
    inputBinding:
      position: 0
      prefix: '--bam'
    label: tumor bam
    secondaryFiles:
      - .bai
  - id: output
    type: string
    inputBinding:
      position: 0
      prefix: '--output'
    label: output VCF file name
outputs:
  - id: filtered_VCF
    type: File
    outputBinding:
      glob: $(inputs.output)
label: mnp_filter
requirements:
  - class: DockerRequirement
    dockerPull: 'dinglab2/mnp_filter:20191211'
  - class: InlineJavascriptRequirement
  - class: ResourceRequirement
    ramMin: 2000

