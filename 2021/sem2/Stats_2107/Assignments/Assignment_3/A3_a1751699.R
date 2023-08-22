library(readr)
library(tidyverse)
library(infer)

Drill <- read_csv("Drill.csv")

##a) i) sample size n for each region
n_Antarctic <- filter(Drill, Drill$Region == "Antarctic") # 60
n_Pacific <- filter(Drill, Drill$Region == "Pacific") # 53

#ii) mean and standard deviation of drilling time(in hours) for drills in each region
mean_Antarctic <- mean(n_Antarctic$Time_hr)
sd_Antarctic <- sd(n_Antarctic$Time_hr)
mean_Pacific <- mean(n_Pacific$Time_hr)
sd_Pacific <- sd(n_Pacific$Time_hr)

#iii) which test is appropriate ? 
# Answer : A non-pooled two sample t-test because the ratio of max(sd_Antarctic, sd_Pacific)/min(sd_Antarctic, sd_Pacific) > 2

#iv) Perform a Welch t-test using R, assuming 5% significance level, to test the hypothesis.
t_test_Antarctic_Pacific <- t.test(Drill$Time_hr ~ Drill$Region, data = Drill, alternative = "greater")

## Conclusion: Since the p-value is greater than the significance level of 5%, there is insufficient evidence to reject the null hypothesis. 
##             Therefore, we can conclude that the drilling time of drills in the Pacific region is longer than those in the Antarctic region. 

##b) 
#i) A non-pooled 2 sample t-test (Welch t-test) between the mean drilling time of OzDrill(Antarctic) and AllDrill(Atlantic)
welch_t <- function(mu1, mu2, sd1, sd2, n1, n2){
  t_stat <- (mu1-mu2)/sqrt((sd1^2/n1)+(sd2^2/n2))
  welch_df <- ((sd1^2/n1)+(sd2^2/n2))^2/((sd1^4/(n1^2*(n1-1)))+(sd2^4/(n2^2*(n2-1))))
  p_val <- 1-pt(t_stat,welch_df)
  return(
    tibble(t_statistic = t_stat,
           DF = welch_df,
           P = p_val)
  )
}

t_test_Antarctic_Atlantic <- welch_t(mean_Antarctic, 25, sd_Antarctic, 2.14, 60, 38)

#ii) The value of test-statistic, degrees of freedom and P-value.
view(t_test_Antarctic_Atlantic)

#iii) Conclusion: Since the p-value is smaller than the significance level of 5%, we have sufficient evidence to reject the null hypothesis. 
#                 Therefore, we can conclude that the driling time of drills in the Atlantic region is shorter than those in the Antarctic region.

#iv) Density Plot for the t-distribution with degrees of freedom obtained in ii)
# find the boundary value for alpha 0.05 at the right tail of the t-distribution
boundary_val <- qt(1-0.05, t_test_Antarctic_Atlantic$DF)

ggplot(tibble(x = c(-4,4)), aes(x=x)) +
  geom_area(xlim=c(boundary_val,4), stat="function", fun=dt, args=list(df=t_test_Antarctic_Atlantic$DF),fill="#00998a") + 
  stat_function(fun=dt, args=list(df=t_test_Antarctic_Atlantic$DF)) + # creates the t-distribution density plot with DF=90.412..
  geom_vline(xintercept = t_test_Antarctic_Atlantic$t_statistic, linetype="dashed", color="red") + # this line indicates where the t-statistic lies
  labs(x = "T",title = "t-distribution(df=90.41287, alpha=0.05)") + 
  theme(plot.title =element_text(size=10, face="bold"), axis.title = element_text(size=rel(0.8))) # set the size and font for the title and axes' title


# Save the plot as 
ggsave("A3_a1751699.png")

