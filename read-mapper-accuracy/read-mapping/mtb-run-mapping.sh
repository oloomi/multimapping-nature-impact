#!/bin/bash
# After synthetic reads are generated by RNFtools, run the mapping tool with 
# different options (best-match and report-all)

# Build index out of reference genome
bowtie2-build /home/mohammad/datasets/bacteria/Mycobacterium_tuberculosis_H37Rv_uid57777/NC_000962.fna mtb

# Run Bowtie2 for mapping reads

# Paired mapping, best-match
bowtie2 -x mtb -X 650 -1 mtb_reads.1.fq -2 mtb_reads.2.fq -S mtb-paired-mapping-best-match.sam 2> log-mtb-paired-mapping-best-match.txt
samtools view -bS mtb-paired-mapping-best-match.sam > mtb-paired-mapping-best-match.bam

# Paired mapping, report-all
bowtie2 -a -x mtb -X 650 -1 mtb_reads.1.fq -2 mtb_reads.2.fq -S mtb-paired-mapping-report-all.sam 2> log-mtb-paired-mapping-report-all.txt
samtools view -bS mtb-paired-mapping-report-all.sam > mtb-paired-mapping-report-all.bam

# Single mapping, best-match
bowtie2 -x mtb -X 650 -U mtb_reads.1.fq,mtb_reads.2.fq -S mtb-single-mapping-best-match.sam 2> log-mtb-single-mapping-best-match.txt
samtools view -bS mtb-single-mapping-best-match.sam > mtb-single-mapping-best-match.bam

# Single mapping, report-all
bowtie2 -a -x mtb -X 650 -U mtb_reads.1.fq,mtb_reads.2.fq -S mtb-single-mapping-report-all.sam 2> log-mtb-single-mapping-best-match.txt
samtools view -bS mtb-single-mapping-report-all.sam > mtb-single-mapping-report-all.bam

echo "\n=== Done ===\n"
