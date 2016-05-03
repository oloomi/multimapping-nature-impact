__author__ = 'soloomi'

import itertools
import random
import sys
import time


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # j+1 instead of j since previous_row and current_row are one character longer than s2
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def kmer_edit_distance(seq, k, sample_size):
    start_time = time.time()
    # getting file number extension from command line
    out_file = open("kmer-ref-edit-distance-{}.txt".format(sys.argv[1]), "w")
    log_file = open("log-kmer-ref-edit-distance-{}.txt".format(sys.argv[1]), "w")
    # the starting position in the genome for sample k-mers
    random.seed(sys.argv[1])
    sample_kmers = random.sample(range(len(seq) - k + 1), sample_size)
    log_file.write("Sample k-mer indices: \n" + str(sample_kmers) + "\n\n")
    log_file.flush()
    log_file.close()

    progress_bar = 1
    for kmer_pos in sample_kmers:
        print(progress_bar)
        progress_bar += 1
        # storing distance frequencies for histogram
        distance_dict = {}
        for ref_pos in range(len(seq) - k + 1):
            distance = levenshtein(seq[kmer_pos: kmer_pos + k], seq[ref_pos: ref_pos + k])            
            if distance in distance_dict:
                distance_dict[distance] += 1
            else:
                distance_dict[distance] = 1
                # print(ref_pos)
        # writing distance:frequency to file for each sample read in a separate line
        out_file.write(" ".join([str(e[0]) + ":" + str(e[1]) for e in distance_dict.items()]) + "\n")
        out_file.flush()
        print("Run time: " + str(round(time.time() - start_time, 4)) + " seconds")
    out_file.close()
    print("Done")

# input_file_path = "../Mycobacterium_tuberculosis_H37Rv_uid57777/NC_000962.fna"
input_file_path = "../Orientia_tsutsugamushi_Ikeda_uid58869/NC_010793.fna"
input_file = open(input_file_path)
# Ignore the first line: the header line
file_lines = input_file.readlines()[1:]
# Join all sequence lines and remove new line characters
dna_seq = "".join(file_lines)
dna_seq = dna_seq.replace("\n", "")
input_file.close()

kmer_edit_distance(seq=dna_seq, k=100, sample_size=25)
