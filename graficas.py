
import matplotlib.pyplot as plt
import pandas as pd

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

def simple(df):
    murder = df.groupby(['DATE', 'MUNICIPIO', 'TIPO DE DELITO'])['VALUE'].sum().reset_index()

    murder['RATE'] = murder.apply(lambda row: row.VALUE/poblacion[row.MUNICIPIO]* 100000, axis=1).round(2)


    rate_max = murder.RATE.max()
    fig, ax = plt.subplots(10, 1, sharex=True, figsize=(20, 15))

    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    i =0
    for key, grp in murder.groupby(['MUNICIPIO']):
        ax[i].plot(grp['DATE'], grp['RATE'])
        ax[i].set_ylim(0, rate_max*1.1)
        ax[i].set_xlabel("Time")
        ax[i].set_title(key, fontsize='large', loc='left',  y=0.5, x=0.02, )
        ax[i].grid(True)

        i +=1

    return fig

