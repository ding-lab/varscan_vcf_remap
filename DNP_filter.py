import vcf
import re
import argparse
import pysam

def search_2_snp(vcf_file):
    vcf_reader = vcf.Reader(open(vcf_file, 'r'))
    chrom_pre = ""
    pos_pre = ""
    ref_pre = ""
    alt_pre = ""
    snps_list = list()
    for record in vcf_reader:
        if re.fullmatch("[ATCG]", str(record.REF)) and re.fullmatch("\[[ATCG]\]", str(record.ALT)):
            if record.CHROM == chrom_pre and record.POS == pos_pre + 1:
                alt_pre_base = re.fullmatch("\[([ATCG])\]", str(alt_pre)).group(1)
                alt_base = re.fullmatch("\[([ATCG])\]", str(record.ALT)).group(1)
                two_snps = str(chrom_pre) + ":" + str(pos_pre) + ":" + str(ref_pre) + ":" + str(alt_pre_base) + ":" + str(record.CHROM) + ":" + str(record.POS) + ":" + str(record.REF) + ":" + str(alt_base)
                snps_list.append(two_snps)
                chrom_pre = record.CHROM
                pos_pre = record.POS
                ref_pre = record.REF
                alt_pre = record.ALT
            else:
                chrom_pre = record.CHROM
                pos_pre = record.POS
                ref_pre = record.REF
                alt_pre = record.ALT
    return snps_list

def validate_2_snp(bam_file, chrom, snp1_pos, snp1_ref, snp1_alt, snp2_pos, snp2_ref, snp2_alt, threshold_value):
    samfile = pysam.AlignmentFile(bam_file, "rb")
    forward_NN = 0
    forward_NM = 0
    forward_MN = 0
    forward_MM = 0
    forward_OT = 0
    reverse_NN = 0
    reverse_NM = 0
    reverse_MN = 0
    reverse_MM = 0
    reverse_OT = 0
    iter = samfile.fetch(chrom, snp1_pos-1, snp2_pos)
    for x in iter:
        if x.reference_end == snp1_pos or x.reference_start + 1 == snp2_pos:
            pass
        else:
            query_sequence = x.query_sequence
            aligned_pairs = x.get_aligned_pairs(matches_only=False, with_seq=False)
            read_index1 = "";
            read_index2 = "";
            for t in aligned_pairs:
                if (t[1] == snp1_pos - 1):
                    read_index1 = t[0]
                if (t[1] == snp2_pos - 1):
                    read_index2 = t[0]
            if x.is_reverse:
                if read_index1 != "None" and read_index2 != "None":
                    two_bases = query_sequence[read_index1] + query_sequence[read_index2]
                    if two_bases == snp1_ref + snp2_ref:
                        reverse_NN = reverse_NN + 1
                    elif two_bases == snp1_ref + snp2_alt:
                        reverse_NM = reverse_NM + 1
                    elif two_bases == snp1_alt + snp2_ref:
                        reverse_MN = reverse_MN + 1
                    elif two_bases == snp1_alt + snp2_alt:
                        reverse_MM = reverse_MM + 1
                    else:
                        reverse_OT = reverse_OT + 1
                else:
                    reverse_OT = reverse_OT + 1
            else:
                if read_index1 != "None" and read_index2 != "None":
                    two_bases = query_sequence[read_index1] + query_sequence[read_index2]
                    if two_bases == snp1_ref + snp2_ref:
                        forward_NN = forward_NN + 1
                    elif two_bases == snp1_ref + snp2_alt:
                        forward_NM = forward_NM + 1
                    elif two_bases == snp1_alt + snp2_ref:
                                        #print (two_bases)
                        forward_MN = forward_MN + 1
                    elif two_bases == snp1_alt + snp2_alt:
                        forward_MM = forward_MM + 1
                    else:
                        forward_OT = forward_OT + 1
                else:
                    forward_OT = forward_OT + 1
    dnp_read_num = forward_NN + forward_MM + reverse_NN + reverse_MM
    total_read_num = forward_NN + forward_NM + forward_MN + forward_MM + forward_OT + reverse_NN + reverse_NM + reverse_MN + reverse_MM + reverse_OT
    if dnp_read_num/total_read_num > threshold_value:
        dnp = str(chrom) + ":" + str(snp1_pos) + ":" + str(snp2_pos)
        return dnp
    else:
        return

