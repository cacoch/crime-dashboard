#!/usr/bin/env python
# coding: utf-8




# load libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import geopandas as gpd
import streamlit as st
import geopandas

def g_simple():

    file_path = 'input/06mun.shp'
    colima = gpd.read_file(file_path)
    st.pyplot(colima.plot().figure)
 
    #mapa_mex.drop([ 'ADM2_PCODE', 'ADM2_REF', 'ADM2ALT1ES','ADM2ALT2ES','ADM1_PCODE','ADM0_ES', 'ADM0_PCODE', 'date', 'validOn', 'validTo'], axis=1, inplace=True)
# 
# 
# 
# 
# mapa_mex.rename(columns={'ADM1_ES': 'ENTIDAD', 'ADM2_ES' : 'MUNICIPIO'}, inplace=True)
# mapa_mex['ENTIDAD'] = mapa_mex['ENTIDAD'].str.upper()
# mapa_mex['ENTIDAD'] = mapa_mex['ENTIDAD'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
# 
# mapa_mex['MUNICIPIO'] = mapa_mex['MUNICIPIO'].str.upper()
# mapa_mex['MUNICIPIO'] = mapa_mex['MUNICIPIO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
# 
# 
# 
# 
# df = pd.read_pickle('colima.pkl')
# df.drop('ENTIDAD', axis=1, inplace=True)
# df.head()
# 
# 
# 
# 
# mapa_col = mapa_mex.loc[mapa_mex['ENTIDAD'] == 'COLIMA'].copy()
# mapa_col.drop('ENTIDAD',  axis=1, inplace=True)
# 
# 
# 
# 
# mrg = mapa_col.merge(df, on='MUNICIPIO')
#pd.pivot_table(
#    mrg,
#    values=['VALUE'],
#    index=['MODALIDAD', 'TIPO', ],
#    aggfunc="sum",
#   # margins=True
#)




# murders =mrg.loc[mrg.MODALIDAD == 'HOMICIDIOS'].copy()
# pd.pivot_table(
#     murders,
#     values=['VALUE'],
#     index=['MUNICIPIO' ],
#     aggfunc="sum",
#     margins=True
# )



# shows excetions
##cmaps['Sequential'] = [
##            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
##            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
##            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
##



# X1 = murders.groupby([pd.Grouper(key='DATE', freq='Y'),'MUNICIPIO']).agg(
#        {'VALUE': 'sum', 'POPULATION': 'first',
#              'geometry':'first', 'Shape_Leng': 'first',
#             'Shape_Area': 'first'}).reset_index()
# X1['RATE'] = 100000 * X1['VALUE'] /X1['POPULATION']
#murders.head()
#https://stackoverflow.com/questions/63974040/line2d-object-has-no-property-column
# from geopandas import GeoDataFrame
# X1 = GeoDataFrame(X1)
# m_2011 = X[X['DATE'].dt.year == 2017]
# m_2011 = GeoDataFrame(m_2011)
# 
# 
# 
# 
# from shapely.geometry import box
# import mapclassify
# 
# variable = 'RATE'
# cmap = 'Oranges'
# fig, ax = plt.subplots(1, figsize=(20, 12))
# minx, miny, maxx, maxy = mrg.total_bounds
# 
# #print(minx, miny, maxx, maxy)
# ax.set_xlim(-104.75, -103.45)
# ax.set_ylim(18.65, 19.55)
# 
# # Create colorbar as a legend
# sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=130))
# # empty array for the data range
# sm._A = []
# # add the colorbar to the figure
# #cbar = fig.colorbar(sm)
# 
# BOX = [box(-104.75, 18.65, -103.45,19.55)]
# grid = gpd.GeoDataFrame({'geometry':BOX})
# grid.boundary.plot(ax=ax, color="green")
# 
# m_2011 = m_2011.clip(grid)
# 
# m_2011.plot(column=variable,
#        cmap=cmap,
#          scheme='quantiles', k=4,legend=True,
#        linewidth=0.8,
#        ax=ax,
#        edgecolor='0.8') #, legend=True,  legend_kwds={'label': 'Distribución del delitos', 'orientation': "vertical"})
# 
# # remove the axis
# ax.axis('off')
# 
# ax.set_title('Homicidios 2011', fontdict={'fontsize': '25', 'fontweight' : '3'})
# 
# 
# m_2011.apply( 
#     lambda x: ax.annotate(
#         text= x.MUNICIPIO + "\n" + str(round(x.RATE,1)),
#           #xy = (x.geometry.representative_point().coords[:][0][0],
#           #              x.geometry.representative_point().coords[:][0][1]),
#          xy=x.geometry.centroid.coords[0],
#           ha='center',
#          xytext=(4,4),
#           textcoords='offset points',
#           color='white',backgroundcolor='blue',alpha=0.9), axis=1);
# 
# plt.show()
# 
# 
# 
# 
# m_2011['centro']
# 
