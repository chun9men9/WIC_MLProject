# Idea borrowed from this script: https://www.kaggle.com/serigne/stacked-regressions-top-4-on-leaderboard


def impute(all_data):

	# PoolQC : data description says NA means "No Pool". That make sense, given the huge ratio of missing value (+99%) and majority of houses have no Pool at all in general.
	all_data["PoolQC"] = all_data["PoolQC"].fillna("None")

	# MiscFeature : data description says NA means "no misc feature"
	all_data["MiscFeature"] = all_data["MiscFeature"].fillna("None")

	# Alley : data description says NA means "no alley access"
	all_data["Alley"] = all_data["Alley"].fillna("None")

	# Fence : data description says NA means "no fence"
	all_data["Fence"] = all_data["Fence"].fillna("None")

	# FireplaceQu : data description says NA means "no fireplace"
	all_data["FireplaceQu"] = all_data["FireplaceQu"].fillna("None")

	# LotFrontage : Since the area of each street connected to the house property most likely have a similar area to other houses in its neighborhood , we can fill in missing values by the median LotFrontage of the neighborhood.
	# Group by neighborhood and fill in missing value by the median LotFrontage of all the neighborhood
	# **** imansingh - maybe do histogram to see if NAs should be treated as a separate category
	all_data["LotFrontage"] = all_data.groupby("Neighborhood")["LotFrontage"].transform(lambda x: x.fillna(x.median()))

	# GarageType, GarageFinish, GarageQual and GarageCond : Replacing missing data with None
	for col in ('GarageType', 'GarageFinish', 'GarageQual', 'GarageCond'):
		all_data[col] = all_data[col].fillna('None')

	# GarageYrBlt, GarageArea and GarageCars : Replacing missing data with 0 (Since No garage = no cars in such garage.)
	# **** imansingh - Should we really replace GarageYrBuilt w/ 0? That means it was built in year zero - could throw off the analysis
	for col in ('GarageYrBlt', 'GarageArea', 'GarageCars'):
		all_data[col] = all_data[col].fillna(0)

	# BsmtFinSF1, BsmtFinSF2, BsmtUnfSF, TotalBsmtSF, BsmtFullBath and BsmtHalfBath : missing values are likely zero for having no basement
	for col in ('BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF','TotalBsmtSF', 'BsmtFullBath', 'BsmtHalfBath'):
		all_data[col] = all_data[col].fillna(0)

	# BsmtQual, BsmtCond, BsmtExposure, BsmtFinType1 and BsmtFinType2 : For all these categorical basement-related features, NaN means that there is no basement.
	for col in ('BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2'):
		all_data[col] = all_data[col].fillna('None')

	# MasVnrArea and MasVnrType : NA most likely means no masonry veneer for these houses. We can fill 0 for the area and None for the type.
		# **** imansingh - maybe do histogram to see if NAs should be treated as a separate category
	all_data["MasVnrType"] = all_data["MasVnrType"].fillna("None")
	all_data["MasVnrArea"] = all_data["MasVnrArea"].fillna(0)

	# MSZoning (The general zoning classification) : 'RL' is by far the most common value. So we can fill in missing values with 'RL'
	# **** imansingh - maybe do histogram to see if NAs should be treated as a separate category
	all_data['MSZoning'] = all_data['MSZoning'].fillna(all_data['MSZoning'].mode()[0])

	# Utilities : For this categorical feature all records are "AllPub", except for one "NoSeWa" and 2 NA . Since the house with 'NoSewa' is in the training set, this feature won't help in predictive modelling. We can then safely remove it.
	# all_data = all_data.drop(['Utilities'], axis=1)

	# Functional : data description says NA means typical
	all_data["Functional"] = all_data["Functional"].fillna("Typ")

	# Electrical : It has one NA value. Since this feature has mostly 'SBrkr', we can set that for the missing value.
	# **** imansingh - maybe do histogram to see if NAs should be treated as a separate category
	all_data['Electrical'] = all_data['Electrical'].fillna(all_data['Electrical'].mode()[0])

	# KitchenQual: Only one NA value, and same as Electrical, we set 'TA' (which is the most frequent) for the missing value in KitchenQual.
	# **** imansingh - maybe do histogram to see if NAs should be treated as a separate category
	all_data['KitchenQual'] = all_data['KitchenQual'].fillna(all_data['KitchenQual'].mode()[0])

	# Exterior1st and Exterior2nd : Again Both Exterior 1 & 2 have only one missing value. We will just substitute in the most common string
	# **** imansingh - maybe do histogram to see if NAs should be treated as a separate category
	all_data['Exterior1st'] = all_data['Exterior1st'].fillna(all_data['Exterior1st'].mode()[0])
	all_data['Exterior2nd'] = all_data['Exterior2nd'].fillna(all_data['Exterior2nd'].mode()[0])

	# SaleType : Fill in again with most frequent which is "WD"
	# **** imansingh - maybe do histogram to see if NAs should be treated as a separate category
	all_data['SaleType'] = all_data['SaleType'].fillna(all_data['SaleType'].mode()[0])

	# MSSubClass : Na most likely means No building class. We can replace missing values with None
	# **** imansingh - maybe do histogram to see if NAs should be treated as a separate category
	all_data['MSSubClass'] = all_data['MSSubClass'].fillna("None")
	
	# Transforming some numerical variables that are really categorical

	all_data['MSSubClass'] = all_data['MSSubClass'].apply(str)
	all_data['OverallCond'] = all_data['OverallCond'].astype(str)
	all_data['OverallQual'] = all_data['OverallQual'].astype(int)
	all_data['GarageCars'] = all_data['GarageCars'].astype(str)
	all_data['YrSold'] = all_data['YrSold'].astype(str)
	all_data['MoSold'] = all_data['MoSold'].astype(str)
	
	return all_data