def combine_2_snp(dnp_list, vcf_file, output_file):
    snp1_chrom=""
    snp1_pos=""
    snp1_id=""
    snp1_ref=""
    snp1_alt=""
    snp1_qual=""
    snp1_filter=""
    snp1_info=""
    snp2_ref=""
    snp2_alt=""
    snp2_set_value=""
    flag = ""
    with open(vcf_file, 'r', encoding = 'utf-8') as vcf_file:
        vcf_content = vcf_file.readlines()
    with open(output_file, 'w', encoding = 'utf-8') as combined_vcf_file:
        for line in vcf_content:
            if re.match("#", line):
                combined_vcf_file.write(line)
            else:
                line = line.rstrip()
                snp_info = re.split("\t", line)
                for dnps in dnp_list:
                    dnp_info = re.split(":", dnps)
                    if snp_info[0] == dnp_info[0] and snp_info[1] == dnp_info[1]:
                        snp1_chrom = snp_info[0]
                        snp1_pos = snp_info[1]
                        snp1_id = snp_info[2]
                        snp1_ref = snp_info[3]
                        snp1_alt = snp_info[4]
                        snp1_qual = snp_info[5]
                        snp1_filter = snp_info[6]
                        snp1_info = snp_info[7]
                        flag = "dnp1"
                        break
                    elif snp_info[0] == dnp_info[0] and snp_info[1] == dnp_info[2]:
                        snp2_ref = snp_info[3]
                        snp2_alt = snp_info[4]
                        snp2_info_list = re.split(";", snp_info[7])
                        snp2_set = snp2_info_list[-1]
                        snp2_set_list = re.split("=", snp2_set)
                        snp2_set_value = snp2_set_list[-1]
                        flag = "dnp2"
                        break
                    else:
                        flag = "snp"
                if flag == "snp":
                    combined_vcf_file.write(line)
                    combined_vcf_file.write("\n")
                    flag = ""
                if flag == "dnp2":
                    combined_vcf_file.write(snp1_chrom)
                    combined_vcf_file.write("\t")
                    combined_vcf_file.write(snp1_pos)
                    combined_vcf_file.write("\t")
                    combined_vcf_file.write(snp1_id)
                    combined_vcf_file.write("\t")
                    combined_vcf_file.write(snp1_ref)
                    combined_vcf_file.write(snp2_ref)
                    combined_vcf_file.write("\t")
                    combined_vcf_file.write(snp1_alt)
                    combined_vcf_file.write(snp2_alt)
                    combined_vcf_file.write("\t")
                    combined_vcf_file.write(snp1_qual)
                    combined_vcf_file.write("\t")
                    combined_vcf_file.write(snp1_filter)
                    combined_vcf_file.write("\t")
                    combined_vcf_file.write(snp1_info)
                    combined_vcf_file.write(",")
                    combined_vcf_file.write(snp2_set_value)
                    combined_vcf_file.write("\t")
                    combined_vcf_file.write(".")
                    combined_vcf_file.write("\t")
                    combined_vcf_file.write(".")
                    combined_vcf_file.write("\t")
                    combined_vcf_file.write(".")
                    combined_vcf_file.write("\n")
                    snp1_chrom=""
                    snp1_pos=""
                    snp1_id=""
                    snp1_ref=""
                    snp1_alt=""
                    snp1_qual=""
                    snp1_filter=""
                    snp1_info=""
                    snp2_ref=""
                    snp2_alt=""
                    snp2_set_value=""
                    flag = ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect DNP from a vcf file")
    parser.add_argument("-i", "--input", type=str, dest="vcf_file", help="input vcf file name")
    parser.add_argument("-b", "--bam", type=str, dest="bam_file", help="input bam file name")
    parser.add_argument("-t", "--threshold", type=float, dest="threshold_value", default=0.5, help="set threshold value for validating DNP")
    parser.add_argument("-o", "--output", type=str, dest="output_file", help="output file name")
    args = parser.parse_args()
    snps_list = search_2_snp(args.vcf_file)
    if len(snps_list) == 0:
        print("There is no DNP searched in the input VCF file")
    else:
        dnps_list = list()
        for element in snps_list:
            snp_info = re.split(":", element)
            dnp = validate_2_snp(args.bam_file, snp_info[0], int(snp_info[1]), snp_info[2], snp_info[3], int(snp_info[5]), snp_info[6], snp_info[7], args.threshold_value)
            if dnp != None:
                dnps_list.append(dnp)
        if len(dnps_list) == 0:
            print("There is no validated DNP in the input VCF file")
        else:
            combine_2_snp(dnps_list, args.vcf_file, args.output_file)
