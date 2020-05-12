# In[1]:
get_ipython().run_line_magic('matplotlib', 'inline')

# In[2]:
from pathlib import Path

# In[3]:
from textblob import TextBlob

# In[4]:
blob = TextBlob(Path('spotifydata1.csv').read_text())

# In[5]:
from nltk.corpus import stopwords

# In[6]:
stop_words = stopwords.words('english')

# In[7]:
items = blob.word_counts.items()

# In[8]:
items = [item for item in items if item[0] not in stop_words]

# In[9]:
from operator import itemgetter

# In[10]:
sorted_items = sorted(items, key=itemgetter(1), reverse=True)

# In[11]:
top40 = sorted_items[1:41]

# In[12]:
import pandas as pd

# In[13]:
df = pd.DataFrame(top40, columns=['word', 'count'])  

# In[14]:
df

# In[15]:
axes = df.plot.bar(x='word', y='count', legend=False)
import matplotlib.pyplot as plt
plt.gcf().tight_layout()






