import pandas as pd
import textblob
import tweepy as tw
import os
import pytz
from datetime import datetime
from datetime import date
import pythainlp
from nltk.corpus import stopwords
#from nltk.tokenize import sent_tokenize, word_tokenize
from pythainlp import sent_tokenize, word_tokenize
from textblob import TextBlob, Word
from nltk.corpus import stopwords
import nltk
from pythainlp.corpus import thai_stopwords
import re
import requests
import json
import altair as alt
import altair_viewer

class tweet():
	def __init__(self,keyword,sdate,edate,lan):
		self.consumer_key= 'GNH7m8k9MeIxkZb3YaRGwpMre'
		self.consumer_secret= '8uzoyRyJMcVubOZ8dTUHfDAQ6cMbrBzgzznFuKPrpgUYDo2lch'
		self.access_key= '713365995138605056-5SX8RkJetUwEQMBpDxVyaZ0wJZNTTvn'
		self.access_secret= 'xPOUS8ryM6Xxqr9mJXkxX5JpKtPlIEn9AvIAsYFyoZCpm'
		self.auth = tw.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.access_key, self.access_secret)
		self.api = tw.API(self.auth, wait_on_rate_limit=True)
		self.keyword = keyword
		self.sdate = sdate
		self.edate = edate
		self.lan = lan
		self.date = date.today().strftime("%Y-%m-%d")
		self.path = "E:\\Users\\glory\\OneDrive\\Documents\\Project\\twitterDB"

		
		

	def stop_word(self,keyword):
		new_stopwords = ["'s","’","https","n't",'’ s','’ m',' ','\n','#','.','/','https','’ t','’ ve']
		stpwrd = nltk.corpus.stopwords.words('english')
		stpwrd.extend(keyword)
		stpwrd.extend(keyword.lower())
		stpwrd.extend(new_stopwords)
		return stpwrd
	def remove_url(self,txt):
		return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

	def remove_url_th(self,txt):

		return " ".join(re.sub("([^\u0E00-\u0E7Fa-zA-Z' ]|^'|'$|''|(\w+:\/\/\S+))", "", txt).split())

	def sentiment(self,text):
		res = TextBlob(text)
		sentiment = res.sentiment.polarity

		return sentiment
	def sentiment_th(self,text):
		url = "https://api.aiforthai.in.th/ssense"
		params = {'text':text}
 
		headers = {
			'Apikey': "0sbMxuqUH06Pm2VwV8bvEMJlrKFr4sDy"
			}

		response = requests.get(url, headers=headers, params=params)
		res = response.json() 
		#print(res)

		sentiment_text = res['sentiment']['polarity']
		sentiment = res['sentiment']['score']
		if sentiment == '0':
			sentiment_text = 'neutral'
		return sentiment_text

	def get_data(self,date):
		self.data = []
		print('date',date)
		keyword = self.keyword + "-filter:retweets"
		date_edit = datetime.strptime(date,"%Y-%m-%d")
		item = 0
		if self.lan == 'en':
			item = 500
		else :
			item = 100
		tweets = tw.Cursor(self.api.search_tweets,q = keyword, 
		lang =self.lan,
		until=date_edit.strftime("%Y-%m-%d"),
		tweet_mode='extended',count = 100,
		result_type ='recent').items(item)
		
		list_tw = [tweet for tweet in tweets]
		print('len tweet :',len(list_tw))
		for tweet in list_tw:
			time = tweet.created_at
			tz = pytz.timezone('Asia/Bangkok')
			timeth = time.astimezone(tz)

			if timeth.strftime("%Y-%m-%d") == date :
				temp = {}
				username = tweet.user.screen_name
				location = tweet.user.location
				hashtags = tweet.entities['hashtags']
				hashtext = list()
				for j in range(0, len(hashtags)):
					hashtext.append(hashtags[j]['text'])
				fulltext = tweet.full_text
				rtwcount = tweet.retweet_count
				fvcount = tweet.favorite_count

				temp['Keyword'] = self.keyword
				temp['Language'] = self.lan
				temp['Username'] = username
				temp['Location'] = location
				temp['Hashtags'] = hashtext
				temp['Fulltext'] = fulltext
				temp['Create at'] = timeth.strftime("%m/%d/%Y")

				if self.lan == "en":
					#temp['Sentiment Value'] = self.sentiment(fulltext)
					if self.sentiment(fulltext) > 0:
						temp['Sentiment']= 'positive'
					elif self.sentiment(fulltext) < 0:
						temp['Sentiment'] = 'negative'
					else:
						temp['Sentiment'] = 'neutral'
				else :
					cleantext = self.remove_url_th(fulltext)
					df_senti = self.sentiment_th(cleantext)
					#temp['Sentiment Value'] = df_senti[1]
					temp['Sentiment'] = df_senti

				temp['Totalretweet'] = rtwcount
				temp['Totalfavorite']= fvcount
				self.data.append(temp)
		

			else :
				pass

		return self.data

	def doubleclick_word(self,path):
		self.df = pd.read_csv(path)
		count_word = {}
		self.wordlist = []
		for i in self.df['Fulltext']:
			fulltext = i
			text = self.remove_url(fulltext)
			textbb = TextBlob(text)
			clean_word = textbb.noun_phrases
			text_ns = [item for item in clean_word]
			for w in text_ns:
				if w in count_word:
					count_word[w] +=1
				else:
					count_word[w] = 1
		cw1 = sorted(count_word.items(), key=lambda x: x[1],reverse=True)
		for i in cw1:
			temp = {}
			temp['Words'] = i[0]
			temp['frequency'] = i[1]
			self.wordlist.append(temp)
			self.wordlist = self.count_word_value()
			self.dfword = self.to_dataframe(self.wordlist)
		return self.dfword


	def count_word_value(self):
		range_date = pd.date_range(self.sdate,self.edate,freq='d')
		count_word = {}
		self.wordlist = []
		stop=list(thai_stopwords())
		stop.append(' ')
		for d in range_date:
			date = d.strftime("%Y-%m-%d")
			newpath = os.path.join(self.path, self.keyword)
			newpath_2 = os.path.join(newpath, self.lan)
			filename = newpath_2 + "\\" + self.keyword +"("+ date +")" + "-" + self.lan + ".csv"
			self.df = pd.read_csv(filename)
			for i in self.df['Fulltext']:
				if self.df['Language'][1] == 'en':
					fulltext = i
					text = self.remove_url(fulltext)
					textbb = TextBlob(text)
					clean_word = textbb.noun_phrases
					text_ns = [item for item in clean_word]
					for w in text_ns:
						if w in count_word:
							count_word[w] +=1
						else:
							count_word[w] = 1

				else :
					fulltext = i
					text = self.remove_url_th(fulltext)
					text2 = word_tokenize(text, engine='newmm')
					text4= [item for item in text2 if item not in stop]
					for w in text4:
						if w in count_word:
							count_word[w] +=1
						else:
							count_word[w] = 1
		cw1 = sorted(count_word.items(), key=lambda x: x[1],reverse=True)
		for i in cw1:
			temp = {}
			temp['Words'] = i[0]
			temp['frequency'] = i[1]
			self.wordlist.append(temp)
		#print(self.wordlist)
		return self.wordlist[:20]


		

	
	def get_data_on_date(self):
		range_date = pd.date_range(self.sdate,self.edate,freq='d')
		print(range_date)
		all_file = []
		count_word = []
		for i in range_date:
			newpath = os.path.join(self.path, self.keyword)
			newpath_2 = os.path.join(newpath, self.lan)
			date = i.strftime("%Y-%m-%d")
			filename = newpath_2 + "\\" + self.keyword +"("+ date +")" + "-" + self.lan + ".csv"
			self.search_db(date)
			
			all_file.append(filename)
			print(i)
		self.wordlist = self.count_word_value()
		self.dfword = self.to_dataframe(self.wordlist)
		self.df = pd.concat(map(pd.read_csv, all_file), ignore_index=True)

		return self.df,self.dfword


		


	def to_dataframe(self,data):
		return pd.DataFrame.from_dict(data)

	#def to_csv(self,df,filename):
		#df.to_csv(filename ,index = False)

	#def count_word(self,clean_text):



	def search_db(self,date):

		
		filename = self.keyword +"("+ date +")" + "-" + self.lan + ".csv"
		keyword_folder = os.listdir(self.path)
		
		if self.keyword not in keyword_folder:
			os.mkdir(os.path.join(self.path, self.keyword))
			newpath =  os.path.join(self.path, self.keyword)
			os.mkdir(os.path.join(newpath, self.lan))
			newpath_2 =  os.path.join(newpath, self.lan)
			data = self.get_data(date)
			self.df = self.to_dataframe(data)
			self.df.to_csv(newpath_2 + "\\" + filename , index = False,encoding = 'utf-8-sig')
		else:
			newpath =  os.path.join(self.path, self.keyword)
			lan_folder = os.listdir(newpath)
			self.wordlist = []
			if self.lan not in lan_folder:
				os.mkdir(os.path.join(newpath, self.lan))
				newpath_2 =  os.path.join(newpath, self.lan)
				file_list = os.listdir(newpath_2)
				data = self.get_data(date)
				self.df = self.to_dataframe(data)
				self.df.to_csv(newpath_2 + "\\" + filename , index = False,encoding = 'utf-8-sig')
			else :
				newpath_2 =  os.path.join(newpath, self.lan)
				file_list = os.listdir(newpath_2)
				if filename in file_list:
					self.df = pd.read_csv(newpath_2 + "\\" + filename)

				else :
					data = self.get_data(date)
					self.df = self.to_dataframe(data)
					self.df.to_csv(newpath_2 + "\\" + filename , index = False,encoding = 'utf-8-sig')


		return self.df

	def plot(self,path):
		x = ['positive','neutral','negative']
		p = 0 
		nu = 0 
		ng = 0
		y = []
		percent = []
		df = pd.concat(map(pd.read_csv, path), ignore_index=True)
		posi = df[(df['Sentiment'] == 'positive')]['Sentiment'].count()
		p += posi
		neu = df[(df['Sentiment'] == 'neutral')]['Sentiment'].count()
		nu += neu
		neg =df[(df['Sentiment'] == 'negative')]['Sentiment'].count()
		ng += neg
		y.append(p)	
		y.append(nu)
		y.append(ng)
		all = df['Sentiment'].count()
		percent_p = p / all * 100
		format_p = "{:.2f}".format(percent_p)
		percent.append(format_p)
		percent_nu = nu / all * 100
		format_nu = "{:.2f}".format(percent_nu)
		percent.append(format_nu)
		percent_ng = ng / all * 100
		format_ng = "{:.2f}".format(percent_ng)
		percent.append(format_ng)		
		categories = x
		values = y
		
		print('xxxxxxxxxxxxxxxxxxxxxxxx',categories,values)
		source = pd.DataFrame({"category": categories, "value": values,"percent": percent})

		circle = alt.Chart(source).encode(
    	theta=alt.Theta(field="value", type="quantitative"),
    	color=alt.Color(field="category", type="nominal"),tooltip = ["category","value","percent"]
		).resolve_scale(theta = 'independent')

		self.chart = circle.mark_arc(outerRadius=120) 
       # text = base.mark_text(radius=140, size=20).encode(text="Region:N")
		return self.chart
			

