import matplotlib.pyplot as plt
import numpy as np


def plot_big(df,  title=''):
    plt.figure(figsize=(15, 10))
    plt.suptitle(title)

    for col in df:
        plt.plot(df.index, df[col], label=col)
    plt.title(df.name)
    plt.legend()
    plt.show()


def plot_small(df,  title=''):
    plt.figure(figsize=(15, 5))
    plt.suptitle(title)

    for col in df:
        plt.plot(df.index, df[col], label=col)
    plt.title(df.name)
    plt.legend()
    plt.show()


def plot_side_by_side(df1, df2, title=''):
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


def plot_dict(Dict):
    temp_name = ''
    for entry in Dict:
        if not temp_name:
            temp_name = entry
        else:
            plot_side_by_side(Dict[temp_name], Dict[entry])
            temp_name = ''

    if temp_name:
        plot_small(Dict[temp_name])


def normalize(data):
    if type(data) is dict:
        norm_dict = {}
        all_cache = {}
        for entry in data:
            df_norm, cache = normalize(data[entry])
            norm_dict[entry] = df_norm
            all_cache[entry] = cache

        return norm_dict, all_cache

    else:
        averages = np.sum(data) / len(data)
        stand_div = np.std(data, axis=0)

        new_df = (data - averages) / stand_div
        new_df.name = data.name

        cache = (averages, stand_div)

        return new_df, cache


def denormalize(data, cache):
    if type(data) is dict:
        Dict = {}
        for entry in data:
            df = denormalize(data[entry], cache[entry])
            Dict[entry] = df

        return Dict

    else:
        average = cache[0]
        stand_div = cache[1]

        new_df = data * stand_div + average
        new_df.name = data.name

        return new_df


def show_content(data):
    if type(data) == dict:
        for entry in data:
            show_content(entry)

    else:
        print("Dataset has", data.shape, "entries.")
        print(f"Data starts from: {data.index[0]}, until {data.index[-1]}")
        print(f"\n\t{'Column':20s} | {'Type':8s} | {'Min':12s} | {'Max':12s}\n")
        for col_name in data.columns:
            col = data[col_name]
            print(f"\t{col_name:20s} | {str(col.dtype):8s} | {col.min():12.1f} | {col.max():12.1f}")

        print('')
