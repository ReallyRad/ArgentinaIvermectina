import pandas as pd
import statsmodels.api as sm

# Load the data into a Pandas DataFrame
data = pd.read_csv('data/merged_dataset.csv')

# Specify the columns to use as predictors (independent variables) and the response variable (dependent variable)
X = data[['CUMULATIVE_IVM', 'CUMULATIVE_VAX']]
y = data['CFR']

# Add a constant term to the predictor variables (to represent the intercept)
X = sm.add_constant(X)

# Fit the multiple regression model using OLS (Ordinary Least Squares) method
model = sm.OLS(y, X).fit()

# Print the summary statistics of the model
print(model.summary())