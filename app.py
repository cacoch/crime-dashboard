import streamlit as st
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns



def main():
    st.title("Colima")
    data_load_state = st.text('Loading data...')

    df = load_data()
    data_load_state.text("Done! (using st.cache)")
    st.write("Data sample")
    st.write(df.sample(n=10))
    
    #grp = df.groupby("BIEN JURÍDICO AFECTADO", "MUNICIPIO"
    grp = df.groupby("MUNICIPIO")
    
    fig, ax = plt.subplots()
    for key, gr in grp:
        ax.scatter(gr.DATE, gr.VALUE, label=key, s=0.2 )

    ax.legend()

    st.pyplot(fig)


def load_data():
    df = pd.read_pickle("colima.pkl")
    return df





if __name__ == '__main__':
    main()
