setwd("C:/Users/cmlim/Dropbox/NYC Data Science/Class/Machine Learning Project/chungmeng")
house_train <- read.csv("../data/train.csv", 
                        header = TRUE, 
                        na.strings = "",
                        stringsAsFactors = FALSE)
## load test data
# house_test <- read.csv("../data/test.csv", 
#                        header = TRUE, 
#                        na.strings = "",
#                        stringsAsFactors = FALSE)
#dim(house_test)
dim(house_train)
str(house_train)
names(house_train)

library(VIM)
aggr(house_train)
library(mice)
md.pattern(house_train)


## get levels of categorical features from data description
factorLevel <- list()
conn <- file("../data/data_description.txt", open="r")
f <-readLines(conn)
for (line in f){
  if(!grepl("^[[:blank:]]", line) & grepl(": ", line)) {
    col_name <<- trimws(gsub(":.*", "", line))
  } else {
    level <- trimws(gsub("\t.*", "", line))
    if (level != "") {
      factorLevel[[col_name]] <- c(factorLevel[[col_name]], level)
    }
  }
}
close(conn)

print(factorLevel[1:20])