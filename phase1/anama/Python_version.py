#conda install -c anaconda nltk
#conda install -c anaconda beautifulsoup4
#conda install -c anaconda lxml

import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import re
import scipy as s


otto=pd.read_excel('/leuphona_datensatz.xlsx')
otto.head()

############Function to clean data

def clean (x):    
    #change to lower case
    x=x.str.lower()

    #Remove nulls
    x = x[~pd.isnull(x)]
    x.index=range(len(x))


    #remove punctuation
    z = pd.Series(s.zeros(len(x)))
    for i in range(len(x)):
        z[i] = re.sub(r'[?|$|*|:|>|<|=|,|\|/|"|(|)|.|+|»|«|!]',r'',x[i])

    #tokenize
    y = pd.Series(s.zeros(len(z)))
    for i in range(len(z)):
        y[i] = word_tokenize(z[i])
       
    #remove words less than 2 characters
    for j in range(len(y)):
        for i in range(len(y[j])):
            if len(y[j][i])<3:
                y[j][i]=""
        
    #remove stop and exclude words
    exclude_words= set(('ja','nein','cm','mehr','oben','','bitte','sellingpoints'))
    stop = set(stopwords.words("german"))
    stops=stop|exclude_words

    w= pd.Series(s.zeros(len(y)))
    for j in range(len(y)):
        w[j]=[i for i in y[j] if i not in stops]
    return w


#########Keywords by search term

#change to lower case
otto.searchterm=otto.searchterm.str.lower()

#clean description and product name data
clean_description=clean(otto[otto.searchterm=='tablet']['product_description'])

clean_product_name=clean(otto[otto.searchterm=='tablet']['product_name'])

#clean selling points data

sellp=otto[otto.searchterm=='tablet']['product_sellingpoints']

join_sellp = sellp.str.cat(sep=',')
soup_sellp=BeautifulSoup(join_sellp, "lxml")

text_selling_points=(soup_sellp.text)
selling_points= pd.Series(s.zeros(1))
selling_points[0]=text_selling_points


clean_selling_point=clean(selling_points)

#join outputs
join_descriptions = clean_description.apply(pd.Series).stack().reset_index(drop=True)

join_product_name = clean_product_name.apply(pd.Series).stack().reset_index(drop=True)

join_selling_point = clean_selling_point.apply(pd.Series).stack().reset_index(drop=True)

join_total_output = pd.concat([join_descriptions,join_product_name,join_selling_point])

#Show results by column
results_description = pd.crosstab(join_descriptions, columns="count")  
results_description.sort_values(by=['count'], ascending=False)

results_product = pd.crosstab(join_product_name, columns="count")  
results_product.sort_values(by=['count'], ascending=False)

results_selling_points = pd.crosstab(join_selling_point, columns="count")  
results_selling_points.sort_values(by=['count'], ascending=False)

# Results total output
results = pd.crosstab(join_total_output, columns="count")  
results.sort_values(by=['count'], ascending=False)
