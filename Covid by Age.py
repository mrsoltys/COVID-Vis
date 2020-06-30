import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
from matplotlib.ticker import ScalarFormatter
import numpy as np
import datetime

#%%

filename=(datetime.datetime.now()-datetime.timedelta(days=0)).strftime("Case data/covid19_case_summary_%Y-%m-%d.csv")

df = pd.read_csv(filename)                                          #Load CSV
df=df.pivot_table(index=['attribute','metric'],columns='description',values='value')  #Reshape the data

#Create a new df with only the data I want
df1=pd.DataFrame(data=df['Cases of COVID-19 in Colorado by Date Reported to the State'].dropna()
                 .xs('Cases', axis=0, level=1, drop_level=True))
df2=pd.DataFrame(data=df['Cases of COVID-19 in Colorado by Date of Illness Onset'].dropna()
                 .xs('Cases', axis=0, level=1, drop_level=True))
df3=pd.DataFrame(data=df['Cumulative Number of Hospitalized Cases of COVID-19 in Colorado by Date Reported to the State'].dropna()
                 .xs('Cases', axis=0, level=1, drop_level=True))
df4=pd.DataFrame(data=df['Number of Deaths From COVID-19 in Colorado by Date of Death - By Day'].dropna()
                 .xs('Deaths', axis=0, level=1, drop_level=True))
df5=pd.DataFrame(data=df['Cumulative Number of Hospitalized Cases of COVID-19 in Colorado by Date of Illness Onset'].dropna()
                 .xs('Cases', axis=0, level=1, drop_level=True))
df6=pd.DataFrame(data=df['Cumulative Number of Deaths From COVID-19 in Colorado by Date of Illness'].dropna()
                 .xs('Cases', axis=0, level=1, drop_level=True))
COVID=pd.concat([df1,df2,df3,df4,df5,df6], axis=1).rename(columns={"Cases of COVID-19 in Colorado by Date Reported to the State": "Cases Reported", 
                         "Cases of COVID-19 in Colorado by Date of Illness Onset": "Cases by Onset",
                         "Cumulative Number of Hospitalized Cases of COVID-19 in Colorado by Date Reported to the State":"Total Hosp",
                         "Number of Deaths From COVID-19 in Colorado by Date of Death - By Day": "Deaths by Date of Death",
                         "Cumulative Number of Hospitalized Cases of COVID-19 in Colorado by Date of Illness Onset":"Hosp by Onset",
                         "Cumulative Number of Deaths From COVID-19 in Colorado by Date of Illness":"Deaths by Onset",})
COVID["Percent Positve"]=pd.DataFrame(data=df['Positivity Data from Clinical Laboratories'].dropna()
                 .xs('Percent Positivity', axis=0, level=1, drop_level=True))['Positivity Data from Clinical Laboratories']
COVID["Total Tests"]=pd.DataFrame(data=df['Positivity Data from Clinical Laboratories'].dropna()
                 .xs('Count of people tested by CDPHE lab', axis=0, level=1, drop_level=True))['Positivity Data from Clinical Laboratories']+pd.DataFrame(data=df['Positivity Data from Clinical Laboratories'].dropna()
                 .xs('Count of people tested by non-CDPHE (commercial) lab', axis=0, level=1, drop_level=True))['Positivity Data from Clinical Laboratories']

#Sort Index by date
COVID.index = pd.to_datetime(COVID.index)
COVID=COVID.sort_index()

#Calculate New Columns
COVID['7DayTests'] = COVID['Total Tests'].iloc[:].rolling(window=7).mean()
COVID['7DayPPos']=COVID['Percent Positve'].iloc[:].rolling(window=7).mean()

COVID['7DayReport'] = COVID['Cases Reported'].iloc[:].rolling(window=7).mean()                               #Calculate 7 day avg of new cases
COVID['change in 7 day reported']=(COVID['7DayReport']-COVID['7DayReport'].shift(7))/COVID['7DayReport'].shift(7)*100
COVID['dHosp'] = COVID['Total Hosp']-COVID['Total Hosp'].shift(1)
COVID['7DayHosp'] = COVID['dHosp'].iloc[:].rolling(window=7).mean()
COVID['change in 7 day Hosp']=(COVID['7DayHosp']-COVID['7DayHosp'].shift(7))/COVID['7DayHosp'].shift(7)*100
COVID['7DayDeaths'] = COVID['Deaths by Date of Death'].iloc[:].rolling(window=7).mean()
COVID['change in 7 day Deaths']=(COVID['7DayDeaths']-COVID['7DayDeaths'].shift(7))/COVID['7DayDeaths'].shift(7)*100

#By onset
COVID['7DayOnset'] = COVID['Cases by Onset'].iloc[:].rolling(window=7).mean()  
COVID['change in 7 day onset']=(COVID['7DayOnset']-COVID['7DayOnset'].shift(7))/COVID['7DayOnset'].shift(7)*100
COVID['dHospOnset'] = COVID['Hosp by Onset']-COVID['Hosp by Onset'].shift(1)
COVID['7DayHospOnset'] = COVID['dHospOnset'].iloc[:].rolling(window=7).mean()
COVID['change in 7 day Hosp Onset']=(COVID['7DayHospOnset']-COVID['7DayHospOnset'].shift(7))/COVID['7DayHospOnset'].shift(7)*100

COVID['dDeathsOnset'] = COVID['Deaths by Onset']-COVID['Deaths by Onset'].shift(1)
COVID['7DayDeathsOnset'] = COVID['dDeathsOnset'].iloc[:].rolling(window=7).mean()
COVID['change in 7 day Deaths Onset']=(COVID['7DayDeathsOnset']-COVID['7DayDeathsOnset'].shift(7))/COVID['7DayDeathsOnset'].shift(7)*100
#%%