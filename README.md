# GNewsAnalysis
Python package for google news search and analysis.

## Dscription
GNewsAnalysis is modified from [gnewsclient](https://github.com/nikhilkumarsingh/gnewsclient/tree/master/gnewsclient) and integrates [newpaper](https://newspaper.readthedocs.io/en/latest/), [jeiba](https://github.com/fxsjy/jieba) and [wordcloud](https://github.com/amueller/word_cloud) to perform "search" and "analysis" of google news. 

Functions:
1. Custermize search of Google News 
2. Keywords extraction  (limited to Chinese. It can be release in the future.)
3. Wordcloud  (limited to Chinese. It can be release in the future.)
![](https://i.imgur.com/Vqs484E.png)
Demontration of searching "氣候變遷" ("Climate change").

## Install
1. Download GNewsAnalysis
1. cd to unzipped GNewsAnalysis folder
1. Use pip to install
```
pip install GNewsAnalysis
# or
pip install .
```

## Demo
可參考套件中 demo.py 檔

```
# import the package
import GNewsAnalysis as G

# Create an object
g = G.SearchNews()

# View the initial configuration for Google news search
g.get_config()

# View options 
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
```
