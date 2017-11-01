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


varlist=data.frame(
  var_type=sapply(house_train,class),
  owner=c(rep('Theo',20),
          rep('Iman',20),
          rep('Chung',20),
          rep('Wing',21))
)

write.csv(varlist,file = 'variable_list.csv')

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

print(factorLevel[31:50])


myhouse_train=house_train[,41:60]
myhouse_train=cbind(myhouse_train,house_train[81])
names(myhouse_train)

num_cols <- sapply(myhouse_train, is.numeric)
num_myhouse_train=myhouse_train[,num_cols]
library(dplyr)
library(tidyr)
library(ggplot2)
num_myhouse_train2=melt(num_myhouse_train,"SalePrice")
num_myhouse_train2 %>%
  ggplot(aes(value,SalePrice)) +  geom_point() + facet_wrap(~variable)
 
  ggplot(aes(Heat_map, value)) + geom_point() + facet_wrap(~city)