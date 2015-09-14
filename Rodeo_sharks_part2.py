import pandas as pd
import numpy as np
import time
from geopy.geocoders import GoogleV3
from geopy.geocoders import Nominatim

geolocator = GoogleV3()
geolocator2 = Nominatim()

# test our geolocator:
geolocator.geocode('66 w 39th street new york city')

# plotting unprovoked attacks in the USA post 1900
df2 = df[(df.Country=='USA') & (df.year>1900) & (df.Type=='Unprovoked')]

def get_location(row):
    time.sleep(.02)
    loc = str(row.Location) + ', ' + str(row.Area) + ', ' + str(row.Country)
    for _ in range(1):
        try:
            # try our first geocoder
            location = geolocator.geocode(loc)
            print location
            print row.index
            if not location==None:
                lat = location[1][0]
                long = location[1][1]
                return lat, long
            else:
                try:
                    # try our second geocoder if first one fails
                    location = geolocator.geocode2(loc)
                    print location
                    print row.index
                    if not location==None:
                        lat = location[1][0]
                        long = location[1][1]
                        return lat, long
                    else:
                        return None, None
                except:
                    return None, None
                    continue
        except:
            return None, None
            continue
        return row.latitude, row.longitude

# running the code below takes a while.  We can read in the csv on line 53 
# df2['latitude'], df2['longitude'] = zip(*df2.apply(get_location,axis=1))
# df2.to_csv('./sharks_coords.csv',index=False)

df2 = pd.read_csv('./sharks/sharks_coords.csv')
df2[['Area','Location','Country','latitude', 'longitude']].head()

# lets plot our attacks in the USA

# super useful for installing: http://ilessendata.blogspot.com/2014/02/making-maps-python.html
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
%matplotlib inline

# create a new df with only locations we have coords for 
dfc = df2.dropna(axis=0, subset=['latitude'])

# USA Plot
USA_map = Basemap(projection='mill', resolution = 'l', llcrnrlon=-180, llcrnrlat=2, urcrnrlon=-62, urcrnrlat=60)
              
plt.figure(figsize=(18,18))

x1,y1 = USA_map(dfc['longitude'].tolist(), dfc['latitude'].tolist())
USA_map.plot(x1,y1, 'bo', markersize=7,alpha=.3)

USA_map.drawlsmask(lakes=False)
USA_map.drawcoastlines(color='gray')
USA_map.fillcontinents(color = 'lightgrey')
USA_map.drawmapboundary()
USA_map.drawstates()
USA_map.bluemarble(alpha=.2)
USA_map.drawcountries()


from sklearn import neighbors

coords = np.column_stack((dfc.latitude,dfc.longitude))

# create our tree
tree = neighbors.KDTree(coords,leaf_size=2)
dist, ind = tree.query(coords[7], k=6) # look at row 7    
print ind[0]  # indices of 5 closest neighbors
print sum(dist[0][1:])  # distances to 5 closest neighbors, excluding the point itself

sums = []
for i in range(len(coords)):
    dist, ind = tree.query(coords[i], k=5)
    sums.append(sum(dist[0][1:]))
    
dfc['dist_sums'] = pd.Series(sums, index=dfc.index)

outliers = dfc.sort(['dist_sums'], ascending=False)

# USA Plot
USA_map = Basemap(projection='mill', resolution = 'l',
    llcrnrlon=-180, llcrnrlat=2,
    urcrnrlon=-62, urcrnrlat=60)
              
plt.figure(figsize=(18,18))

x1,y1 = USA_map(outliers['longitude'][25:].tolist(), outliers['latitude'][25:].tolist())
x2,y2 = USA_map(outliers['longitude'][:25].tolist(), outliers['latitude'][:25].tolist())

USA_map.plot(x1,y1, 'bo', markersize=7)
USA_map.plot(x2,y2, 'ro', markersize=7)

USA_map.drawlsmask(lakes=False)
USA_map.drawcoastlines(color='gray')
USA_map.fillcontinents(color = 'lightgrey')
USA_map.drawmapboundary()
USA_map.drawcountries()
USA_map.drawstates()
USA_map.bluemarble(alpha=.2)

CA_map = Basemap(projection='mill', resolution='l',
llcrnrlon=-128, llcrnrlat=33,
urcrnrlon=-113, urcrnrlat=44)

plt.figure(figsize=(18,10))

# coords for fatal attacks 
x1,y1 = CA_map(outliers[(outliers.Area=='California')]['longitude'][:10].tolist(),outliers[(outliers.Area=='California')]['latitude'][:10].tolist())
x2,y2 = CA_map(outliers[(outliers.Area=='California')]['longitude'][10:].tolist(),outliers[(outliers.Area=='California')]['latitude'][10:].tolist())


CA_map.plot(x2,y2, 'bo', markersize=5,alpha=.5)
CA_map.plot(x1,y1, 'ro', markersize=5)

CA_map.drawlsmask(lakes=False)
CA_map.drawcoastlines(color='gray')
CA_map.fillcontinents(color = 'lightgrey')
CA_map.drawmapboundary()
CA_map.drawstates()
CA_map.bluemarble(alpha=.2)

plt.show()