class click():

	def __init__(self,path):
		
		self.path = path

	def remove_url(self,txt):
		return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

	def remove_url_th(self,txt):

		return " ".join(re.sub("([^\u0E00-\u0E7Fa-zA-Z' ]|^'|'$|''|(\w+:\/\/\S+))", "", txt).split())

	def to_dataframe(self,data):
		return pd.DataFrame.from_dict(data)

	def doubleclick(self):
		self.df = pd.read_csv(self.path)
		count_word = {}
		self.wordlist = []
		for i in self.df['Fulltext']:
			fulltext = i
			text = self.remove_url(fulltext)
			textbb = TextBlob(text)
			clean_word = textbb.noun_phrases
			text_ns = [item for item in clean_word]
			for w in text_ns:
				if w in count_word:
					count_word[w] +=1
				else:
					count_word[w] = 1
		cw1 = sorted(count_word.items(), key=lambda x: x[1],reverse=True)
		for i in cw1:
			temp = {}
			temp['Words'] = i[0]
			temp['frequency'] = i[1]
			self.wordlist.append(temp)
			self.wordlist = self.count_word_value()
			self.dfword = self.to_dataframe(self.wordlist)
		return self.dfword

	def count_word_value(self):
		count_word = {}
		self.wordlist = []
		self.df = pd.read_csv(self.path)
		for i in self.df['Fulltext']:
			fulltext = i
			text = self.remove_url(fulltext)
			textbb = TextBlob(text)
			clean_word = textbb.noun_phrases
			text_ns = [item for item in clean_word]
			for w in text_ns:
				if w in count_word:
					count_word[w] +=1
				else:
					count_word[w] = 1
		cw1 = sorted(count_word.items(), key=lambda x: x[1],reverse=True)
		for i in cw1:
			temp = {}
			temp['Words'] = i[0]
			temp['frequency'] = i[1]
			self.wordlist.append(temp)
		
		return self.wordlist
			
	
#data = tweet('เกม',"2022-04-19","2022-04-19",'th')
#data.get_data_on_date()
			


		



			

			

