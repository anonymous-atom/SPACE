# Import necessary libraries
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt   # plotting
import seaborn as sns   # plotting heatmap
import statsmodels.api as sm  # seasonal trend decomposition
from statsmodels.graphics import tsaplots   # autocorrelation

#Read data
import pandas as pd
pd.set_option('display.max_columns', None)

df = pd.read_csv('NEO_count.csv', infer_datetime_format=True, parse_dates=['cd'], index_col='cd')
df.head()

#Print smallest and largest date
print(df.index.min())
print(df.index.max())

#DataFrame for count of NEOs per year
df_year = df.resample('Y').sum()
df_year.head(20)

plt.style.use('fivethirtyeight')
#Plot NEOs per year plotly
import plotly.express as px
fig = px.line(df_year, x=df_year.index, y='count', title='Number of Near Earth Objects (NEO) per year')

