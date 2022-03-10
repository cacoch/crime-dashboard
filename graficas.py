
import matplotlib.pyplot as plt
import pandas as pd

def simple(df):
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(df['DATE'], df['VALUE'])

    return fig


