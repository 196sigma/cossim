## predict-runtime.R
rm(list=ls())

## key parameters
total.sections <- 14254*5/3

## Fill data
nsections <- c(10,100,200,300, 1000,14254)
npairs <- c(24,2360,9460, 21944, 246744,44007365)
runtimes <- c(.12,10.74, 43.11, 126.74, 2910.89,NA)
X <- data.frame(nsections, npairs, runtimes)
plot(X$nsections, X$npairs)
points(X$nsections, X$npairs, type='l')

## predict number of pairs as a function of number of sections
summary(m1 <- lm(npairs ~ -1 + nsections + I(nsections**2), data=X))
predicted.pairs <- m1$coeff[["nsections"]]*total.sections + m1$coeff[["I(nsections^2)"]]*(total.sections**2)

## predict runtime as a function of number of pairs
plot(X$nsections, X$runtimes)
points(X$nsections, X$runtimes, type='l')

plot(X$npairs, X$runtimes)
points(X$npairs, X$runtimes, type='l')

summary(m2 <- lm(runtimes ~ npairs, data=X))
predicted.runtime <- m2$coeff[["(Intercept)"]] + m2$coeff[["npairs"]]*predicted.pairs
(predicted.runtime/(60*60*24))
## predict memory requirements (Mb)
predicted.memory <- predicted.pairs*(15.8+17.4)/246744
