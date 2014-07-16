library(ggplot2)

sp.500 <- read.csv("Dropbox/workspace/math582/SP500.csv")

# how many years of data will we analyze
num.years <- 56

returns <- as.numeric(sp.500$VALUE)

# compute the log returns of these prices
log.returns <- diff(log(returns))

# get mu_(m) and sigma of the security
mu.m <- mean(log.returns)
sigma <- sqrt(var(log.returns))

std.returns <- (log.returns-mu.m)/sigma
df <- data.frame(std.returns)
colnames(df) <- "returns"

p0 <- ggplot(df, aes(x=returns)) + geom_histogram(aes(y=..density..), binwidth=0.05) +
  geom_line(aes(y = ..density.., colour = 'Empirical Data'), stat = 'density') +  
  stat_function(fun = dnorm, aes(colour = 'Normal Distribution')) +                       
  #geom_histogram(aes(y = ..density..), alpha = 0.4) +                        
  scale_colour_manual(name = 'Density', values = c('black', 'red')) + 
  opts(legend.position = c(0.20, 0.85)) + xlab("Standardized Log Returns") +
  ylab("Probability Density") + labs(title="S&P 500 returns, 1957-2013")

pdf("Dropbox/workspace/math582/SP500.pdf")
plot(p0)
dev.off()