def derived_vars(all_data):
	# Adding total sqfootage and total finished sqfootage feature 
	all_data['TotalSF'] = all_data['TotalBsmtSF'] + all_data['GrLivArea']
	all_data['TotalFinishedSF'] = all_data['BsmtFinSF1'] + all_data['BsmtFinSF2'] + all_data['GrLivArea']
	all_data['HighQualFinishedSF'] = all_data['TotalSF'] - all_data['LowQualFinSF']


	# Adding total baths feature 
	all_data['TotalBaths'] = all_data['FullBath'] + all_data['BsmtFullBath'] + (.5 * (all_data['HalfBath'] + all_data['BsmtHalfBath']))

	return all_data

def interact_vars(all_data):
	# Numeric Var Interactions  
	all_data['OverallQual * TotalBaths'] = all_data['OverallQual'] * all_data['TotalBaths']
	all_data['OverallQual * TotalSF'] = all_data['OverallQual'] * all_data['TotalSF']
	all_data['TotalBaths * TotalSF'] = all_data['TotalBaths'] * all_data['TotalSF']
	#all_data['GarageCars * GarageArea'] = all_data['GarageCars'].astype(int) * all_data['GarageArea']

	# Categorical Var Interactions
	all_data['OverallQual + OverallCond'] = all_data['OverallQual'].astype(str) + "+" + all_data['OverallCond'].astype(str) 
	all_data['BsmtQual + BsmtCond'] = all_data['BsmtQual'] + "+" + all_data['BsmtCond']
	all_data['GarageQual + GarageCond'] = all_data['GarageQual'] + "+" + all_data['GarageCond']
	all_data['ExterQual + ExterCond'] = all_data['ExterQual'] + "+" + all_data['ExterCond']
	all_data['Heating + HeatingQC'] = all_data['Heating'] + "+" + all_data['HeatingQC']
	all_data['SaleType + SaleCondition'] = all_data['SaleType'] + "+" + all_data['SaleCondition']

	return all_data

def select_vars_train(all_data):
	# drop features that seem less relevant to sale price.
	#dropped_data = all_data.drop(['MSSubClass, MSZoning, LotFrontage, LotArea, OverallCond'], axis=1)
	selected_data = all_data[['Id', 'Neighborhood', 'HouseStyle', 'OverallQual', 'YearBuilt', 'ExterQual', 'Foundation', 'BsmtQual', 'TotalSF', 'TotalBaths', 'GarageFinish', 'GarageCars', 'PavedDrive', 'SaleType', 'SaleCondition', 'OverallQual * TotalBaths', 'OverallQual * TotalSF', 'TotalBaths * TotalSF', 'SalePrice']]
	selected_data.head()
	return selected_data

def select_vars_test(all_data):
	# drop features that seem less relevant to sale price.
	#dropped_data = all_data.drop(['MSSubClass, MSZoning, LotFrontage, LotArea, OverallCond'], axis=1)
	selected_data = all_data[['Id', 'Neighborhood', 'HouseStyle', 'OverallQual', 'YearBuilt', 'ExterQual', 'Foundation', 'BsmtQual', 'TotalSF', 'TotalBaths', 'GarageFinish', 'GarageCars', 'PavedDrive', 'SaleType', 'SaleCondition', 'OverallQual * TotalBaths', 'OverallQual * TotalSF', 'TotalBaths * TotalSF']]
	selected_data.head()
	return selected_data














































