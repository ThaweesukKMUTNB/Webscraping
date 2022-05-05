from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import nltk
from nltk import sent_tokenize
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from nltk.corpus import stopwords
import string 
from nltk.tokenize import word_tokenize
import concurrent.futures
from concurrent.futures import as_completed
import time
from os import listdir
from os.path import isfile, join
from thai_sentiment import get_sentiment

class manage():
    def __init__(self,url):
        self.domain_url = url
        self.all_url = []
        self.all_url_non_dup=[]
        self.external_link = []
    def get_req(self,url):
        try:
            return requests.get(url, allow_redirects=False,timeout = 5).text
        except:
            return ''

    def get_soup(self,req):
        return BeautifulSoup(req,'html.parser')

    def crawl(self,url):
       
        req = self.get_req(url)
        soup = self.get_soup(req)
        
        for i in soup.find_all('a'):
            
            try:
                if i['href'].startswith('/'):
                    link = urljoin(url,i.get('href'))
                    if link not in self.all_url:
                        self.all_url.append(link)
                    #crawl(link)
                elif i['href'].startswith(url):
                    link = i.get('href')
                    if link not in self.all_url:
                        self.all_url.append(link)
                    #crawl(link)
                else:
                    link = i.get('href')
                    self.external_link.append(link)
                    
            except:
                pass
     
        return self.all_url
    
    def get_external_link(self):
        return self.external_link
    
    def get_second_crawl(self):

        a = self.crawl(self.domain_url)
        print(len(a))
        # [a2.append(i) for i in a if i  not in a2]

        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(100) as executor:
            results = [ executor.submit(self.crawl, i) for i in a ]
           
        
                
        print(time.time() - start)  
        st2 = time.time()
        [self.all_url_non_dup.append(i) for i in self.all_url if i  not in self.all_url_non_dup]
        print(time.time()-st2)
        print('len all_url :',len(self.all_url))
        print(len(self.all_url_non_dup))
        return self.all_url_non_dup
    
    

    def count_keywords(self,sen, keyword):

        self.count =  sen.count(keyword)
        return self.count

    def total_words(self,sen):
        total = word_tokenize(sen)
        self.non_dup_total = []
        [self.non_dup_total.append(i) for i in total if i  not in self.non_dup_total]

        return self.non_dup_total
    
    def check_sentiment(self,sentence,lang):
        self.res = ''
        
        if lang == 'en':
            tb = TextBlob(sentence)
        
            final_pol = tb.sentiment.polarity
            if final_pol > 0 :
                self.res = 'Positive'
            elif final_pol==0:
                self.res = 'Neutral'
            else:
                self.res = 'Negative'
        elif lang == 'th':
            polarity=''
            try: 
                url = "https://api.aiforthai.in.th/ssense"
                
                text = 'สาขานี้พนักงานน่ารักให้บริการดี'
                
                params = {'text':sentence}
                
                headers = {
                    'Apikey': "Dunuya4Yp7V2z0Hrtn2P6PIxKLLIcLOR"
                    }
                
                response = requests.get(url, headers=headers, params=params)
                polarity = response.json()['sentiment']['polarity']
            except:
                self.res = 'Neutral'
            if polarity == 'positive':
                self.res = 'Positive'
            elif polarity == 'neutral':
                self.res = 'Neutral'
            elif polarity == '':
                self.res == 'Neutral'
            else:
                self.res = 'Negative'
            print(self.res)
    
        return self.res

    def to_dataframe(self,data):
    
        df = pd.DataFrame.from_dict(data)
        
        df = df.dropna()
        return df
    def to_csv(self,df,fname):
        df.to_csv(fname,index = False)

    def read_csv(self,fname):
        return pd.read_csv(fname)

    def clean_text1(self,sen):
        # stop_words = stopwords.words("english")
        punct = set(string.punctuation)
        sen = sen.lower()
        # sen = ' '.join([word for word in sen.split(' ') if word not in stop_words])
        sen = sen.encode('ascii', 'ignore').decode()
        sen = re.sub(r'https*\S+', ' ', sen)
        sen = re.sub(r'@\S+', ' ', sen)
        sen = re.sub(r'#\S+', ' ', sen)
        sen = re.sub(r'\'\w+', '', sen)
        sen = "".join([ch for ch in sen if ch not in punct])
        sen = re.sub(r'\w*\d+\w*', '', sen)
        sen = re.sub(r'\s{2,}', ' ', sen)
        return sen

    
    def get_keyword_folder(self):
        mypath = '\\Users\\Nachanon\\Desktop\\Web-scraping\\keyword'
        return [f for f in listdir(mypath) if isfile(join(mypath, f))]
