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
from manager import *
import concurrent.futures
from concurrent.futures import as_completed
from collections import Counter
from datetime import datetime
class gameinformer_content(manage):
    def __init__(self):
        self.data = []
        self.mn = manage('https://www.gameinformer.com/')
        self.all_url = self.mn.get_second_crawl()

        external = self.mn.get_external_link()
        r_external = list(filter(('#').__ne__, external))
        self.s_external = []
        for i in r_external:
            try:
                t = i.split('/',3)[2]
                self.s_external.append(t)
            except:
                pass
        self.ref_external =list(filter(('www.gameinformer.com').__ne__, self.s_external))
        print(Counter(self.ref_external))
        # print(len(self.s_external))
        # print('++++++++++++',external)
        print('crawl done')
        
        pattern =  re.compile(r'(https://www.gameinformer.com/(\d+/\d+/\d+|gamer-culture|sweepstakes)/)')
        self.new_url = list(filter(pattern.match,self.all_url))
        self.new_non_dup_url  = []
        [self.new_non_dup_url.append(i) for i in self.new_url if i  not in self.new_non_dup_url]
        r = requests.get('https://www.gamespot.com/').text
        s = BeautifulSoup(r,'html.parser')
        self.lang = s.find_all('html',{'lang':re.compile(r'\w{2}')})[0]['lang']
    def ref_link(self):
        data_ref = []
        count_ex = Counter(self.ref_external)
        for i in count_ex:
            obj = {'name': i ,'total_ref':count_ex[i]}
            data_ref.append(obj)
        return data_ref

    def get_content(self,i):

        
        obj = {}
        text = ''
        req = self.mn.get_req(i)
        soup = self.mn.get_soup(req)
        obj['name'] = i.replace('https://www.','').split('.')[0]
        obj['date'] = datetime.today().strftime('%Y/%m/%d')
        obj['url'] = i 
        for header in soup.find_all('h1'):
            obj['header'] = header.text.replace('\n','').replace('\ ','').strip()

        for k in soup.find_all('div',{'class': re.compile(r'(clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden gi5-body gi5-text-with-summary field__item)')}):
            for p in k.find_all('p'):
                text = text + p.get_text().replace('\n','').replace('\ ','').strip()
        if text == '':
            obj['content'] = 'No Content.'
        else:
            text = self.mn.clean_text1(text)
            obj['content'] = text
            obj['lang'] = self.lang
            total_word = self.mn.total_words(text)
            lenght_total = len(total_word)
            obj['total_word'] = lenght_total

            polarity = self.mn.check_sentiment(text,self.lang)
            obj['sentiment'] = polarity
        

        # self.data.append(obj)
        return obj
        print(time.time() - start)
        print('get_content ****')
        return self.data

    def get_content_manager(self):
        with concurrent.futures.ThreadPoolExecutor(100) as executor:
            results = [ executor.submit(self.get_content, i) for i in self.new_non_dup_url ]
            for result in as_completed(results):
                re = result.result()
                self.data.append(re)
        return self.data
