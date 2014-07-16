library(e1071)
library(ggplot2)

# fb.r

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
fb <- read.csv("Dropbox/workspace/math582/fb.csv")

# number of days in a year
t.day <- 1/252
# how many days of data will we analyze
num.days <- nrow(fb)

# get the adjusted closing prices
adj.close <- rev(fb$Adj.Close)

# compute the log returns of these prices
log.returns <- diff(log(adj.close))

# get mu and sigma of the security
theta <- 1/t.day * mean(log.returns)
sdev <- sqrt(1/t.day * var(log.returns))

bsm.call <- function(S, tau, K, r, sigma) {
    d.1 <- 1/sigma*sqrt(tau) * (log(S/K) + (r+sigma^2 / 2)*tau)
    d.2 <- d.1 - sigma*sqrt(tau)
    pnorm(d.1) * S - pnorm(d.2) * K * exp(-r * tau)
}

K <- c(40, 50, 60, 70, 80)
current.price <- fb$Adj.Close[1]
time.to.exp <- 1 # one year
r <- theta # risk-free rate

bsm.call.prices <- bsm.call(current.price, time.to.exp, K, r, sdev)

A <- var(log.returns) / t.day
B <- moment(log.returns, order=3, center=TRUE)
nu <- 1/(2*theta^2) * (3*A + sqrt(9*A^2 - 4*B*theta))
sigma <- sqrt(A - theta^2 * nu)
sigma.2 <- sigma^2

mc <- 10000
num.days <- 252
t.day <- 1/num.days
# num.draws <- mc * num.days

X.values <- rep(0, mc)
for (i in 1:mc) {
    gamma.draws <- rgamma(num.days, shape=t.day/nu, rate=1/nu)
    norm.draws <- rnorm(num.days)
    gamma.part <- theta*sum(gamma.draws)
    vp <- sqrt(gamma.draws) * norm.draws
    variance.part <- sigma*sum(vp)
    X.values[i] <- gamma.part + variance.part
}

S.values <- current.price * exp(X.values)
opt.prices <- rep(NA, length(K))
for (i in 1:length(K)) {
    payoff.values <- rep(0, mc)
    for (j in 1:mc) {
        payoff.values[j] <- max(S.values[j] - K[i], 0)
    }
    mean.payoff <- mean(payoff.values)
    opt.prices[i] <- exp(-r * time.to.exp) * mean.payoff
}

vg <- data.frame(S.values)
colnames(vg) <- "Price"
vg$Model <- "VG"

bsm <- data.frame(current.price*exp(rnorm(mc, theta, sdev)))
colnames(bsm) <- "Price"
bsm$Model <- "BM"

apr.14.15 <- rbind(vg, bsm)

p0 <- ggplot(apr.14.15, aes(Price, fill=Model)) + geom_density(alpha=0.3)
p1 <- p0 + labs(title="Stock price at expiration \n under different models") + ylab("Probability density")

# pdf("Dropbox/workspace/math582/fb.pdf")
plot(p1)
# dev.off


