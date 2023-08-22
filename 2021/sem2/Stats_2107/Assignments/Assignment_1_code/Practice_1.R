library(tidyverse)

s <- "    this is an example string    "
trimws(s)

vect_1 <- c(s, s, " A", " B ", "  C ", "D ")
f <- factor()