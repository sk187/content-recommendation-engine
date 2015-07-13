import pandas as pd
import os

#############################
## Content-Based Filtering ##
#############################

# read in songs data
songs = pd.read_csv('songs.csv')
del songs ['Unnamed: 0']
songs.to_csv('/Users/sunggyunkim/Documents/DAT6/data/clean_songs.csv')

clean_songs = pd.read_csv('/Users/sunggyunkim/Documents/DAT6/data/clean_songs.csv')

# Content Based Preferences
del songs['song_title']
del songs['artist']

# Create a dictionary of all content in songs liked
likes = songs[songs.like == 1].sum()
# gets rid of the likes column
likes = likes[0:len(likes)-1]

i = 0
like_dic = {}
for song in likes:
    like_dic[likes.index[i]]= song/len(likes)
    i+= 1

# Create a dictionary of all content in songs disliked
dislikes = songs[songs.like == -1].sum()
# gets rid of the likes column
dislikes = dislikes[0:len(dislikes)-1]
i = 0
dislike_dic = {}
for song in dislikes:
    dislike_dic[dislikes.index[i]]= song/len(dislikes)*-1
    i+= 1

# Create Preference Dictionary from like and dislike values
pref_dic = {}
for key, value in like_dic.iteritems():
    # print "Like: %s" % like_dic[key]
    # print "Disike: %s " % dislike_dic[key]
    pref_dic[key] = float(like_dic[key]+dislike_dic[key])

#Code 1 for songs not rated, 0 for rated songs
recommendation_list = []
for song in songs.like:
    if song == 0:
        recommendation_list.append(1)
    else:
        recommendation_list.append(0)
clean_songs['recommendable'] = recommendation_list
songs['recommendable'] = recommendation_list

#Create Recommendation Score
features = songs
del features['like']
del features['recommendable']

i = 0
rec_score = []
while i < len(features):
    row = features.iloc[i]
    rec_val = 0
    j = 0
    for feat_val in row:
        pref_val = pref_dic[row.index[j]] #Pref Feature Value
        dot_score = pref_val * feat_val
        rec_val += dot_score
        j+= 1
    rec_score.append(rec_val)
    i += 1
clean_songs['rec_score'] = rec_score

a = clean_songs[clean_songs.recommendable ==1]
rec_list_score_sort = a.sort(['rec_score'], ascending=[0])


rec_list = rec_list_score_sort[['song_title','artist','rec_score']]