__author__ = 'soloomi'

# import itertools

input_file_path = "kmer-ref-edit-distance-{0}.txt"
dist_freq_dict = {}
for file_num in range(1, 28):
    input_file = open(input_file_path.format(file_num))
    for line in input_file.readlines():
        line = line.rstrip("\n")
        dist_freq_lst = line.split(" ")
        for df in dist_freq_lst:
            dist_freq = df.split(":")
            distance = int(dist_freq[0])
            frequency = dist_freq[1]
            if distance in dist_freq_dict:
                dist_freq_dict[distance].append(frequency)
            else:
                dist_freq_dict[distance] = [frequency]
    input_file.close()

out_file = open("edit-distance-merged.txt", "w")
for dist in sorted(dist_freq_dict.keys()):
    print(dist, " ".join(dist_freq_dict[dist]))
    out_file.write(str(dist) + " " + " ".join(dist_freq_dict[dist]) + "\n")
out_file.close()
