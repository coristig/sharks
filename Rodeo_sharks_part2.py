import pandas as pd
df2 = pd.read_csv('/Users/coristig/github/colin/sharks/sharks_coords.csv')
df2.columns

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

tree = neighbors.KDTree(coords,leaf_size=2)
dist, ind = tree.query(coords[7], k=5)     
print(ind[0])  # indices of 4 closest neighbors
print(sum(dist[0][1:]))  # distances to 4 closest neighbors

print(dist[0])
print(dist[0][1:])

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

