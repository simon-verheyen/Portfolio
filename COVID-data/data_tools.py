import matplotlib.pyplot as plt
import numpy as np
import matplotlib


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


def get_random_val_set(df):
    selection_mask = np.random.rand(len(df)) < 0.8

    train_set = df[selection_mask]
    validation_set = df[~selection_mask]

    return train_set, validation_set


def heatmap(data, row_labels, col_labels, ax=None, cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1] + 1) - .5, minor=True)
    ax.set_yticks(np.arange(data.shape[0] + 1) - .5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}", textcolors=["black", "white"], threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A list or array of two color specifications.  The first is used for
        values below a threshold, the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max()) / 2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts


def plot_heatmap(df, size=(11, 9)):
    corr = np.array(df.corr())
    fig, ax = plt.subplots(figsize=size)

    if df.name:
        im, cbar = heatmap(corr, df.columns, df.columns, ax=ax, cmap="RdPu", cbarlabel=df.name)
    else:
        im, cbar = heatmap(corr, df.columns, df.columns, ax=ax, cmap="RdPu")
    _ = annotate_heatmap(im)

    fig.tight_layout()
    plt.show()
