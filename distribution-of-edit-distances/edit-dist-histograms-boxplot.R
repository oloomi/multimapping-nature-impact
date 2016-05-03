library(ggplot2)

# Background distribution
bg.df = data.frame(dist = 0, freq = 0, ref = "")
con <- file("edit-distance-merged-bg.txt", "r")
in.file  = readLines(con)
for(line in in.file) {
  line.splt = strsplit(line, " ")
  line.splt = as.integer(line.splt[[1]])
  bg.df <- rbind(bg.df, data.frame(dist = line.splt[1], freq = line.splt[-1], ref = "Background"))  
}
close(con)
bg.df = bg.df[-1, ]

# MTB Genome distribution
mtb.genome.df = data.frame(dist = 0, freq = 0, ref = "")
con <- file("edit-distance-merged-mtb.txt", "r")
in.file  = readLines(con)
for(line in in.file) {
  line.splt = strsplit(line, " ")
  line.splt = as.integer(line.splt[[1]])
  mtb.genome.df <- rbind(mtb.genome.df, data.frame(dist = line.splt[1], freq = line.splt[-1], ref = "MTB"))  
}
close(con)
mtb.genome.df = mtb.genome.df[-1, ]

# Orientia Tsutsugamushi Genome distribution
ot.genome.df = data.frame(dist = 0, freq = 0, ref = "")
con <- file("edit-distance-merged-tsutsu.txt", "r")
in.file  = readLines(con)
for(line in in.file) {
  line.splt = strsplit(line, " ")
  line.splt = as.integer(line.splt[[1]])
  ot.genome.df <- rbind(ot.genome.df, data.frame(dist = line.splt[1], freq = line.splt[-1], ref = "OT"))  
}
close(con)
ot.genome.df = ot.genome.df[-1, ]

bg.genome.df = rbind(mtb.genome.df, ot.genome.df, bg.df)

# Finding the edit distance that has the maximum frequency

mtb.mean.dist = weighted.mean(mtb.genome.df$dist, mtb.genome.df$freq)
ot.mean.dist = weighted.mean(ot.genome.df$dist, ot.genome.df$freq)
bg.mean.dist = weighted.mean(bg.df$dist, bg.df$freq)

# To display different lines in different facets, we need to create a dataframe
# vline.data <- data.frame(z = c(mtb.mean.dist, ot.mean.dist, bg.mean.dist), 
#                          ref = c("Mycobacterium Tuberculosis", "Orientia Tsutsugamushi", "Background distribution"))
vline.data <- data.frame(z = c(mtb.mean.dist, ot.mean.dist, bg.mean.dist), 
                         ref = c("MTB", "OT", "Background"))

theme_set(theme_gray(base_size = 20))

boxplot.hist <- ggplot(bg.genome.df, aes(factor(dist), freq)) +   
  geom_boxplot(outlier.colour = "black", outlier.size = 0.5, fill = "firebrick1") + 
  scale_x_discrete(breaks=seq(0,80,5)) + 
  scale_y_log10() + 
  xlab("Levenshtein distance") + 
  ylab("Frequency") + 
  facet_grid(ref ~ .) + 
  geom_vline(aes(xintercept = z), vline.data, , linetype="dashed")
print(boxplot.hist)

ggsave(boxplot.hist, file="edit-distance-boxplot-dist-mtb-ot-background.pdf")
