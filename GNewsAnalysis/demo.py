# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 09:51:20 2019
1. Google news search
2. Keywords extract
3. WordCloud
# 4. Simlarity analysis (iterative search)
Modified from gnewsclient
@author: Chung-Yi Lin
"""
# import the package
import GNewsAnalysis as G

# Create an object
g = G.SearchNews()

# View the initial configuration for Google news search
g.get_config()

# View the options 
g.editions
g.languages
g.orders
g.topics

# Change config
g.orders = "newest"
g.query = "水資源"

# Search the news 
# ToDataframe = False => output dictionary format
# FullExtract = False => the full news content will not be extract. (much faster)
df = g.search(ToDataframe = True, FullExtract = True)

# Extract the keywords. ( using jieba => Chinese)
# Currently only support chinese 
g.articles = df
df2 = g.keywords()

# Form the wordcloud
# Currently only support chinese 
# using title
g.wordcloud(ColName = "title", StopWords = {})
# using news content
g.wordcloud(ColName = "content", StopWords = {})


# [Options] 
# You can form your own jieba dictionary and assign the path
#g.dictpath = file path
# You can assign the font to customize the wordcloud
#g.fontpath = file path






