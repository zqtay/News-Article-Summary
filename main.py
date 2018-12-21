from urllib.request import urlopen
import re

def extracttitle(page):
  titletag=re.compile('<title.*?>(.*?)</title>')
  titletagged=titletag.search(urlopen(page).read().decode('utf-8'))
  title = titletagged.group(1)
  return title

def extractbody(page):  
  body=''
  ptag=re.compile('<p.*?>(.*?)</p>\s*')
  tagtoremove=re.compile('<.*?>')
  kwtoremove = ['img','src','alt','subscribe','login', 'log in','log-in','copyright','whatispremium','Reporting was contributed by']
  kwtoremove=kwtoremove+[i.capitalize() for i in kwtoremove]
  wordtoremove=['\xa0','Related Coverage   Advertisement']
  ptagged=ptag.findall(urlopen(page).read().decode('utf-8'))
  
  #remove irrelevant p-tagged items
  for i in ptagged:
    if not any(x in i for x in kwtoremove):
      body = body+i+' '
  
  #remove <> and irrelevant words
  body=tagtoremove.sub('',body)
  for x in wordtoremove:
    body=body.replace(x,' ')

  return body

def summarise(body):
  wordcount,scoredict={},{}
  commonword=['he','she','it','i','you','we','they','him','her','me','us','them','his','hers','its','my','your','our','their','mine','yours','ours','theirs','from','to','at','in','into','out','up','down','on','off','be','been','being','is','are','am','was','were','will','would','can','could','has','have','had','do','does','did','done','doing','and','or','so','but','of','by','also','too','for','about','as','with','then','the','a','an','a','where','which','when','what','who','how','whose','whom','this','that','these','those','there','here','.',',','?','!','"','\'',':',' ','']
  commonword=commonword+[i.capitalize() for i in commonword]
  mo=re.compile('\w+')
  endofsentence=re.compile(r'(\w+)(\.)("|\')?(\s)')

  #create a dict of wordcounts for unique words
  for i in mo.findall(body):
    if i not in commonword:
      wordcount[i]=body.count(i)
  
  #tag each sentence with *** and split them into list
  sentences=endofsentence.sub(r'\1\2\3 ***',body.strip()).split('***')

  #calculate word replication score for each sentence and create a scorelist
  for sentence in sentences[1:-1]:
    score=0
    if sentence in commonword:
      pass
    else:
      for word in wordcount.keys():
        if word in sentence:
          score+=wordcount[word]
      score=round(score/len(i),3)
    scoredict[sentence]=score
  
  #arrange the scorelist
  sortedscoredict=sorted(scoredict, key=scoredict.get)
  sortedscoredict.reverse()

  top1,top2=sortedscoredict[0:2] 

  #return the summarised article with starting, ending and top two scoring sentences 
  if sentences.index(top1)<sentences.index(top2):
    return sentences[0]+top1+top2+sentences[-1] 
  else:
    return sentences[0]+top2+top1+sentences[-1] 




webpage=input('Please enter URL of the article to summarise:\n')

print(extracttitle(webpage))
print('\n')
print(summarise(extractbody(webpage)))
