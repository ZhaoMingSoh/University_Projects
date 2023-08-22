library(tidyverse)
library(readr)

survey2003_dirty <- read_csv("survey2003_dirty.csv")



#Q1 : ------------------ Clean the data --------------------

## Before I do anything else, ensure the each variable is under the correct class for their values.
lapply(survey2003_dirty, class) 
### Both height and weight were incorrectly classified, from character class --> numeric class
survey2003_dirty$height <- as.numeric(survey2003_dirty$height)
survey2003_dirty$weight <- as.numeric(survey2003_dirty$weight)

## A) Variable : favourite_genre
table(survey2003_dirty$favourite_genre)
### Since "prefer not to answer" is not a valid category in movies' genre, it is set to NA 
survey2003_dirty$favourite_genre[survey2003_dirty$favourite_genre == "prefer not to answer"] <- NA
table(survey2003_dirty$favourite_genre)
table(survey2003_dirty$favourite_genre, useNA = 'always')
### consolidating the naming convention for all the different genres in the favourite_genre variable
survey2003_dirty$favourite_genre <- fct_recode(survey2003_dirty$favourite_genre, action = "actin", comedy = "comdy", comedy = "Comedy", thriller = "Thriler", thriller = "thrller")
table(survey2003_dirty$favourite_genre)

## B) Variable : sleep_hr
table(survey2003_dirty$sleep_hr)
### There is only 24 hours in a day, so any data that exceed this would be an error. So they are all set to NA
survey2003_dirty$sleep_hr[survey2003_dirty$sleep_hr > 24] <- NA
table(survey2003_dirty$sleep_hr, useNA = 'always')

## C) Variable : TV_hr
table(survey2003_dirty$TV_hr)
### Negative hours is not valid, so any data that are negatives will be set to NA. 
survey2003_dirty$TV_hr[survey2003_dirty$TV_hr < 0] <- NA
table(survey2003_dirty$TV_hr, useNA = "always")

## D) Variable : height
table(survey2003_dirty$height)
### According to an article in this news site https://amp.adelaidenow.com.au/news/national/worlds-smallest-man-chandra-bahadur-dangi-in-sydney/news-story/e8cf2c005dc8ba7a22188fd120c805e8 , the shortest adult in Australia is around 54.6cm tall. So anything below this would be impossible. The height of 1.78 and 16.4 are set to NA.
survey2003_dirty$height[survey2003_dirty$height < 54.6] <- NA
### A height of 1865 is absolutely not possible, so this is a So it is set to NA.
survey2003_dirty$height[survey2003_dirty$height == 1865] <- NA
table(survey2003_dirty$height, useNA = "always")

## E) Variable : weight
table(survey2003_dirty$weight)
### A weight of 4.1 is not possible for a grown adult, so this is an outlier. Therefore, it is set to NA. 
survey2003_dirty$weight[survey2003_dirty$weight == 4.1] <- NA
### A weight of 190kg is possible, but it doesn't fit it with the average weight of individuals presented in this dataset. This is an outlier. But I will not set it to NA. 
table(survey2003_dirty$weight, useNA = "always")

## F) Variable : Gender 
table(survey2003_dirty$gender)
### consolidating the naming convention for all the different types of spellings and conventions for female and male.
survey2003_dirty$gender <- fct_recode(survey2003_dirty$gender, female = "F", female = "Female", male = "M", male = "Male")
table(survey2003_dirty$gender)

#Q2_&_Q3 : Plots 
## Histogram for numerical variables 
ggplot(survey2003_dirty, aes(sleep_hr)) + geom_histogram()
ggplot(survey2003_dirty, aes(TV_hr)) + geom_histogram()

## Filter out any outliers from the dataset for height and weight for more accurate depiction of their distributions.
survey2003_dirty %>%
  filter(height > 55) %>%
  ggplot(aes(x = height)) +
  geom_histogram()
survey2003_dirty %>%
  filter(weight < 190) %>%
  ggplot(aes(x = weight)) +
  geom_histogram()

survey2003_dirty %>%
  select(where(is.numeric)) %>%
  pivot_longer(everything())

## bar charts for categorical variables
ggplot(survey2003_dirty[!is.na(survey2003_dirty$favourite_genre),], aes(x = favourite_genre)) + geom_bar(na.rm = TRUE)
ggplot(survey2003_dirty, aes(x = gender)) + geom_bar()

#Q4 : Five Number Summary
summary(survey2003_dirty)
sd(survey2003_dirty$sleep_hr, na.rm=TRUE)
## Checking the categorical variables using frequency table
table(survey2003_dirty$favourite_genre, useNA = 'always')
table(survey2003_dirty$gender)


#Q5 : Save cleaned data
write_csv(survey2003_dirty, "survey2003_cleaned.csv")
A1_a1751699 <- read_csv("survey2003_cleaned.csv")


