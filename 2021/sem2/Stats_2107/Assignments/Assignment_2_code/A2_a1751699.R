library(tidyverse)
library(reshape2)

proportion_ss <- function(alpha, p, delta){
  z_a <- qnorm(1-(alpha))
  n <- ((z_a)^2*(p*(1-p)))/delta^2 # sample size n
  return(ceiling(n))
}

## b) Return the sample size n required to find a population proportion p 
#     with given alpha=0.05, p=0.2 and delta=0.1
proportion_ss(0.05/2,0.2,0.1)

## c) plot the required sample size n (Y-axis) against the population proportion that ranges
#  from 10% to 90% at 5% increment.
## d) produce the same plot as c) but with different measure of delta such as [delta = 5%, 8% and 10%].
proportion_vector <- 0
n_vector_D10 <- 0

# vectors that store sample size n for delta 5% and 10%
n_vector_D5 <- 0
n_vector_D8 <- 0

# i) 16*5% = 80% , so we loop the addition of 5% to the initial population proportion p of 10% 16 times 
#    until it goes to a total of 90% and store it in the proportion_vector. 
#    Then, use the 16 different proportion values to calculate the require sample size n for each different 
#    measure of delta and store the results into the respective n_vectors_D10, n_vectors_D5 and n_vectors_D10
for(i in 1:16){
  proportion_vector[i] <- 0.1+(0.05*i)
  n_vector_D10[i] <- proportion_ss(0.05/2, proportion_vector[i], 0.1)
  n_vector_D8[i] <- proportion_ss(0.05/2, proportion_vector[i], 0.08)
  n_vector_D5[i] <- proportion_ss(0.05/2, proportion_vector[i], 0.05)
}

## Answers for c)
# turn both proportion_vector and n_vector into a tibble data frame
d_tibble <- tibble(sample_size = n_vector_D10, proportion = proportion_vector) 

# construct the plot x-axis=proportions and y-axis=sample size
ggplot(d_tibble, aes(x=proportion, y=sample_size)) + geom_line(colour = "orange") + geom_point() + labs(x="proportion p", y="Sample size n") 

# iii) Return the required sample size n to find a population proportion p with given 
#      alpha=0.05, p=0.6 and delta=0.1
filter(d_tibble, d_tibble$proportion == 0.6)

## Answers for d)
d_tibble_2 <- tibble(proportion = proportion_vector, sample_size_D5 = n_vector_D5, sample_size_D8 = n_vector_D8, sample_size_D10 = n_vector_D10)

# Convert the wide d_tibble_2 data frame into a long data frame format for efficient plotting
long_d_tibble_2 <- d_tibble_2 %>%
  gather(n, sample_size_value, sample_size_D5:sample_size_D10)

# construct the plot 
ggplot(long_d_tibble_2, aes(x = proportion, y = sample_size_value, col = n)) + geom_line() + geom_point() + labs(x="proportion p", y="Sample size n", colour="Sample Size for each delta")
 
# iii) Return the required sample size n to find a population proportion p with given
#      alpha=0.05, p=0.5 and delta=0.07.
proportion_ss(0.05/2,0.5,0.07)

## Answers for e)
margin_err <- function(alpha, p, n){
  z_a <- qnorm(1-(alpha))
  delta = sqrt((z_a^2*(p*(1-p)))/n) # margin of error
  return(round(delta, digits=2))
}

# i) find the margin of error(delta) for a population with given sample size n=100, 
#    p=0.5 and alpha=0.05
margin_err(0.05/2,0.5,100)

# ii) find the proportion of a population with given delta=0.08, alpha=0.05 and n=100
# construct the root function 
quad_Roots <- function(a,b,c){
  roots <- c((-b+(b^2-(4*a*c))^(1/2))/(2*a), (-b-(b^2-(4*a*c))^(1/2))/(2*a))
  return(round(roots, digits=2))
}

p <- function(alpha, n, delta){
  z_a <- qnorm(1-(alpha))
  c <- (n*delta^2)/z_a^2
  result <- quad_Roots(-1,1,-c)
  return(result)
}

p(0.05/2,100,0.08)








