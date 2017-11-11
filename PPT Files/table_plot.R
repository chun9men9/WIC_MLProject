tableplot(house_train %>% select(one_of("SalePrice","OverallQual", "ExterQual", "BsmtQual",
                                        "KitchenQual", "GarageFinish", "FireplaceQu","Foundation")), 
          decreasing = TRUE, 
          nBins = 18,
          colorNA = "#FF1414", colorNA_num = "#FF1414")

tableplot(house_train %>% select(one_of("SalePrice","GrLivArea", "YearBuilt","FullBath","GarageArea",
                                        "TOtRmsAbvGrd")), 
          decreasing = TRUE, 
          nBins = 18,
          colorNA = "#FF1414", colorNA_num = "#FF1414")