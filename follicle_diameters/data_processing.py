import pandas as pd
import numpy as np

data = pd.read_csv("follicle_data.csv", header=None) #reading in csv file

print(data.head(6))
print(data.shape)
print(data.median(axis=1))
