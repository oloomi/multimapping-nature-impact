import time
import itertools
import sys

# Gets a DNA sequence as input and returns its reverse complement
def rev_comp(seq):
    seq_dict = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}
    return "".join([seq_dict[base] for base in reversed(seq)])

# Creates a hash table and counts k-mers for the reference sequence
# It then counts the number of hamming distance 1 and hamming distance 2 neighbours for each k-mer
# seq: the reference genome sequence string
# k: the k-mer length
def count_kmers(seq, genome_name, k):
    out_file = open("kmer-count-{}-k-{}.txt".format(genome_name, k), "w")
    kmer_dict = {}
    for i in range(len(seq) - k + 1):
        if seq[i:i + k] in kmer_dict:
            kmer_dict[seq[i:i + k]][0] += 1
            kmer_dict[rev_comp(seq[i:i + k])][0] += 1
        else:
            kmer_dict[seq[i:i + k]] = [0] * 3
            kmer_dict[rev_comp(seq[i:i + k])] = [0] * 3

    # For progress bar
    full_progress = len(kmer_dict)
    current_progress = 0

    for key_kmer in kmer_dict:
        # Counting hamming distance 1 neighbors for each distinct k-mer
        neighbor_count = 0
        for j in range(k):
            # kmer_str = seq[i:i+k] with one mismatch
            for base_iter, base in enumerate(['A', 'T', 'C', 'G']):
                if key_kmer[j] != base:
                    # kmer_str = first part + mismatch + second part
                    kmer_str = key_kmer[ : j] + base + key_kmer[j + 1 : ]
                    if kmer_str in kmer_dict:
                        # Add its positions in genome to the locations list (Update: increment the count)
                        neighbor_count += (kmer_dict[kmer_str][0] + 1)
        kmer_dict[key_kmer][1] = neighbor_count

        # Counting hamming distance 2 neighbors for each distinct k-mer
        neighbor_count = 0
        for pos_tuple in itertools.combinations(range(k), 2):
            for base_tuple in itertools.product(["A", "C", "T", "G"], repeat=2):
                if (key_kmer[pos_tuple[0]] != base_tuple[0]) & (key_kmer[pos_tuple[1]] != base_tuple[1]):
                    # kmer_str: the k-mer with two mismatches
                    kmer_str = key_kmer[:pos_tuple[0]] + base_tuple[0] + key_kmer[(pos_tuple[0] + 1): pos_tuple[1]]\
                                   + base_tuple[1] + key_kmer[(pos_tuple[1] + 1):]
                    if kmer_str in kmer_dict:
                        neighbor_count += (kmer_dict[kmer_str][0] + 1)
        kmer_dict[key_kmer][2] = neighbor_count
        out_file.write(" ".join(repr(e) for e in kmer_dict[key_kmer]) + "\n")

        current_progress += 1
        sys.stdout.write("\r" + str(round((current_progress / full_progress), 4) * 100) + "%")
        sys.stdout.flush()

    out_file.close()
    return kmer_dict


# Creates a hash table and counts number of distinct k-mers for the reference sequence
# It then counts the number of hamming distance 1 neighbours for each k-mer
# seq: the reference genome sequence string
# k: the k-mer length
def num_distinct_kmers(seq, k):
    kmer_dict = {}
    for i in range(len(seq) - k + 1):
        if seq[i:i + k] in kmer_dict:
            kmer_dict[seq[i:i + k]] += 1
            kmer_dict[rev_comp(seq[i:i + k])] += 1
        else:
            kmer_dict[seq[i:i + k]] = 0
            kmer_dict[rev_comp(seq[i:i + k])] = 0

    num_distinct = 0
    for key_kmer in kmer_dict:
        # Counting hamming distance 1 neighbors for each distinct k-mer
        neighbor_count = 0
        for j in range(k):
            # kmer_str = seq[i:i+k] with one mismatch
            for base_iter, base in enumerate(['A', 'T', 'C', 'G']):
                if key_kmer[j] != base:
                    # kmer_str = first part + mismatch + second part
                    kmer_str = key_kmer[ : j] + base + key_kmer[j + 1 : ]
                    if kmer_str in kmer_dict:
                        neighbor_count = 1
                        break
            if neighbor_count == 1:
                break
        if neighbor_count == 0:
            num_distinct += 1

    return (len(kmer_dict), num_distinct)

start_time = time.time()

input_file_path = "E:\\Datasets\\bacteria\\all.fna.tar\\Mycobacterium_tuberculosis_H37Rv_uid57777\\NC_000962.fna"
# input_file_path = "E:\\Datasets\\bacteria\\all.fna.tar\\Orientia_tsutsugamushi_Ikeda_uid58869\\NC_010793.fna"
input_file = open(input_file_path)
# Ignore the first line: the header line
file_lines = input_file.readlines()[1:]
# Join all sequence lines and remove new line characters
dna_seq = "".join(file_lines)
dna_seq = dna_seq.replace("\n", "")
input_file.close()

# Counting hamming distance 0, 1 and 2 neighbours
count_kmers(dna_seq, "mtb", 27)
# count_kmers(dna_seq, "tsutsugamushi", 27)

print("\n" + "Run time: " + str(round(time.time() - start_time, 4)) + " seconds")
