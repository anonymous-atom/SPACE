
import requests
import pandas as pd
import numpy as np

# Get data from API
#url = 'https://ssd-api.jpl.nasa.gov/cad.api/'

# Read the csv file
df = pd.read_csv('NEO.csv')

#Set pandas to display all columns
pd.set_option('display.max_columns', None)

#Columns 'des', 'orbit_id', 'jd', 'cd', 'dist', 'dist_min', 'dist_max', 'v_rel','v_inf', 't_sigma_f', 'h'

#Only keep date in 'cd' column
df['cd'] = df['cd'].str[:11]

#Get count of NEO on each date and make a new dataframe
df2 = df.groupby('cd').size().reset_index(name='count')

#Convert 'cd' column to datetime
df2['cd'] = pd.to_datetime(df2['cd'])

#Sort by date
df2 = df2.sort_values(by=['cd'])

#Convert to csv file
df2.to_csv('NEO_count.csv', index=False)

#Plot the data using plotly
#Make sure the graph looks detailed enough
import plotly.express as px
# fig = px.line(df2, x='cd', y='count', title='Number of Near Earth Objects (NEO) per day')
# fig.show()

#Use Data from 2019 to 2020 to forecast the number of NEO in 2021
import statsmodels.api as sm

import matplotlib.pyplot as plt
#Perform rolling statistics
timeseries = df2['count']
rolmean = timeseries.rolling(window=365).mean()
rolstd = timeseries.rolling(window=365).std()

#Plot rolling statistics
orig = plt.plot(timeseries, color='blue', label='Original')
mean = plt.plot(rolmean, color='red', label='Rolling Mean')
std = plt.plot(rolstd, color='black', label='Rolling Std')
plt.legend(loc='best')
plt.title('Rolling Mean & Standard Deviation')
plt.show(block=False)



#Seasonality trend and residual by ETS decomposition
from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(timeseries, period=365)

trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

#Plot with x axis as date
plt.subplot(411)
plt.plot(timeseries, label='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal,label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()
plt.show()


#Perform Dickey-Fuller test:
from statsmodels.tsa.stattools import adfuller
print('Results of Dickey-Fuller Test:')
dftest = adfuller(timeseries, autolag='AIC')
dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
for key,value in dftest[4].items():
    dfoutput['Critical Value (%s)'%key] = value
print(dfoutput)

#Build a function to further check the stationarity of the data
def test_stationarity(timeseries):

        #Determing rolling statistics
        rolmean = timeseries.rolling(window=365).mean()
        rolstd = timeseries.rolling(window=365).std()

        #Plot rolling statistics:
        orig = plt.plot(timeseries, color='blue',label='Original')
        mean = plt.plot(rolmean, color='red', label='Rolling Mean')
        std = plt.plot(rolstd, color='black', label = 'Rolling Std')
        plt.legend(loc='best')
        plt.title('Rolling Mean & Standard Deviation')
        plt.show(block=False)

        #Perform Dickey-Fuller test:
        print('Results of Dickey-Fuller Test:')
        dftest = adfuller(timeseries, autolag='AIC')
        dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
        for key,value in dftest[4].items():
            dfoutput['Critical Value (%s)'%key] = value
        print(dfoutput)


#Do first difference
df2['first_difference'] = df2['count'] - df2['count'].shift(1)
test_stationarity(df2['first_difference'].dropna(inplace=False))

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
#ACF and PACF plots:
lag_acf = plot_acf(df2['first_difference'].dropna(), lags=20)
lag_pacf = plot_pacf(df2['first_difference'].dropna(), lags=20, method='ols')

fig_first = plot_acf(df2['first_difference'].dropna())
plt.show()

#As we have a seasonal trend, we need to use SARIMA model
model = sm.tsa.statespace.SARIMAX(df2['count'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 365))
results = model.fit()
print(results.summary())
print("Working")

#Now Prdict Forecast Oh this seasonal data using cuML
import cuml
import matplotlib.pyplot as plt
from cuml.tsa.arima import ARIMA
import cudf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

#Convert to cudf dataframe
df2 = cudf.DataFrame(df2)

#Set index as date
df2 = df2.set_index('cd')

model = ARIMA(df2, order=(1,1,1), seasonal_order=(1,1,1,7),
              fit_intercept=False)


#Fit the model
model.fit()

#Forecast for next year using forecast() function
forecast = model.forecast(365)

#Convert to pandas dataframe
forecast = forecast.to_pandas()


#Plot the forecast
plt.plot(forecast)
plt.show()

