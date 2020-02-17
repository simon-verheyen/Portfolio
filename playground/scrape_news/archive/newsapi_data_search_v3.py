from urllib.request import urlopen  # Needed for accessing urls
import json  # Needed to process json
import pandas as pd
import datetime

""" Mke delta_time an hour and set everything up from that!!! """

# Will use criteria (keyword, country, category) to create url
def get_json(keyword, source, period, page):

    url_start = 'https://newsapi.org/v2/everything?'
    url_end = 'apiKey=6452f6e1b7bf430eb07477bbe23353c4'

    url_mid = 'sortBy=publishedAt&'
    url_mid += 'pageSize=20&'

    url_mid = 'q=' + keyword + '&'
    url_mid += 'page=' + str(page) + '&'

    if source == 0:
        url_mid += 'source=' + str(source) + '&'

    from_param, to_param = get_times()

    url_mid += 'from=' + from_param + '&'
    url_mid += 'to=' + to_param + '&'


    # Combine url pieces to create completed url
    url = url_start + url_mid + url_end

    print(url)
    response = urlopen(url)
    raw_data = response.read().decode("utf-8")

    return json.loads(raw_data)


# json data gets converted to pandas data-frame for ease of data access/queries
def process_json(json_data):
    # Data attributes that will be collected
    amount = json_data['totalResults']
    data_collection = {'source_name': [], 'author': [], 'title': [], 'publishedAt': [], 'description': [], 'content': []}

    # Per article will extract the wanted attributes and add it to the corresponding data array
    # Filling the arrays in same order of entries
    for article in json_data['articles']:
        for info in article:
            if info == 'source':
                data_collection['source_name'].append(article[info]['name'])
            elif info in data_collection:
                data_collection[info].append(article[info])

    # Transforms the dict into a pandas data-frame
    df = pd.DataFrame(data_collection)

    return df, amount


def get_times():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    from_param = yesterday.strftime("%Y-%m-%d")
    to_param = today.strftime("%Y-%m-%d")

    return from_param, to_param


def get_page_data(keyword, source, period, page):
    try:
        json_data = get_json(keyword, source, period, page)

    except:
        print("can't get json_data")
        return

    df, total_amount = process_json(json_data)

    return df, total_amount


def search_everything(keyword, source, period):
    page = 1

    df_total, amount = get_page_data(keyword, source, period, page)
    print(amount)

    while amount > 0:
        page += 1
        amount -= 20

        df_page, amount = get_page_data(keyword, source, period, page)
        df_total = pd.merge(df_total, df_page, how='outer')
        print(df_total.shape)

    return df_total
