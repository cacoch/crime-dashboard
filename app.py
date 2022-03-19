import streamlit as st
import numpy as np
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import matplotlib.pyplot as plt
import seaborn as sns
from graficas import simple
from geo_graficas import g_simple

global XX
XX = ['A', 'B']

def main():
    #st.title("La estadistica")
    data_load_state = st.text('Loading data...')
    global df
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

        municipios = st.multiselect("Municipio", 
                df['MUNICIPIO'].unique().tolist())

        years = st.multiselect("Año", 
                pd.DatetimeIndex(df['DATE']).year.unique().tolist())

        bienJ = st.multiselect( 'Bien jurídico afectado',
                df['BIEN JURÍDICO AFECTADO'].unique().tolist(),
                key="bienJ")

        X= df[df['BIEN JURÍDICO AFECTADO'].isin(bienJ)]
        tipo2 = st.multiselect('Tipo de delito',
                 options=X['TIPO DE DELITO'].unique().tolist(),
                 key="tipo_del")

        XX= df[df['TIPO DE DELITO'].isin(tipo2)]
        subtipo = st.multiselect('Subtipo de delito', 
         XX['SUBTIPO DE DELITO'].unique().tolist())

        modalidad = st.multiselect('Modalidad', 
         X['MODALIDAD'].unique().tolist())

        st.write("Nombres de columnas y su orden en la table pivote")
        pivot_index = st.multiselect('Columnas de pivote', 
            ['ENTIDAD',
             'MUNICIPIO',
             'BIEN JURÍDICO AFECTADO',
             'TIPO DE DELITO',
             'SUBTIPO DE DELITO',
             'MODALIDAD',
             'DATE'])

        if st.button("Filtrar"):
            st.write("Sooon ...")
            st.write(municipios, years, bienJ, tipo2, subtipo, modalidad)
            df1 = filtro(df, years=years, municipios=municipios, bienJ=bienJ, tipo=tipo2, subtipo=subtipo, modalidad=modalidad)
        

            if "DATE" in pivot_index:
                df1['DATE'] = df1['DATE'].dt.strftime("%Y")

            pivot = pd.pivot_table(
                df1,
                values=['VALUE'],
                #index=['MODALIDAD', 'TIPO', 'SUBTIPO'],
                index= pivot_index,
                aggfunc="sum",
                margins=True
            )
            #pivot = pd.concat([
            #    d.append(d.sum().rename((k, 'Total')))
            #    for k, d in pivot.groupby(level=0)
            #]).append(pivot.sum().rename(('Grand', 'Total')))

            st.dataframe(df1)
            st.write("-------")
            st.write(pivot.to_html() ,unsafe_allow_html=True)


    elif page == 'Graficas':
        st.caption("No seleccionar municipio, quiere decir todos")
        municipios = st.multiselect("Municipio", 
                df['MUNICIPIO'].unique().tolist())

        st.selectbox("Selecciona indicador", ["dummy1", "dummy2", "dummy"])
        st.radio("Metrica", ["Valores absolutos", "Por cada 100k habitantes"])
        if st.button("Grafica"):
            """The selection doesn't works yet!!
                    It's fixed to murders """
            df1 = filtro(df, years=[], municipios=[],
                    bienJ=[], tipo=['Homicidio'], subtipo=[], modalidad=[])
            fig = simple(df1)
            st.pyplot(fig)

    elif page == 'Mapas':
        g_simple()

    st.stop()

def menu_filtro_delito():
    print(st.session_state.bienJ)
    print("tipo del")
    #del st.session_state['tipo_del'] 
    XX = ["x", "y"]

    


    

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
def filtro(ds, years, municipios, bienJ, tipo, subtipo, modalidad):
    
        
    def filter_fn(row):
        if municipios: # check if is empty
            c0 = row['MUNICIPIO'] in municipios
        else:  # is empty, so no filter
            c0 = True

        if bienJ:
            c1 = row['BIEN JURÍDICO AFECTADO'] in bienJ
        else:
            c1 = True
            
        if tipo:
            c2 = row['TIPO DE DELITO'] in tipo
        else:
            c2 = True
        
        if subtipo:
            c3 = row['SUBTIPO DE DELITO'] in subtipo
        else:
            c3 = True
        
        if modalidad:
            c4 = row['MODALIDAD'] in modalidad
        else:
            c4 = True
            
        if years:
            c5 = row['DATE'].year in years 
        else:
            c5 = True

        return c0 & c1 & c2 & c3 & c4 & c5
    
    # filter data
    f = ds.apply(filter_fn, axis=1)
    ds = ds[f]
    print(ds.info())

    return ds

def load_data():
 #http://www.diputados.gob.mx/sedia/biblio/usieg/usieg_anu_est16/Colima/Poblaci%C3%B3n.xls
 # http://cuentame.inegi.org.mx/monografias/informacion/col/territorio/div_municipal.aspx?tema=me&e=06
    df1 = pd.read_csv("pob_colima.csv")
    df = pd.read_pickle("colima.pkl")
    return df





if __name__ == '__main__':
    main()
