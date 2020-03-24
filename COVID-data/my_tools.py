import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import datetime


def plot_big(df, legend=True):
    plt.figure(figsize=(15, 10))
    plt.suptitle(title)

    for col in df:
        plt.plot(df.index, df[col], label=col)
    plt.title(df.name)
    
    if legend:
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
    
    dates1 = df1.index.tolist()
    ax = plt.gca()

    formatter = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(formatter)

    locator = mdates.DayLocator()
    ax.xaxis.set_major_locator(locator)
    
    for col in df1:
        plt.plot(dates1, df1[col], label=col)
    plt.title(df1.name)

    plt.subplot(122)
    
    dates2 = df2.index.tolist()
    ax = plt.gca()

    formatter = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(formatter)

    locator = mdates.DayLocator()
    ax.xaxis.set_major_locator(locator)
    
    for col in df2:
        plt.plot(dates2, df2[col], label=col)
    plt.title(df2.name)
    plt.show()


def convert_datetime_to_x(df):
    dates = df.values.tolist()



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


def get_random_val_set(df):
    selection_mask = np.random.rand(len(df)) < 0.8

    train_set = df[selection_mask]
    validation_set = df[~selection_mask]

    return train_set, validation_set