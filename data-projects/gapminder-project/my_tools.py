import matplotlib.pyplot as plt
import numpy as np


def plot_df_big(df):
    plt.figure(figsize=(15, 10))

    for col in df:
        plt.plot(df.index, df[col], label=col)
    plt.legend()
    plt.show()


def plot_side_by_side(df1, df2, title):
    plt.figure(figsize=(15, 5))
    plt.suptitle(title)

    plt.subplot(121)
    for col in df1:
        plt.plot(df1.index, df1[col], label=col)
    plt.title(df1.name)
    plt.legend()

    plt.subplot(122)
    for col in df2:
        plt.plot(df2.index, df2[col], label=col)
    plt.title(df2.name)
    plt.legend()
    plt.show()


def normalize_columns(df):
    averages = np.sum(df) / len(df)
    new_df = df / averages

    return new_df
