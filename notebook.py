import os
from sklearn import linear_model
import pandas as pd

current_path = os.path.dirname(os.path.realpath(__file__))

museums_df = pd.read_csv(current_path + '/museums.csv', names=["name", "city", "vistors per year", "year reporteds"])
cities_df = pd.read_csv(current_path + '/cities.csv', names=["name", "population"])
merge_df = pd.merge(cities_df, museums_df, left_on='name', right_on='city', how='outer')
data = merge_df[["vistors per year"]]
target = merge_df['population']

print(data)
print(target)

lm = linear_model.LinearRegression()
model = lm.fit(data, target)

predictions = lm.predict(data)
print(predictions[0:5])
