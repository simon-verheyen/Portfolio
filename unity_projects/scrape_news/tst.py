import pandas as pd
#import data_support
import create_searches
import newsapi_main
#import newsapi_data_search_v3
from newsapi import NewsApiClient
#import numpy as np
#from datetime import datetime, timedelta


def main():

    df = pd.read_csv('data_sources_newsapi')


    print(df[df['language']=='en']['id'].tolist())



main()
