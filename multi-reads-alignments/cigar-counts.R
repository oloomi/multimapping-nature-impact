library('ggplot2')

mtb.cigar.percentages = read.table("cigar-counts-percentage-hist-mtb-h37rv-single.txt")
ot.cigar.percentages = read.table("cigar-counts-percentage-hist-ot-ikeda-single.txt")

mtb.cigar.percentages$Organism = "Mycobacterium Tuberculosis"
ot.cigar.percentages$Organism = "Orientia Tsutsugamushi"

both.cigar.percentages = rbind(mtb.cigar.percentages, ot.cigar.percentages)
colnames(both.cigar.percentages) = c("Percentage", "Organism")

percentages.hist <- ggplot(both.cigar.percentages, aes(x = Percentage, fill = Organism)) + 
  geom_histogram(position = "dodge", binwidth = 10, origin = 0) + 
  scale_fill_manual(values = c("royalblue2", "firebrick1")) + 
  scale_x_continuous(breaks=seq(0,100,10)) + 
  xlab("Percentage of number of mapping locations with different CIGAR's for a read") + 
  ylab("Frequency (number of reads that have a given percentage)") + 
  scale_y_log10()

print(percentages.hist)
ggsave(percentages.hist, file="mtb-ot-single-report-all-percentages-hist-ylog10.pdf")

percentages.hist <- ggplot(both.cigar.percentages, aes(x = Percentage, fill = Organism)) + 
  geom_histogram(position = "dodge", binwidth = 10, origin = 0) + 
  scale_fill_manual(values = c("royalblue2", "firebrick1")) + 
  scale_x_continuous(breaks=seq(0,100,10)) + 
  xlab("Percentage of number of mapping locations with different CIGAR's for a read") + 
  ylab("Frequency (number of reads that have a given percentage)")

print(percentages.hist)
ggsave(percentages.hist, file="mtb-ot-single-report-all-percentages-hist.pdf")
