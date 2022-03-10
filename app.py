import streamlit as st
import numpy as np
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import matplotlib.pyplot as plt
import seaborn as sns
from graficas import simple


def main():
    #st.title("La estadistica")
    data_load_state = st.text('Loading data...')
    df = load_data()
    data_load_state.text("Done! (using st.cache)")

    page = st.sidebar.selectbox("Selecciona página", ['Homepage', 'Muestra datos', 'Pivot table', 'Graficas', 'Mapas'])

    if page == 'Homepage':
        st.title('XXX')

    elif page == 'Muestra datos':
        st.title("Muestra de datos")

        #st.dataframe( df.style.format({"DATE": 
        #    lambda t: t.strftime("%b %Y")}))
        AgGrid(df)
        st.markdown("""Se pueden filtrar los datos pinchando en el 
        titulo de la tabla""")

        
    elif page == 'Pivot table':

        pivot = pd.pivot_table(
            df,
            values=['VALUE'],
            #index=['MODALIDAD', 'TIPO', 'SUBTIPO'],
            index=['TIPO DE DELITO', 'MUNICIPIO'],
            aggfunc="sum",
            margins=True
        )
        st.write(pivot.to_html() ,unsafe_allow_html=True)


    elif page == 'Graficas':
        fig = simple(df)
        st.pyplot(fig)


    st.stop()


    
    df = filtro(df, tipo='Homicidio', return_cols=['TIPO DE DELITO', 'SUBTIPO DE DELITO'])
    
    st.write(df.MUNICIPIO.unique().tolist())


    grp = df.groupby("MUNICIPIO")
    
    fig, ax = plt.subplots()
    for key, gr in grp:
        ax.plot(gr.DATE, gr.VALUE, label=key)

    ax.legend()

    st.pyplot(fig)

# given province  name and date, we aproximate poblation size linearly 
def get_poblacion(poblacion, province, date):
    # define poblation census at 2015 Jun, 60 month later at 2020 Jun
    start_date = '2015-6'

    muni = [ "Armería", "Colima", "Comala", "Coquimatlán",
           "Cuauhtémoc", "Ixtlahuacán", "Manzanillo", "Minatitlán",
           "Tecomán", "Villa de Álvarez" ]
    x0 = pd.to_datetime( start_date, format='%Y-%m') 
    y2 ,y1  = poblacion.loc[province, ['POB2020', 'POB2015']]

    delta = int((date - x0)/np.timedelta64(1, 'M'))

    # interval in month between samples (5 year)
    interval = 60
    
    #slope
    m = (y2 - y1) /interval

    y = m * delta + y1
    return y

# return rate, values  for colima, Mexico, max state
def filtro(ds, bien=None, tipo=None, subtipo=None, modalidad=None, return_cols=[]):
    
    fields = ['BIEN JURÍDICO AFECTADO', 'TIPO DE DELITO', 'SUBTIPO DE DELITO', 'MODALIDAD']
    
    if set(fields) != set(fields).union(set(return_cols)):
        raise ValueError("Wrong return columns name")
        
    def filter_fn(row):
        if bien:
            c1 = (row['BIEN JURÍDICO AFECTADO'] == bien)
        else:
            c1 = True
            
        if tipo:
            c2 = (row['TIPO DE DELITO'] == tipo)
        else:
            c2 = True
        
        if subtipo:
            c3 = (row['SUBTIPO DE DELITO'] == subtipo)
        else:
            c3 = True
        
        if modalidad:
            c4 = (row['MODALIDAD'] == modalidad)
        else:
            c4 = True
            
        return c1 & c2 & c3 & c4
    
    # filter data
    f = ds.apply(filter_fn, axis=1)
    ds = ds[f]
    ds = ds[['DATE', 'MUNICIPIO', 'VALUE'] + return_cols]
    
    # group and sum to remove duplicate rows 
    ds = ds.groupby(['DATE', 'MUNICIPIO'] + return_cols)['VALUE'].sum().reset_index()

    # calculate rate per month, state and category
    if False: """
    ds['RATE'] = ds.apply(lambda row: row.VALUE / get_poblacion(
        row.ENTIDAD,row.DATE) * 100000 ,axis=1).round(2)
    
    # calculate max state rate per month and category 
    ds_max =ds.groupby(['DATE'] + return_cols).agg(MAX=('RATE' ,'max')).reset_index() 
    
    # calculate national value per category 
    ds_nac =ds.groupby(['DATE'] + return_cols).agg(VALUE=('VALUE' ,'sum')).reset_index()
    ds_nac['ENTIDAD'] = 'Nacional'
    # calculate national rate per category
    ds_nac['RATE'] = ds_nac.apply(lambda row: row.VALUE / get_poblacion(
        row.ENTIDAD,row.DATE) * 100000 ,axis=1).round(2)    
    nacional = ds_nac.copy()                                           
    #ds_col = ds.loc[ds.ENTIDAD == 'Colima']                                               
    ds_col = ds.loc[ds.ENTIDAD == 'Michoacán de Ocampo']       
                                                   
                                                   
    result_nac = pd.merge(ds_max, ds_nac, on=['DATE']+ return_cols)
    result  = result_nac.append( ds_col, sort=True)
    
    result.sort_values('DATE', inplace=True)
    result.reset_index(drop=True, inplace=True)

    
    return result, nacional
    """
    return ds

def load_data():
 #http://www.diputados.gob.mx/sedia/biblio/usieg/usieg_anu_est16/Colima/Poblaci%C3%B3n.xls
 # http://cuentame.inegi.org.mx/monografias/informacion/col/territorio/div_municipal.aspx?tema=me&e=06
    df1 = pd.read_csv("pob_colima.csv")
    df = pd.read_pickle("colima.pkl")
    return df





if __name__ == '__main__':
    main()
