#imports
import pandas as pd
import numpy as np
import requests
import re
import sqlite3
import os
import logging
from datetime   import datetime
from bs4        import BeautifulSoup
from sqlalchemy import create_engine

##data_collection - products showcase
def products_showcase(url, headers):

    #API request - page 1
    page  = requests.get(url, headers=headers)

    #beautiful soup
    soup = BeautifulSoup(page.text, 'html.parser')

    #collect all pages
    total_items = soup.find_all('h2', class_='load-more-heading')[0].get('data-total')
    items_shown = soup.find_all('h2', class_='load-more-heading')[0].get('data-items-shown')
    numero_paginas = round(int(total_items)/int(items_shown))

    #API request all pages
    url2 = url + '?page-size=' + str(int(numero_paginas)*int(items_shown))
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    page  = requests.get(url2, headers=headers)

    #Beautiful soup object
    soup2 = BeautifulSoup(page.text, 'html.parser')

    #table with all products
    products = soup2.find('ul', class_ = 'products-listing small')

    #list with id, category
    products_list = products.find_all('article', class_ = 'hm-product-item')

    #id
    list_id = []
    for i in range (len(products_list)):
        product_id = products_list[i].get('data-articlecode') 
        list_id.append(product_id)  

    #category
    list_category = []
    for i in range (len(products_list)):
        product_category = products_list[i].get('data-category')
        list_category.append(product_category)
                            
    #name
    product_list_2 = products.find_all('a',class_='link')
    list_name = []
    for i in range (len(product_list_2)):
        name = product_list_2[i].get_text()
        list_name.append(name)

    #price
    product_list_3 = products.find_all('span', class_ = 'price regular')
    list_price = []
    for i in range(len(product_list_3)):
        price = product_list_3[i].get_text()
        list_price.append(price)

    #create dataframe with collected data
    showcase = pd.DataFrame([list_id, list_category, list_name,list_price]).T
    showcase.columns = (['Art. No.', 'category','product_name', 'price'])
    
    return showcase


