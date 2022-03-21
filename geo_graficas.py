#!/usr/bin/env python
# coding: utf-8




# load libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import geopandas as gpd
import streamlit as st
import geopandas
from shapely.geometry import box

poblacion = {"Armería" : 27626,
"Colima" : 157048,
"Comala" : 21661,
"Coquimatlán" : 20837,
"Cuauhtémoc" : 31267,
"Ixtlahuacán" : 5623,
"Manzanillo" : 191031,
"Minatitlán" : 10231,
"Tecomán" : 116305,
"Villa de Álvarez" : 149762}

def g_simple(df):

    file_path = 'input/06mun.shp'
    BOX = [box(-104.75, 18.65, -103.45,19.55)]
    grid = gpd.GeoDataFrame({'geometry':BOX})
    colima = gpd.read_file(file_path)
    grid = grid.set_crs(epsg=6365)
    colima = colima.to_crs(epsg=6365)
    shape_clip = colima.clip(grid, keep_geom_type=True)

    df['DATE'] = df['DATE'].dt.year

    murder =df.groupby(['DATE', 'MUNICIPIO'])['VALUE'].sum().reset_index()
    murder['RATE'] = murder.apply(lambda row: row.VALUE/poblacion[row.MUNICIPIO]* 100000, axis=1).round(2)
    shape_clip.rename(columns={'NOMGEO': 'MUNICIPIO'}, inplace=True)

    murder_geo = pd.merge(shape_clip, murder, on="MUNICIPIO")
    print(murder.shape)
    print(murder_geo.shape)
    murder_2020 = murder_geo[(murder_geo.DATE == 2020)]
    print(murder_2020.shape)

    
    pivot_tbl = pd.pivot_table(
            df,
            values=['VALUE'],
            index=['DATE', 'MUNICIPIO'],
            aggfunc="sum",
            margins=True
            )
    #st.write(pivot_tbl.to_html(), unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(12,14))

    murder_2020.plot(column='RATE', ax=ax, scheme='equal_interval', k=5, cmap='OrRd', edgecolor='k', legend=True)



    st.write("2020")
    st.write(murder_2020[['MUNICIPIO','VALUE','RATE']].sort_values(['RATE']))
    murder_2020.apply(lambda x: ax.annotate(text=x['MUNICIPIO'] 
        + "\n"+ str(x['RATE']), 
        xy=x.geometry.centroid.coords[0], ha='center', backgroundcolor="yellow"), axis=1);
    st.pyplot(fig)
    
 
# mapa_mex['ENTIDAD'] = mapa_mex['ENTIDAD'].str.upper()
# mapa_mex['ENTIDAD'] = mapa_mex['ENTIDAD'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
# 
# mapa_mex['MUNICIPIO'] = mapa_mex['MUNICIPIO'].str.upper()
# mapa_mex['MUNICIPIO'] = mapa_mex['MUNICIPIO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
 




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

# import mapclassify
# 
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
