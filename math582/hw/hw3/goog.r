# Christian Drappi
# Math 582 with Prof. Arlie Petters
# Homework #3, due Monday, Feb. 17, 2014





# Answers:

# Problem (a): P(S(2/10/2014) > S(2/7/2014)) = 0.5649

# Problem (b): P(1190 < S(2/14/2014) < 1200) = 0.0919

# Problem (c): P(1073.99 < S(3/7/2014) < 1435.08) = 0.9545






# I programmed this assignment in R.
# Below is all of the code

#### Load and prepare data
goog <- read.csv("Dropbox/workspace/math582/hw3/goog.csv")

# number of days in a year
t.day <- 1/252
# how many days of data will we analyze
num.days <- 121

# get the adjusted closing prices
adj.close <- rev(goog$Adj.Close[1:num.days])

# compute the log returns of these prices
log.returns <- diff(log(adj.close))

# get mu_(m) and sigma of the security
mu.m <- 1/t.day * mean(log.returns)
sigma <- sqrt(1/t.day * var(log.returns))









#### Problem (a):
# Determine the probability that Google’s 
# closing price on February 10, 2014
# is above the aforementioned current price. 
# Compare your answer with the
# actual closing price.

#### Answer (a)

# the amount of trading days until 2/10/2014
time.1 <- 1

# Google's closing price will be above the
# current price in three days 
# iff S(1/252) / S(0) > 1
# iff ln(S(1/252)-S(0)) > 0.
# The probability of this happening is
# one minus the value of the normal cdf at 0
# with mean = mu_(m) * t and sdev = sigma * sqrt(t)
# (since the normal cdf gives the probability of 
# finishing below the current price)

prob.1 <- 1 - pnorm(0, mu.m * time.1 * t.day, sigma * sqrt(time.1*t.day))
p.1 <- round(prob.1, digits = 4)
# 0.6131594
print(paste("Problem (a): ", "P(S(2/10/2014) > S(2/7/2014)) = ", p.1, sep=""))






















#### Problem (b):
# Determine the probability that Google’s 
# closing price on Valentine’s Day,
# February 14, 2014, will be between 
# $1,190 and $1,200?

#### Answer (b)

# the amount of trading days until 2/14/2014
time.2 <- 5

# get the current price
feb.7.price <- adj.close[121]
# set the price bounds for the 
# probability calculation
bottom.price <- 1190
top.price <- 1200

# compute the size of log returns that 
# correspond to the prices
bottom.logr <- log(bottom.price/feb.7.price)
top.logr <- log(top.price/feb.7.price)

bottom.q <- pnorm(bottom.logr, mu.m * time.2*t.day, sigma * sqrt(time.2*t.day))
top.q <- pnorm(top.logr, mu.m * time.2*t.day, sigma * sqrt(time.2*t.day))
prob.2 <- top.q - bottom.q
p.2 <- round(prob.2, digits = 4)
print(paste("Problem (b): ", "P(1190 < S(2/14/2014) < 1200) = ", p.2, sep=""))



















#### Problem (c):
# Find a 95.45% conﬁdence interval for
# Google’s closing price on March 7, 2014.


#### Answer (c)

# the amount of trading days until 3/7/2014
time.3 <- 20

conf <- 0.9545
bottom.conf <- (1-conf)/2
top.conf <- 1-bottom.conf

bottom.interval <- feb.7.price*exp(qnorm(bottom.conf, mu.m * time.3*t.day, sigma * sqrt(time.3*t.day)))
top.interval <- feb.7.price*exp(qnorm(top.conf, mu.m * time.3*t.day, sigma * sqrt(time.3*t.day)))

b.i <- round(bottom.interval, digits = 2)
t.i <- round(top.interval, digits = 2)

print(paste("Problem (c): ", "P(", b.i, " < S(3/7/2014) < ", t.i, ") = ", conf, sep=""))








