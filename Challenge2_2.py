# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 01:06:02 2017

@author: fxie_
"""

import itertools
import sqlite3
import re
from operator import itemgetter
import time
import pandas as pd

from sqlalchemy import create_engine

# Create your engine.
#engine = create_engine('sqlite:///reddit.db')
#with engine.connect() as conn, conn.begin():
#    table_comments = pd.read_sql_query("SELECT * FROM comments WHERE subreddit_id = '%s'"%subid, engine)

#    subreddit_ids = pd.read_sql_query("SELECT subreddits.id FROM subreddits", engine)
#    for subid in subreddit_ids['id']:
#    	  df = pd.read_sql_query("SELECT author_id FROM comments WHERE subreddit_id = '%s'"%subid, engine)
    
#    i=subreddit_ids[1][0]
def find_most_common(map_key):
    temp=list()
    sample=sub_author_dict[map_key]
    a =max([len(sample.union(sub_author_dict[key])) for key in sub_author_dict if not((key==map_key)or(key =='0'))])
    print(a)
    return {map_key:a}

    
with sqlite3.connect('reddit.db') as conn:
    size_dict = dict()
    for i in range(10):
        size_dict.update({i+1:0})
    start = time.clock()
    #Solve the Error "'gbk' codec can't encode character '\xc2' in position 147: illegal multibyte sequence"
    conn.text_factory = lambda x:str(x,'latin1')
    sub_author_dict = {'0':0}
#    size_dict.update({0:})
#    for i in range(10):
#        size_dict.update({i+1:0})
    turns=0
    #create a Cursor object and call its execute() method to perform SQL commands
    c = conn.cursor()
    c.execute("""SELECT id From subreddits Order by name""")
    id_table_subreddits=[" ".join(row) for row in c.fetchall()]


    for subrebbitid in id_table_subreddits:
        turns=turns+1

#        vectorizer= CountVectorizer()
        print('[{}]{}'.format(turns,subrebbitid))
        
#        subname= (subreddit_name,)
        c.execute("""SELECT comments.author_id
                                      FROM subreddits 
                                      join comments on subreddits.id = comments.subreddit_id
                                      WHERE subreddits.id=?
                                      """, (subrebbitid,))
        authorids= [" ".join(row) for row in c.fetchall()]
        
        sub_author_dict.update({subrebbitid:set(authorids)})
        
        elapsed =  (time.clock()-start)
        print("Time used: ",elapsed)
    start = time.clock()
    for mostcommon in map(find_most_common,id_table_subreddits[0:100]):
        size_dict.update(mostcommon)
        size_sorted = sorted(size_dict.items(),key = itemgetter(1), reverse = True)[:10]
        size_dict = dict(size_sorted)   
         
        
        
    result= sorted(size_dict.items(),key = itemgetter(1), reverse = True)[:10]

           
    #    print('find the first 10')
    with open('challenge2_1.txt', 'wt') as f:
        for key,value in result:
            print("subreddit:'{}'\n total number of distinct words:{}".format(key,size_dict[key]),file=f)
            print('\n')
    elapsed =  (time.clock()-start)
    print("Time used: ",elapsed)