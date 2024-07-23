import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt

import datashader as ds
import datashader.transfer_functions as tf
import holoviews as hv
from holoviews.operation.datashader import datashade
from bokeh.io import output_notebook, show


path = "data/data/networks/uk_nodes.csv"


df = pd.read_csv(path)
print(df)

gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.x_coord, df.y_coord),crs="EPSG:32618")
print(gdf)
gdf_27700 = gdf.to_crs(epsg=27700)
print(gdf_27700)

gdf_27700.plot()
plt.show()


