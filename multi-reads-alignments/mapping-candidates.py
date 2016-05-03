__author__ = 'soloomi'


def cigar_counts(sam_file_path, organism):
    from collections import defaultdict

    read_cigar_dict = defaultdict(lambda: defaultdict(int))

    sam_file = open(sam_file_path)
    for line in sam_file.readlines():
        if line[0] == "@":
            continue
        fields = line.rstrip("\n").split("\t")
        read_id = fields[0]
        cigar = fields[5]
        # how many times a cigar string is seen for each read
        read_cigar_dict[read_id][cigar] += 1

    cigar_counts_file = open("cigar-counts-{}.txt".format(organism), "w")
    counts_percentage_file = open("cigar-counts-percentage-{}.txt".format(organism), "w")
    counts_percentage_file_hist = open("cigar-counts-percentage-hist-{}.txt".format(organism), "w")
    # for each read
    for read_id, cigar_counts in read_cigar_dict.items():
        cigar_counts_str = ""
        counts_percentage_str = ""
        counts_sum = sum(cigar_counts.values())
        # for each cigar string (i.e. each of locations that a read is mapped)
        for cigar, count in cigar_counts.items():
            # the CIGAR string \tab how many mapping locations with that CIGAR
            cigar_counts_str += "{}\t{}\t".format(cigar, count)
            # percentage of the above count (without writing the cigar string to file)
            counts_percentage_str += "{}\t".format(int(100 * count / counts_sum))
            # this is specifically for using later on in R for plotting diagrams
            counts_percentage_file_hist.write("{}\n".format(int(100 * count / counts_sum)))
        cigar_counts_file.write(cigar_counts_str + "\n")
        counts_percentage_file.write(counts_percentage_str + "\n")

    cigar_counts_file.close()
    counts_percentage_file.close()
    counts_percentage_file_hist.close()
    sam_file.close()


def cigar_counts_stats(sam_file_path, organism):
    from collections import defaultdict

    read_cigar_dict = defaultdict(lambda: defaultdict(int))

    sam_file = open(sam_file_path)
    for line in sam_file.readlines():
        if line[0] == "@":
            continue
        fields = line.rstrip("\n").split("\t")
        read_id = fields[0]
        cigar = fields[5]
        # * means no alignment for a read
        if cigar != "*":
            # how many times a cigar string is seen for each read
            read_cigar_dict[read_id][cigar] += 1

    # total number of reads
    total_reads = len(read_cigar_dict)
    # number of reads that map only to one location
    unique_reads = 0
    # number of reads that map to different locations with the same alignment
    same_multi_reads = 0
    # number of reads that map to different locations with different alignments
    diff_multi_reads = 0

    # for each read
    for read_id, cigar_counts in read_cigar_dict.items():
        # if this read has only one CIGAR
        if len(cigar_counts) == 1:
            # if it has repeated only once, that's a read which maps only to one location
            if sum(cigar_counts.values()) == 1:
                unique_reads += 1
            # Otherwise, it maps to more than one location, but with the same alignment
            else:
                same_multi_reads += 1
        else:
            diff_multi_reads += 1

    cigar_counts_stats_file = open("stats-cigar-counts-{}.txt".format(organism), "w")
    cigar_counts_stats_file.write("#reads that map to only one location:\t{}\t{}\n".
                                  format(unique_reads, round(unique_reads/total_reads, 3)))
    cigar_counts_stats_file.write("#reads that map more than one location, with same CIGAR:\t{}\t{}\n".
                                  format(same_multi_reads, round(same_multi_reads/total_reads, 3)))
    cigar_counts_stats_file.write("#reads that map more than one location, with different CIGAR's:\t{}\t{}\n".
                                  format(diff_multi_reads, round(diff_multi_reads/total_reads, 3)))
    cigar_counts_stats_file.write("#all reads:\t{}\n".format(total_reads))

    cigar_counts_stats_file.close()
    sam_file.close()

# cigar_counts("head-mtb-mapping.sam", "mtb-test")
# cigar_counts("mtb-h37rv-simulated-single-report-all.sam", "mtb-h37rv-single")
# cigar_counts("o-tsutsugamushi-ikeda-simulated-single-report-all.sam", "ot-ikeda-single")

# cigar_counts_stats("head-mtb-mapping.sam", "mtb-test")
cigar_counts_stats("mtb-single-mapping-report-all.sam", "mtb-h37rv-single")
cigar_counts_stats("ot-single-mapping-report-all.sam", "ot-ikeda-single")
