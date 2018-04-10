import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from pandas import Series
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap
import warnings
warnings.filterwarnings('ignore')

#volcanoes = pd.read_csv("/home/mazeqing/下载/database.csv")
earthquakes = pd.read_csv("/home/mazeqing/下载/database.csv")
def fig_p(data):
    series=Series(data).value_counts().sort_index()
    series.plot(kind='bar')
    
#全球地震分布
    
#the earthquakes dataset has nuclear explosions data in it so here i use only the earthquakes information
earthquakes_eq=pd.DataFrame()
earthquakes_eq=earthquakes[earthquakes['Type']=='Earthquake']
m = Basemap(projection='mill',llcrnrlat=-80,urcrnrlat=80, llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
fig = plt.figure(figsize=(12,10))

##longitudes_vol = volcanoes["Longitude"].tolist()
##latitudes_vol = volcanoes["Latitude"].tolist()

longitudes_eq = earthquakes_eq["Longitude"].tolist()
latitudes_eq = earthquakes_eq["Latitude"].tolist()

##x,y = m(longitudes_vol,latitudes_vol)
a,b= m(longitudes_eq,latitudes_eq)


plt.title("Earthquakes (green)")
##m.plot(x, y, "o", markersize = 5, color = 'red')
m.plot(a, b, "o", markersize = 3, color = 'green')

m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='coral',lake_color='aqua')
m.drawmapboundary()
m.drawcountries()
plt.show()

#将地震数据按纬度划分

#division of long&lat
def division(data):
    north_n=sum(data["Latitude"] >=30)
    middle_n=sum(np.logical_and(data["Latitude"]<30, data["Latitude"]>-30))
    south_n=sum(data["Latitude"]<= -30)
    #precentage
    total=north_n+middle_n+south_n
    north_p=north_n/total*100
    middle_p=middle_n/total*100
    south_p=south_n/total*100
    return north_n,middle_n,south_n,north_p,middle_p,south_p

#volc=division(volcanoes)

# 地震依纬度划分情况

eq=division(earthquakes_eq)

##print("There are",volc[0],"volcanoes in latitude over 30N",volc[1],
##      "in latitude between 30N and 30S and",volc[2],
##      "in latitude over 30S. In precentage it is %.2f%%"% volc[3],",",
##      "%.2f%%"% volc[4],"and","%.2f%%"% volc[5],"respectively.\n")

print("There were",eq[0],"earthquakes in latitude over 30N",eq[1],
      "in latitude between 30N and 30S and",eq[2],
      "in latitude over 30S. In precentage it is %.2f%%"% eq[3],",",
      "%.2f%%"% eq[4],"and","%.2f%%"% eq[5],"respectively.")
division=['over 30N','middle equator','over 30S']
count=[eq[0],eq[1],eq[2]]

fig7=plt.figure(figsize=(10,5))  
plt.bar(division,count,0.4,color="green")  
plt.ylabel("Count")
plt.title("Number of earthquakes by latitude")
plt.show()  


# 最近五年地震发生情况

##recent_active = volcanoes[(volcanoes["Last Known Eruption"]>='2012 CE') & (volcanoes["Last Known Eruption"]<='2016 CE')]
##print(recent_active.shape)
##longitudes_vol = recent_active["Longitude"].tolist()
##latitudes_vol = recent_active["Latitude"].tolist()


earthquakes_eq["Date"] = pd.to_datetime(earthquakes_eq["Date"])
earthquakes_eq["year"] = earthquakes_eq['Date'].dt.year
last_eq = earthquakes_eq[(earthquakes_eq["year"]>=2012) & (earthquakes_eq["year"]<=2016)]
print(last_eq.shape)


longitudes_eq = last_eq["Longitude"].tolist()
latitudes_eq = last_eq["Latitude"].tolist()


n = Basemap(projection='mill',llcrnrlat=-80,urcrnrlat=80, llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
##x,y = n(longitudes_vol,latitudes_vol)
c,d = n(longitudes_eq,latitudes_eq)

fig2 = plt.figure(figsize=(12,10))
plt.title("Earthquakes (green) that were recently active in the last 5 years")
##n.plot(x, y, "o", markersize = 5, color = 'red')
n.plot(c, d, "o", markersize = 3, color = 'green')
n.drawcoastlines()
n.fillcontinents(color='coral',lake_color='aqua')
n.drawmapboundary()
n.drawcountries()
plt.show()



##  地震发生最频繁的年份
earthquakes_eq['year'] = earthquakes_eq['Date'].dt.year

fig3=plt.figure(figsize=(10,5))
fig_p(earthquakes_eq['year'])
plt.ylabel("Count")
plt.title("Number of earthquakes by year")
plt.show()  
most_eq_year=Series(earthquakes_eq['year']).value_counts().sort_index().idxmax(axis=1)
print("The year with most earthquakes is:", most_eq_year)


##  地震震级（over 5.5）

fig4=plt.figure(figsize=(10,5))
fig_p(np.around(earthquakes_eq["Magnitude"]))
plt.ylabel("Count")
plt.title("Earthquakes magnitude (round up)")
plt.show() 

# 核爆炸震级

earthquakes_nex=pd.DataFrame()
earthquakes_nex=earthquakes[earthquakes['Type']=='Nuclear Explosion']
fig5=plt.figure(figsize=(10,5))
fig_p(np.around(earthquakes_nex["Magnitude"]))
plt.ylabel("Count")
plt.title("Nuclear Explosions magnitude (round up)")
plt.show() 


# 核爆炸数量按年分排列

earthquakes_nex["Date"] = pd.to_datetime(earthquakes_nex["Date"])
earthquakes_nex['year'] = earthquakes_nex['Date'].dt.year

fig6=plt.figure(figsize=(10,5))
fig_p(earthquakes_nex['year'])
plt.ylabel("Count")
plt.title("Number of Nuclear Explosion by year")
plt.show()
