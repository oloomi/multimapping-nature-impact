__author__ = 'soloomi'

import time
import itertools
import sys

# Process FASTA file and return a single string DNA sequence
def process_fasta(input_file_path):
    input_file = open(input_file_path)
    # Ignore the first line: the header line
    file_lines = input_file.readlines()[1:]
    # Join all sequence lines and remove new line characters
    dna_seq = "".join(file_lines)
    dna_seq = dna_seq.replace("\n", "")
    input_file.close()
    return dna_seq


# Gets a DNA sequence as input and returns its reverse complement
def rev_comp(seq):
    seq_dict = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}
    return "".join([seq_dict[base] for base in reversed(seq)])

# Creates a hash table and counts k-mers for the reference sequence
# It then counts the number of hamming distance 1 and hamming distance 2 neighbours for each k-mer
# seq: the reference genome sequence string
# k: the k-mer length
def count_kmer_positions(seq, genome_name, k):
    out_file = open("kmer-positions-count-revcomp-{}-k-{}.txt".format(genome_name, k), "w")
    kmer_dict = {}
    for i in range(len(seq) - k + 1):
        if seq[i:i + k] in kmer_dict:
            kmer_dict[seq[i:i + k]][0] += 1
            kmer_dict[rev_comp(seq[i:i + k])][0] += 1
        else:
            kmer_dict[seq[i:i + k]] = [0] * 3
            kmer_dict[rev_comp(seq[i:i + k])] = [0] * 3

    # For progress bar
    full_progress = 2 * (len(seq) - k + 1)
    # Counters
    unique_kmers = 0
    hamming_0_kmers_count = 0
    hamming_1_kmers_count = 0
    hamming_2_kmers_count = 0

    for i in range(len(seq) - k + 1):
        key_kmer = seq[i:i + k]
        # hamming distance 0 neighbours
        # unique k-mers
        if kmer_dict[key_kmer][0] == 0:
            unique_kmers += 1
        else:
            hamming_0_kmers_count += 1
        # Counting hamming distance 1 neighbors for each k-mer
        neighbour_found = False
        for j in range(k):
            # kmer_str = seq[i:i+k] with one mismatch
            for base_iter, base in enumerate(['A', 'T', 'C', 'G']):
                if key_kmer[j] != base:
                    # kmer_str = first part + mismatch + second part
                    kmer_str = key_kmer[ : j] + base + key_kmer[j + 1 : ]
                    if kmer_str in kmer_dict:
                        # Add its positions in genome to the locations list (Update: increment the count)
                        hamming_1_kmers_count += 1
                        neighbour_found = True
                        break
            if neighbour_found:
                break

        # Counting hamming distance 2 neighbors for each distinct k-mer
        neighbour_found = False
        for pos_tuple in itertools.combinations(range(k), 2):
            for base_tuple in itertools.product(["A", "C", "T", "G"], repeat=2):
                if (key_kmer[pos_tuple[0]] != base_tuple[0]) & (key_kmer[pos_tuple[1]] != base_tuple[1]):
                    # kmer_str: the k-mer with two mismatches
                    kmer_str = key_kmer[:pos_tuple[0]] + base_tuple[0] + key_kmer[(pos_tuple[0] + 1): pos_tuple[1]]\
                                   + base_tuple[1] + key_kmer[(pos_tuple[1] + 1):]
                    if kmer_str in kmer_dict:
                        hamming_2_kmers_count += 1
                        neighbour_found = True
                        break
            if neighbour_found:
                break

        sys.stdout.write("\r{:.2f}%".format(i/full_progress))
        sys.stdout.flush()

    # ---- For reverse complement strand ----
    seq = rev_comp(seq)
    for i in range(len(seq) - k + 1):
        key_kmer = seq[i:i + k]
        # hamming distance 0 neighbours
        # unique k-mers
        if kmer_dict[key_kmer][0] == 0:
            unique_kmers += 1
        else:
            hamming_0_kmers_count += 1
        # Counting hamming distance 1 neighbors for each k-mer
        neighbour_found = False
        for j in range(k):
            # kmer_str = seq[i:i+k] with one mismatch
            for base_iter, base in enumerate(['A', 'T', 'C', 'G']):
                if key_kmer[j] != base:
                    # kmer_str = first part + mismatch + second part
                    kmer_str = key_kmer[ : j] + base + key_kmer[j + 1 : ]
                    if kmer_str in kmer_dict:
                        # Add its positions in genome to the locations list (Update: increment the count)
                        hamming_1_kmers_count += 1
                        neighbour_found = True
                        break
            if neighbour_found:
                break

        # Counting hamming distance 2 neighbors for each distinct k-mer
        neighbour_found = False
        for pos_tuple in itertools.combinations(range(k), 2):
            for base_tuple in itertools.product(["A", "C", "T", "G"], repeat=2):
                if (key_kmer[pos_tuple[0]] != base_tuple[0]) & (key_kmer[pos_tuple[1]] != base_tuple[1]):
                    # kmer_str: the k-mer with two mismatches
                    kmer_str = key_kmer[:pos_tuple[0]] + base_tuple[0] + key_kmer[(pos_tuple[0] + 1): pos_tuple[1]]\
                                   + base_tuple[1] + key_kmer[(pos_tuple[1] + 1):]
                    if kmer_str in kmer_dict:
                        hamming_2_kmers_count += 1
                        neighbour_found = True
                        break
            if neighbour_found:
                break

        sys.stdout.write("\r{:.2f}%".format(i /full_progress + 0.5))
        sys.stdout.flush()

    out_file.write("Distinct: {}\n".format(len(kmer_dict)))
    out_file.write("Unique: {}\n".format(unique_kmers))
    out_file.write("Hamming 0: {}\n".format(hamming_0_kmers_count))
    out_file.write("Hamming 1: {}\n".format(hamming_1_kmers_count))
    out_file.write("Hamming 2: {}\n".format(hamming_2_kmers_count))
    out_file.close()
    return kmer_dict

input_file_path = "E:\\Datasets\\bacteria\\all.fna.tar\\Mycobacterium_tuberculosis_H37Rv_uid57777\\NC_000962.fna"
dna_seq = process_fasta(input_file_path)
count_kmer_positions(dna_seq, "mtb", 27)

input_file_path = "E:\\Datasets\\bacteria\\all.fna.tar\\Orientia_tsutsugamushi_Ikeda_uid58869\\NC_010793.fna"
dna_seq = process_fasta(input_file_path)
count_kmer_positions(dna_seq, "ot", 27)
