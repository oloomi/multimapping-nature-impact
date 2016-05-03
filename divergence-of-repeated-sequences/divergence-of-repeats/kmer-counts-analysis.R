#install.packages("ggplot2")
library(ggplot2)
library(grid)
library(gridExtra)

theme_set(theme_gray(base_size = 20))

#-----------------------------------------------------------------------------
# Drawing histogram of number of k-mers that have no hamming distance d neighbours for MTB and OT

mtb.counts.table <-  read.table("kmer-count-mtb-k-27.txt", sep = " ")
mtb.counts.table.df <- rbind(data.frame(Distance = "Hamming 0", count = mtb.counts.table$V1),
                        data.frame(Distance = "Hamming 1", count = mtb.counts.table$V2),
                        data.frame(Distance = "Hamming 2", count = mtb.counts.table$V3))

tsutsu.counts.table <-  read.table("kmer-count-tsutsugamushi-k-27.txt", sep = " ")
tsutsu.counts.table.df <- rbind(data.frame(Distance = "Hamming 0", count = tsutsu.counts.table$V1),
                         data.frame(Distance = "Hamming 1", count = tsutsu.counts.table$V2),
                         data.frame(Distance = "Hamming 2", count = tsutsu.counts.table$V3))

mtb.counts.table.df$Organism = "MTB"
tsutsu.counts.table.df$Organism = "OT"
mtb.ot = rbind(mtb.counts.table.df, tsutsu.counts.table.df)

mtb.ot.hist <- ggplot(mtb.ot, aes(x = count, fill = Distance)) + 
  geom_histogram(position = "dodge", binwidth = 1, origin = 0) + 
  scale_fill_manual(values = c("firebrick1", "royalblue2", "seagreen3")) + 
  xlab("Multiplicity (number of neighbours with given Hamming distance)") + 
  ylab("Frequency (number of distinct k-mers)") + 
  theme(axis.text.x=element_text(size=12)) + theme(axis.text.y=element_text(size=12)) + 
  scale_y_log10() + coord_cartesian(ylim=c(1, 1e07)) + 
  facet_grid(Organism ~ .)
print(mtb.ot.hist)
ggsave(mtb.ot.hist, file="hamming-kmer-count-k-27-mtb-ot.pdf")

#-------------------- Statistics --------------------
nrow(mtb.counts.table)
colSums(mtb.counts.table)
sum(mtb.counts.table)

nrow(tsutsu.counts.table)
colSums(tsutsu.counts.table)
sum(tsutsu.counts.table)

#-----------------------------------------------------------------------------
# Number of distinct k-mers for different k's (k from 5 to 50) for MTb and OT
distinct.kmers.mtb <- read.table("distinct-kmers-k-5-50-mtb.txt", sep = " ")
distinct.kmers.tsutsu <- read.table("distinct-kmers-k-5-50-tsutsugamushi.txt", sep = "\t")

distinct.kmers = data.frame(k = distinct.kmers.mtb$V1, h0.mtb = distinct.kmers.mtb$V2, h1.mtb = distinct.kmers.mtb$V3,
                            h0.tsutsu = distinct.kmers.tsutsu$V2, h1.tsutsu = distinct.kmers.tsutsu$V3)

distinct.plot <- ggplot(distinct.kmers, aes(k, y = value, color = Distance, label = k)) + 
  geom_line(aes(y = h0.mtb, col = "MTB-Hamming 0")) + 
  geom_line(aes(y = h1.mtb, col = "MTB-Hamming 1")) + 
  geom_line(aes(y = h0.tsutsu, col = "OT-Hamming 0")) + 
  geom_line(aes(y = h1.tsutsu, col = "OT-Hamming 1")) + 
  geom_point(aes(y = h0.mtb, col = "MTB-Hamming 0")) + 
  geom_point(aes(y = h1.mtb, col = "MTB-Hamming 1")) + 
  geom_point(aes(y = h0.tsutsu, col = "OT-Hamming 0")) + 
  geom_point(aes(y = h1.tsutsu, col = "OT-Hamming 1")) + 
  xlab("K (k-mer length)") + ylab("Number of distinct k-mers") +   
  scale_y_log10()

print(distinct.plot)
ggsave(distinct.plot, file="distinct-kmers-mtb-tsutsugamushi.pdf")


#-----------------------------------------------------------------------------
# Plotting the histogram for the Mummer exact repeat results
exact.repeats.table <-  read.table("long-repeats-rc-25-counts.txt", sep = " ")
repeat.hist <- ggplot(exact.repeats.table, aes(x = V1, fill = ..count..)) + 
  geom_histogram(position = "dodge", binwidth = 10, origin = 25) + 
  xlab("Repeat length") + ylab("Frequency in the genome") +
  scale_fill_gradient("") + 
  scale_y_log10()

print(repeat.hist)