##data collection - all products
def data_collection_all_products(showcase, headers):

    #empty dataframe
    df_compositions = pd.DataFrame()

    #df_pattern
    cols = ['Art. No.', 'Composition', 'Fit']
    df_pattern = pd.DataFrame(columns=cols)

    #lists
    for j in range (len(showcase)): 
        #API request
        url3 = 'https://www2.hm.com/en_us/productpage.' + showcase.loc[j, 'Art. No.']+ '.html'
        logger.debug('Product: %s', url3 )
        
        #beatifulsoup object
        page  = requests.get(url3, headers=headers)
        soup_item = BeautifulSoup(page.text, 'html.parser')

        #colors
        colors = []
        product_list = soup_item.find_all ('a', class_ = 'filter-option miniature active') + soup_item.find_all('a', class_ = 'filter-option miniature')
    
        #get text - color
        for i in range (len(product_list)):
            color = product_list[i].get('data-color')
            colors.append(color) 
    
        #get text - id
        ids = []
        for i in range(len(product_list)):
            id_item = product_list[i].get('data-articlecode')
            ids.append(id_item)
    
        #dataframe
        df_colors = pd.DataFrame([ids, colors]).T
        df_colors.columns = (['Art. No.', 'Color_Name'])
    
        #collect data from each product/color
        for color in range (len(df_colors)):
        
            #API request
            url4 = 'https://www2.hm.com/en_us/productpage.'+ df_colors.loc[color, 'Art. No.'] +'.html'
            logger.debug('Color: %s', url4)
            
            #beatifulsoup object
            page  = requests.get(url4, headers=headers)
            soup_item = BeautifulSoup(page.text, 'html.parser')
 
            #names
            names = soup_item.find('h1', class_='primary product-item-headline').get_text()
        
            #prices
            prices = soup_item.find('div', class_ = 'primary-row product-item-price').get_text()
            prices = re.findall( r'\d+\.?\d+', prices)[0]
        
            #composition
        
            #extract data
            list1 = soup_item.find_all('div', class_='details-attributes-list-item')
        
            #get and clean text
            elements = []
            for i in range (len(list1)):
                element = list(filter(None,soup_item.find_all('div', class_='details-attributes-list-item')[i].get_text().split('\n')))
                elements.append(element)
        
        
            #transpose and rename dataframe 
            df_composition = pd.DataFrame(elements).T
            df_composition.columns = df_composition.iloc[0]
    
            #delete first row, get columns
            df_composition = df_composition.iloc[1: ]
   
            #delete rows with 'NA' in all columns.
            df_composition = df_composition.dropna(axis = 0, how = 'all')
    
            #fill NA with the information from the line above 
            df_composition = df_composition.fillna(method='ffill')
    
            #remove'Pocket lining:', 'Lining:' , 'Shell:' , 'Pocket:'
            df_composition['Composition'] = df_composition['Composition'].replace('Pocket lining:', '',regex=True)
            df_composition['Composition'] = df_composition['Composition'].replace('Lining:', '',regex=True)
            df_composition['Composition'] = df_composition['Composition'].replace('Shell:', '',regex=True)
            df_composition['Composition'] = df_composition['Composition'].replace('Pocket:', '',regex=True)
    
            #garantee the same number of columns
            df_composition = pd.concat ([df_pattern, df_composition], axis=0)
    
            #add names and prices
            df_composition['Product_Name'] = names
            df_composition['Price'] = prices
        
            #merge df_colors and df_composition
            df_composition = pd.merge(df_composition[['Art. No.','Product_Name', 'Price','Fit','Composition']], df_colors, how='left',on='Art. No.')
            df_compositions = pd.concat([df_compositions, df_composition], axis=0)              
        
        
    #add collected data to dataframe and drop duplicates
    df_compositions['Style_Code'] = df_compositions['Art. No.'].apply(lambda x: x[:-3])
    df_compositions['Color_Code'] = df_compositions['Art. No.'].apply(lambda x: x[-3:])
    df_compositions.drop_duplicates(subset=None, keep="first", inplace=True)
    df_compositions['Scrapy_Datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return df_compositions


##Data Cleaning
def data_cleaning(df_compositions):

    #copy
    data = df_compositions.copy()

    #product name rename
    data['Product_Name'] = data['Product_Name'].str.replace('\n', '')
    data['Product_Name'] = data['Product_Name'].str.replace('\t', '')
    data['Product_Name'] = data['Product_Name'].str.replace('  ', '')
    data['Product_Name'] = data['Product_Name'].str.replace(' ', '_').str.lower()

    #product price
    data['Price'] = data['Price'].astype(float)

    #fit
    data['Fit'] = data['Fit'].str.replace(' ', '_').str.lower()

    #color
    data['Color_Name'] = data['Color_Name'].str.replace(' ', '_').str.lower()


    #composition
    #break composition by comma - (expand true change it into dataframe)
    df1 = data['Composition'].str.split(',',expand=True).reset_index(drop=True)

    #Cotton |Polyester |Spandex 
    #Create empty dataframe with same length as data
    df_ref = pd.DataFrame(index=np.arange(len(data)), columns=['Cotton','Polyester','Spandex'])

    #cotton - There`s cotton in column 0 and 1 from df1
    df_cotton_0 = df1.loc[df1[0].str.contains('Cotton', na = True), 0]
    df_cotton_1 = df1.loc[df1[1].str.contains('Cotton', na = True), 1]
    #combine
    df_cotton = df_cotton_0.combine_first(df_cotton_1)
    #rename dataframe
    df_cotton.name = 'Cotton'
    #concat
    df_ref = pd.concat([df_ref, df_cotton], axis=1)
    #drop duplicated column
    df_ref = df_ref.iloc[:,~df_ref.columns.duplicated(keep='last')]


    #Polyester - there`s polyester only in column 0 from df1
    df_polyester_0 = df1.loc[df1[0].str.contains('Polyester',na=True),0]
    #rename dataframe
    df_polyester_0.name = 'Polyester'
    #concat
    df_ref = pd.concat([df_ref, df_polyester_0], axis=1)
    #drop duplicated column
    df_ref = df_ref.iloc[:,~df_ref.columns.duplicated(keep='last')]

    #Spandex - there`s spandex only on column 1 from df1
    df_spandex_1 = df1.loc[df1[1].str.contains('Spandex',na=True),1]
    #rename dataframe
    df_spandex_1.name = 'Spandex'
    #concat
    df_ref = pd.concat([df_ref, df_spandex_1], axis=1)
    #drop duplicated column
    df_ref = df_ref.iloc[:,~df_ref.columns.duplicated(keep='last')]

    #join df_ref wih product_id
    df_aux = pd.concat([data['Art. No.'].reset_index(drop=True), df_ref],axis=1)

    #format composition data
    df_aux['Cotton'] = df_aux['Cotton'].apply( lambda x: int( re.search( '\d+', x ).group(0) ) / 100 if pd.notnull( x ) else x )
    df_aux['Polyester'] = df_aux['Polyester'].apply( lambda x: int( re.search( '\d+', x ).group(0) ) / 100 if pd.notnull( x ) else x )
    df_aux['Spandex'] = df_aux['Spandex'].apply( lambda x: int( re.search( '\d+', x ).group(0) ) / 100 if pd.notnull( x ) else x )

    #group by product id and get maximum value of each material
    df_aux = df_aux.groupby('Art. No.').max().reset_index().fillna(0)

    #merge data with df_aux
    data = pd.merge( data, df_aux, on = 'Art. No.', how = 'left')

    #drop_columns
    data = data.drop(columns='Composition', axis=1)

    #drop duplicates
    data = data.drop_duplicates()
    data.rename(columns = {'Art. No.':'Art_No'}, inplace = True)
    
    return data

##data insert into datawarehouse - sqlite
def data_insert(data):
    data_insert = data[['Art_No',
                        'Product_Name',
                        'Color_Name',
                        'Color_Code',
                        'Style_Code',
                        'Fit',
                        'Price',
                        'Cotton',
                        'Polyester',
                        'Spandex',
                        'Scrapy_Datetime']]
    
                    

    #create database connection
    conn = create_engine('sqlite:///databasehm.sqlite', echo=False)
    #data insert
    data_insert.to_sql('men_jeans_hm', con = conn, if_exists='append', index = False)
    return None

if __name__ == '__main__':
    #logging
    if not os.path.exists('Log'):
        os.makedirs('Log')
    logging.basicConfig(
        filename = 'Log/webscrapin_hm.txt',
        level = logging.DEBUG,
        format = '%(asctime)s - %(levelname)s -  %(name)s -  %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S'
    )
    
    logger = logging.getLogger('webscraping_hm')
    
    #parameters
    url = 'https://www2.hm.com/en_us/men/products/jeans.html'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    
    #data_collection - products showcase
    showcase = products_showcase(url,headers)
    logger.info('data collection - products showcase done')
    
    
    #data collection - all products
    df_compositions = data_collection_all_products(showcase, headers)
    logger.info('data collection - all products done')
    
    #data cleaning
    data = data_cleaning(df_compositions)
    logger.info('data cleaning done')
    
    #data insert into datawarehouse - sqlite
    data_insert(data)
    logger.info('data insert into datawarehouse done')
    
    