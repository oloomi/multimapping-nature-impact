library('ggplot2')
library('grid')

theme_set(theme_gray(base_size = 20))

# Plotting the histogram for Mummer exact repeats for MTB and OT
tsutsu.repeats <-  read.table("Orientia_tsutsugamushi_Ikeda_uid58869-repeats-rc-27.txt", sep = "", header = TRUE)
mtb.repeats <-  read.table("Mycobacterium_tuberculosis_H37Rv_uid57777-repeats-rc-27.txt", sep = "", header = TRUE)

ot.repeats <- subset(tsutsu.repeats, Length < 2000)
ot.long.repeats <- subset(tsutsu.repeats, Length >= 2000)
mtb.long.repeats <- subset(mtb.repeats, Length >= 2000)

# Repeats shorter than 2000 bps
repeats.df <- rbind(data.frame(Organism = "MTB", count = mtb.repeats$Length),
                    data.frame(Organism = "OT", count = ot.repeats$Length))

repeats.hist <- ggplot(repeats.df, aes(x = count, fill = Organism)) + 
  geom_histogram(position = "dodge", binwidth = 5, origin = min(repeats.df$count)) +  
  scale_fill_manual(values = c("royalblue2", "firebrick1")) +
  xlab("Repeat length") + ylab("Frequency (number of repeats with a certain length)") + 
  theme(axis.text.x=element_text(size=12)) + theme(axis.text.y=element_text(size=12)) + 
  scale_y_log10(breaks=c(1,10,100,1000,10000)) + coord_cartesian(ylim=c(1, 50000))

print(repeats.hist)

# Long repeats
long.repeats.df <- data.frame(Organism = "Orienta Tsutsugamushi", count = ot.long.repeats$Length)

long.repeats.hist <- ggplot(long.repeats.df, aes(x = count, fill = Organism)) + 
  geom_histogram(binwidth = 5, origin = min(long.repeats.df$count)) +  
  scale_fill_manual(values = c("firebrick1"), guide = FALSE) +
  theme(axis.text.x=element_text(size=12)) + theme(axis.text.y=element_text(size=12)) + 
  scale_x_continuous(breaks=c(2000,6000,10000)) + 
  xlab("Repeat length") + ylab("Frequency") 

print(long.repeats.hist)

# For making an inset
vp <- viewport(width = 0.4, height = 0.4, x = 0.64, y = 0.75)

full <- function() {
  print(repeats.hist)
  print(long.repeats.hist, vp = vp)
}

full()

ggsave(file="MTB-OT-repeats-rc-27-histogram.pdf")

