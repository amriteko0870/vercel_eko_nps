import re  
from datetime import datetime
from nps.models import *
from user_auth.models import *
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as sia
from textblob import TextBlob


# email validation
def validate_email(email):  
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):  
        return True  
    return False  

# email already exist check
def new_email_check(email):
    try:    
        user_data.objects.get(email = email)
        return False
    except:
        return True
    
# Organization already exist check   
def new_organisation_check(org_name):
    try:
        user_data.objects.get(org_name = org_name)
        return False
    except:
        return True
    
# token varification
def check_token(token):
    try:
        user = user_data.objects.get(token = token)
        res = { 'status':True,
                'user_info':{   
                                'user_id':user.id,
                                'username':user.username,
                                'org_name':user.org_name,
                                'email':user.email
                            }
              }
        return res
    except:
        res = {
                'status':False
              }
        return res
    
def date_validator(date):
    try:
        datetime.strptime(str(date)[:10], "%Y-%m-%d")
        return 1
    except:
        return 0
    

def test_func(x,y):

    for i in range(1000):
        print(f"{x} {y} {i}")
    return i

# def sentiment_scores(x):
#     sentence = str(x['review'])
#     nps = x['nps']
#     sid_obj = sia()
#     sentiment_dict = sid_obj.polarity_scores(sentence)
#     pos = sentiment_dict['pos']*100
#     neg = sentiment_dict['neg']*100
#     neu = sentiment_dict['neu']*100

#     if pos > neg:
#         max = pos
#         sentiment = 'Positive'
#     else:
#         max = neg
#         sentiment = 'Negative'
#     if max < neu:
#         max = neu
#         sentiment = 'Neutral'         

#     if sentiment == 'Negative' and eval(str(nps)) <3:
#         sentiment = 'Extreme'
#     if sentence == '':
#         sentiment = 'Neutral'
#     return sentiment

def sentiment_scores(df):
    sentence = str(df['review'])
    nps = df['nps']
    sentiment = TextBlob(sentence)
    polarity = sentiment.polarity
    if polarity >= 0.05 :
        sentiment = 'Positive'
    elif polarity <= - 0.05 :
        sentiment = 'Negative'
    else :
        sentiment = 'Neutral'
    if sentiment == 'Negative' and nps >4:
        sentiment = 'Neutral'
    if sentiment == 'Negative' and nps < 3 :
        sentiment = 'Extreme'
    if sentiment == 'Negative' and nps >8:
        sentiment = 'Positive'
    return sentiment

def file_upload_process(user_id,df,file,file_size):
    df.fillna('',inplace=True)
    print('##############################')
    print("Sentiment process started")
    f = file_uploading_status(
                            user_id = user_id,
                            status = "Processing sentiment for reviews"
                         )
    f.save()
    print(f.id)
    print('##############################')
    df['sentiment'] = df.apply(sentiment_scores,axis=1)
    print('##############################')
    print("Values getting stored in database")
    file_uploading_status.objects.filter(user_id = user_id).update(status = "Values getting stored in databse")
    print('##############################')   
    for i in range(df.shape[0]):
        print(i)
        review = df['review'][i]
        nps = df['nps'][i]
        date = datetime.strptime(str(df['date'][i])[:10], "%Y-%m-%d")
        sentiment = df['sentiment'][i]
        n = nps_data(
                    user_id = user_id,
                    review = review,
                    nps = nps,
                    date = date,
                    sentiment = sentiment,
                    uploading_status = True
                )
        n.save()
    print('##############################')
    print("Completed")
    file_uploading_status.objects.filter(user_id = user_id).delete()
    print('##############################')   
    log_obj = upload_log(
                            user_id = user_id,
                            file_name = file,
                            file_size = f'{file_size} kb' if file_size < 1000 else f'{round(file_size/1000,2)} mb'
                        )
    log_obj.save()

def nps_type(x):
    if x < 7:
        return 'Detractor'
    elif x > 6 and x < 9:
        return 'Passive'
    elif x > 8:
        return 'Promoter'