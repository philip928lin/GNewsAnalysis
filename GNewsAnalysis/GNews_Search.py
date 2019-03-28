# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 09:29:03 2019

@author: Philip
"""
from GNewsAnalysis.utils import editionMap, topicMap, langMap, orderMap
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd
from newspaper import Article
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
import jieba.analyse
import os
"""
Section 1: Search News with Google News Search Engine
"""
class SearchNews:
    def __init__(self, edition='Taiwan', topic='top stories', location=None,
                 query="氣候變遷", language='chinese traditional', order=None):
        '''
        constructor function
        '''
        # list of editions and topics
        self.editions = list(editionMap)
        self.topics = list(topicMap)
        self.languages = list(langMap)
        self.orders = list(orderMap)

        # default parameter values
        self.edition = edition
        self.topic = topic
        self.location = location
        self.query = query
        self.language = language
        self.order = order

        # parameters to be passed in HTTP request
        self.params = {'output': 'atom',
                       'ned': self.edition,
                       'topic': self.topic,
                       'geo': self.location,
                       'q': self.query,
                       'hl': self.language,
                       'order': self.order}
        # jieba and wordcloud
        this_dir, this_filename = os.path.split(__file__)
        self.fontpath = os.path.join(this_dir, "font", "NotoSerifCJKtc-hinted","NotoSerifCJKtc-Black.otf")
        self.dictpath = os.path.join(this_dir,"dict","dict.txt.big" )

    def get_config(self):
        '''
        function to get current configuration
        '''
        config = {
            'edition': self.edition,
            'topic': self.topic,
            'language': self.language,
            'location': self.location,
            'query': self.query,
            'order': self.order
        }
        return config

    def reset(self):
        '''
        function to reset the parameters
        '''
        self.edition = 'Taiwan'
        self.language = 'chinese traditional'
        self.location = None
        self.query = None
        self.topic = 'top stories'
        self.order = None
        
        # jieba and wordcloud
        this_dir, this_filename = os.path.split(__file__)
        self.fontpath = os.path.join(this_dir, "font", "NotoSerifCJKtc-hinted","NotoSerifCJKtc-Black.otf")
        self.dictpath = os.path.join(this_dir,"dict","dict.txt.big" )
        
    def set_params(self):
        '''
        function to set params for HTTP request
        '''
        # setting edition
        try:
            self.params['ned'] = editionMap[self.edition]
        except KeyError:
            print(f"{self.edition} edition not found.\n"
                  f"Use editions attribute to get list of editions.")
            return False
        # setting topic
        try:
            self.params['topic'] = topicMap[self.topic]
        except KeyError:
            print(f"{self.topic} topic not found.\n"
                  f"Use topics attribute to get list of topics.")
            return False
        # setting language
        try:
            self.params['hl'] = langMap[self.language]
        except KeyError:
            print(f"{self.language} language not found.\n"
                  f"Use langugaes attribute to get list of languages.")
            return False
        # setting query
        if self.query is not None:
            self.params['q'] = self.query
            # topic overrides query parameter. So, clearing it.
            self.params['topic'] = None
        # setting location
        if self.location is not None:
            self.params['geo'] = self.location
            # topic overrides location parameter. So, overriding it.
            self.params['topic'] = None
        if self.order is not None:
            self.params['order'] = self.order
        # params setting successful
        return True
    
    def load_feed(self):
        '''
        function to load atom feed
        '''
        url = "https://news.google.com/news"
        resp = requests.get(url, params=self.params)
        soup = BeautifulSoup(resp.content, 'html5lib')
        return soup

    def scrape_feed(self, soup, FullExtract = False):
        '''
        function to scrape atom feed
        '''
        entries = soup.findAll('entry')
        articles = []
        for entry in tqdm(entries):
            article = {}
            content = BeautifulSoup(entry.content.text, 'html5lib')
            article['title'] = content.a.text
            article['media'] = content.font.text
            #article['title'] = entry.title.text
            article['link'] = entry.link['href']
            article['releasedAt'] = entry.updated.text
            if FullExtract:
                try:
                    OrgNews = Article(article['link'])
                    OrgNews.download()
                    OrgNews.parse()
                    article['authors'] = OrgNews.authors
                    article['content'] = OrgNews.text
                    article['image'] = OrgNews.top_image
                    article['video'] = OrgNews.movies
                except:
                    print("\nError in extract ",article['link'] + "\n")
                    article['authors'] = None
                    article['content'] = None
                    article['image'] = None
                    article['video'] = None
            articles.append(article)
        try:
            if len(articles) == 0:
                raise NotFound
        except NotFound:
                print("The articles for the given response are not found.")
                return
        return articles
    
    def search(self, ToDataframe = True, FullExtract = False):
        '''
        function to fetch news articles
        '''
        status = self.set_params()
        # params not set properly
        if status is False:
            return
        soup = self.load_feed()             # Request
        # Option for obtain orginal news content
        if FullExtract:
            print("This will take a while...\n")
            articles = self.scrape_feed(soup, FullExtract = True)   # Extract full article
        else:
            articles = self.scrape_feed(soup)   # Extract
        
        self.articles = pd.DataFrame(articles)
        
        if ToDataframe:
            return pd.DataFrame(articles)
        else:
            return articles
        
    def keywords(self):
        # Frequency (Chinese)
        jieba.set_dictionary(self.dictpath)
        df = self.articles
        def nlp_jieba(ColName):
            jiebalist = []
            for i in range(df.shape[0]):
                if df.loc[i,ColName] is None:
                    jiebalist.append(None)
                    continue
                jiebalist.append(jieba.analyse.extract_tags(df.loc[i,ColName], topK=20, withWeight=True))
            df[ColName+"_jieba"] = jiebalist
        for i in ["title", "content"]:
            if i in list(df):
                nlp_jieba(i)
        self.articles = df
        return df
    
    
    def wordcloud(self, ColName = "title", StopWords = None):
        terms = []
        df = self.articles
        ColName1 = ColName+"_jieba"
        if ColName1 not in list(df):
            df = self.keywords()
        for i in df[ColName1]:
            if i is not None:
                terms = terms + i
        terms = [i[0] for i in terms]
        words = ",".join(terms)        
        # 設定停用字(排除常用詞、無法代表特殊意義的字詞)
        stopwords = {}.fromkeys(StopWords)
        # 產生文字雲
        wc = WordCloud(font_path=self.fontpath, #設置字體
                       background_color="white", #背景顏色
                       max_words = 2000 ,        #文字雲顯示最大詞數
                       width=800, height=400,    # Rsolution
                       stopwords=stopwords)      #停用字詞
        wc.generate(words)
        # 視覺化呈現
        plt.figure()
        plt.imshow(wc)
        plt.axis("off")
        plt.title("Wordcloud of "+ColName)
        plt.show()
        
        
# Dealing Exception error
class NotFound(Exception):
    """Raised when the list articles in the function scapefeed() is empty"""
    pass