library(tidyverse)
library(readr)
crop <- read_csv("crop.csv")

#a) - Scatterplot of height of the crop vs Salinity of the Soil by different crops type. 
crop$Type <- as.factor(crop$Type)
crop %>%
  ggplot(aes(Salinity, Height, col = Type)) + geom_point()

#b) - Fit All three ANCOVA models
library(modelr)
# Model 1 - identical regression : Height vs Salinity
Model_1 <- lm(Height ~ Salinity, data = crop)
summary(Model_1)

# Model 2 - parallel regression : Height on Type vs Salinity
Model_2 <- lm(Height ~ Salinity + Type, data = crop)
summary(Model_2)

## This is what we want --
# Model 3 - separate regression : Height on Type vs Salinity with Interaction
Model_3 <- lm(Height ~ Salinity + Salinity*Type, data = crop)
summary(Model_3)
#c) Test for statistical significance 
anova(Model_3)

#d) Calculate BIC for Model 1, Model 2 & Model 3.
BIC(Model_1, Model_2, Model_3)

#e) Assess the assumptions for Model 3 (Separate Regression Lines)
plot(Model_3, which=1) # Residuals vs Fitted plot
plot(Model_3, which=2) # QQ plot
plot(Model_3, which=3) # Scale location plot

#f) Calculate the estimated difference in mean height between Type 2 and Type 3 crops & Calculate the 95% CI 
#   Employ Contrast - useful for comparing different group means
library(emmeans)
Model_3_em <- emmeans(Model_3, "Type")
summary(Model_3_em)
tyep_2_vs_Type_3_em <- contrast(Model_3_em, method=list("Type 2 vs Type 3"=c(0,1,-1)))
tyep_2_vs_Type_3_em
confint(tyep_2_vs_Type_3_em) # 95% CI


