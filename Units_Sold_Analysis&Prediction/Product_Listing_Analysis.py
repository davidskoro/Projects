# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 14:29:46 2020

############################################################################################################################################################################
# Product Listing Analysis and prediction                                                                                                                           
# Product listing data from Wish.com, providing insight into variables imapcting Units Sold 
# and a model for predicting Units Sold with 41.62% accuracy.                        
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Data found through Kaggle.com: https://www.kaggle.com/jmmvutu/summer-products-and-sales-in-ecommerce-wish?select=summer-products-with-rating-and-performance_2020-08.csv                                                         
############################################################################################################################################################################

@author: David
"""
import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn import metrics

#%% Load the data

proj = pd.read_csv('summer-products_2020-08.csv')
# Convert Prices from EUR to USD (as of November 21,2020)
proj['USD_Price'] = proj['price']*1.19
proj['USD_Retail'] = proj['retail_price']*1.19

#%% Summary statstics

# Product Color
color_data = pd.DataFrame()
color_data['Color'] = proj['product_color']
color_data['Price'] = proj['USD_Price']
color_data['Retail_Price'] = proj['USD_Retail']
color_data['Sold'] = proj['units_sold']
color_data['Rating'] = proj['rating']
color_data['Merchant']= proj['merchant_rating']
color_data['Ad'] = proj['uses_ad_boosts']
color_data['Picture'] = proj['merchant_has_profile_picture']
color_data['Origin'] = proj['origin_country']

# Origin frequency
origin_freq = color_data.groupby('Origin').count()
origin_freq['Freq'] = origin_freq['Price']
origin_freq = origin_freq['Freq']


# Color frequency
color_freq = color_data.groupby('Color').count().sort_values(by='Price', ascending=False)
color_freq['Freq'] = color_freq['Price']
print(color_freq['Freq'].head)

# Averages for each color 
color_summary = color_data.groupby('Color').mean().sort_values(by='Price', ascending=False)
color_summary['Freq'] = color_freq['Freq']
color_summary = color_summary.sort_values(by='Freq', ascending=False)

# How much over/under retail? Retail is a refrence price to indicate a regular value
color_summary['Over_Under'] = color_summary['Price']-color_summary['Retail_Price']

# Colors with a frequency over 5 (More then 5 products listed as this color)
color_freq = color_summary.loc[color_summary['Freq']>5]

# Save dataframes
color_data.to_csv('output/color_data.csv')
origin_freq.to_csv('output/origin_freq.csv')
color_summary.to_csv('output/color_avg_summary.csv')

#%% Scatter Plots to visualize and understand correlations between data

#Plot all data
SoldP = color_summary.plot.scatter('Sold','Price')
SoldP.set(Title = 'Units Sold vs Price')
SoldR=color_summary.plot.scatter('Sold','Rating')
SoldR.set(Title = 'Units Sold vs Rating')
# Plot only colors that appeared more then 5 times
SoldP_freq=color_freq.plot.scatter('Sold','Price')
SoldP_freq.set(Title = 'Units Sold vs Price (Freq > 5)')
SoldR_freq=color_freq.plot.scatter('Sold','Rating')
SoldR_freq.set(Title = 'Units Sold vs Rating (Freq > 5)')
# Rating has a more clear relationship with units sold then price, according to the scatter plots

# Save Visualizations
SoldP.get_figure().savefig('output/Sold_vs_Price')
SoldR.get_figure().savefig('output/Sold_vs_Rating')
SoldP_freq.get_figure().savefig('output/Sold_vs_Price_5')
SoldR_freq.get_figure().savefig('output/Sold_vs_Rating_5')
#%% How much do listing variables impact units sold?

model_Q1 = sm.OLS.from_formula('Sold ~ Price + Merchant + Rating + Picture', data=color_data)
result_Q1 = model_Q1.fit()
print(result_Q1.summary())


#%% Can units sold be predicted?

pred_vars = ['Price', 'Rating', 'Merchant']
train, test = train_test_split(color_data, test_size=0.25, shuffle=False)
dtree = tree.DecisionTreeClassifier(criterion="entropy", random_state=0)
dtree.fit(train[pred_vars], train['Sold'])
predict = dtree.predict(test[pred_vars])
Q2results = pd.DataFrame(predict)

Q2results.columns=['Prediction']
compare=pd.DataFrame()
compare['True']=test['Sold']

compare_reset = compare.reset_index(drop=True)
Q2_reset = Q2results.reset_index(drop=True)
compared = pd.DataFrame()
compared['Real'] = compare_reset['True']
compared['Predict'] = Q2_reset['Prediction']

#Evaluation:
# Observed Accuracy
print(compared.dtypes)
Obs_acc = (accuracy_score(compare_reset, Q2_reset))
print("Observed accuracy is:", Obs_acc)
# Observed accuracy is 41.62%

# Precision, Recall, F-1 Score
result = metrics.classification_report(test['Sold'], predict, digits=4)
print(result)
 

