from import_statements import *


#----------------------------Annotation Functions--------------------------------------
class roundRating(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 1)'
class twoDecimal(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 2)'
class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 0)'



# Create your views here.

@api_view(['POST'])
def add_url(request):
    data = request.data
    token = data['token']
    url = data['url']
    feature_id = url.split('data=!3m1!4b1!4m8!3m7!1s')[1].split('!8m2!')[0]
    # Token verification
    token_data = check_token(token)
    if token_data['status']:
        user_info = token_data['user_info']
    else:
        res = {
                'status':False,
                'status_code':401,
                'title':'Unauthorized',
                'message':'Authentication Failed'
              } 
        return Response(res)
    
    user_id = user_info['user_id']
    try:
        review_url.objects.get(user_id = user_id)
        review_url.objects.filter(user_id = user_id).update(url = url,feature_id = feature_id)
        res = {
                'status':True,
                'status_code':200,
                'title':'OK',
                'message':'review url updated'
              }
    except:
        url_obj = review_url(
                                user_id = user_id,
                                url = url,
                                feature_id = feature_id
                            )
        url_obj.save()
        res = {
                'status':True,
                'status_code':200,
                'title':'OK',
                'message':'review url added'
              }
    return Response(res)


@api_view(['POST'])
def get_rating(request):
    data = request.data
    """
     token verification
    """
    user_id = 3
    gr_obj = google_reviews.objects.filter(user_id = user_id).values().order_by('-date')
    total = gr_obj.count()
    avg_rating = round(sum(gr_obj.values_list('rating',flat=True))/total,2)
    start_5 = gr_obj.filter(rating=5).count()
    start_4 = gr_obj.filter(rating=4).count()
    start_3 = gr_obj.filter(rating=3).count()
    start_2 = gr_obj.filter(rating=2).count()
    start_1 = gr_obj.filter(rating=1).count()

    try:
        star_5_percentage = round(start_5*100/total,2)
    except:
        star_5_percentage = 0
    try:
        star_4_percentage = round(start_4*100/total,2)
    except:
        star_4_percentage = 0
    try:
        star_3_percentage = round(start_3*100/total,2)
    except:
        star_3_percentage = 0
    try:
        star_2_percentage = round(start_2*100/total,2)
    except:
        star_2_percentage = 0
    try:
        star_1_percentage = round(start_1*100/total,2)
    except:
        star_1_percentage = 0

    res = {
            'status':True,
            'status_code':200,
            'title':'OK',
            'message':'Data for net rating card',
            'data':{
                        'total':total,
                        'rating':avg_rating,
                        'star':round(avg_rating),
                        '5':start_5,
                        '4':start_4,
                        '3':start_3,
                        '2':start_2,
                        '1':start_1,
                        '_5':f"{star_5_percentage}%",
                        '_4':f"{star_4_percentage}%",
                        '_3':f"{star_3_percentage}%",
                        '_2':f"{star_2_percentage}%",
                        '_1':f"{star_1_percentage}%",
                    }
          }

    return Response(res)

@api_view(['POST'])
def netSentimentCard(request):
    data = request.data
    """
     token verification
    """
    user_id = 3
    gr_obj = google_reviews.objects.filter(user_id = user_id).values().order_by('-date')
    total = gr_obj.count()
    sentiment_positive = gr_obj.filter(sentiment='Positive').count()
    sentiment_neutral = gr_obj.filter(sentiment='Neutral').count()
    sentiment_negative = gr_obj.filter(sentiment='Negative').count()
    sentiment_extreme = gr_obj.filter(sentiment='Extreme').count()

    try:
        sentiment_positive_percentage  = round(sentiment_positive*100/total,2)
    except:
        sentiment_positive_percentage = 0
    try:
        sentiment_neutral_percentage  = round(sentiment_neutral*100/total,2)
    except:
        sentiment_neutral_percentage = 0
    try:
        sentiment_negative_percentage  = round(sentiment_negative*100/total,2)
    except:
        sentiment_negative_percentage = 0
    try:
        sentiment_extreme_percentage  = round(sentiment_extreme*100/total,2)
    except:
        sentiment_extreme_percentage = 0
    nss = sentiment_positive_percentage - sentiment_negative_percentage - sentiment_extreme_percentage
    nss = round(nss,2) if nss > 0 else 0

    res = {
            "status":True,
            "status_code":200,
            "title":"OK",
            "message":"Data for net sentiment card",
            "data":{
                    "nss": {
                                "nss_score": nss,
                                "total": total,
                                "positive": sentiment_positive_percentage,
                                "total_positive": sentiment_positive,
                                "negative": sentiment_negative_percentage,
                                "total_negative": sentiment_negative,
                                "extreme": sentiment_extreme_percentage,
                                "total_extreme": sentiment_extreme,
                                "neutral": sentiment_neutral_percentage,
                                "total_neutral": sentiment_neutral
                        },
                    "nss_pie": [
                                    {
                                        "label": "Positive",
                                        "percentage": sentiment_positive_percentage,
                                        "color": "#00AC69"
                                    },
                                    {
                                        "label": "Negative",
                                        "percentage": sentiment_negative_percentage,
                                        "color": "#EE6123"
                                    },
                                    {
                                        "label": "Extreme",
                                        "percentage": sentiment_extreme_percentage,
                                        "color": "#DB2B39"
                                    },
                                    {
                                        "label": "Neutral",
                                        "percentage": sentiment_neutral_percentage,
                                        "color": "#939799"
                                    }
                                ]
                        }
          } 
    return Response(res)

@api_view(['POST'])
def net_cards(request):
    data = request.data
    """
     token verification
    """
    user_id = 3
    gr_obj = google_reviews.objects.filter(user_id = user_id).values().order_by('-date')
    surveyed = gr_obj.count()
    comments = gr_obj.exclude(review = '').count()
    alerts = gr_obj.filter(sentiment = 'Extreme').count()

    res = {
            'status':True,
            'status_code':200,
            'title':'OK',
            'message':'Data for net cards',
            'data':[
                    {
                        'title':"Surveyed",
                        'value':surveyed
                    },
                    {
                        'title':"Comments",
                        'value':comments
                    },
                    {
                        'title':"Alerts",
                        'value':alerts
                    },
                    ]
          }
    return Response(res)


@api_view(['POST'])
def all_comments(request):
    data = request.data
    """
     token verification
    """
    user_id = 3
    gr_obj = google_reviews.objects.filter(user_id = user_id).exclude(review = "").values('id','name','review','rating','date','sentiment').order_by('-date')
    if len(gr_obj)>0:
        gr_obj = pd.DataFrame(gr_obj)
        gr_obj['date'] = gr_obj['date'].apply(lambda x : datetime.strptime(str(x)[:10],'%Y-%m-%d').strftime('%b %Y'))
        gr_obj = gr_obj.to_dict(orient='records')
    else:
        gr_obj = []
    return Response(gr_obj)

@api_view(['POST'])
def all_alerts(request):
    data = request.data
    """
     token verification
    """
    user_id = 3
    gr_obj = google_reviews.objects.filter(user_id = user_id,sentiment='Extreme').exclude(review = "").values('id','name','review','rating','date','sentiment').order_by('-date')
    if len(gr_obj)>0:
        gr_obj = pd.DataFrame(gr_obj)
        gr_obj['date'] = gr_obj['date'].apply(lambda x : datetime.strptime(str(x)[:10],'%Y-%m-%d').strftime('%b %Y'))
        gr_obj = gr_obj.to_dict(orient='records')
    else:
        gr_obj = []
    return Response(gr_obj)

@api_view(['POST'])
def nss_over_time(request):
    data = request.data
    """
     token verification
    """
    user_id = 3
    gr_obj = google_reviews.objects.filter(user_id = user_id).order_by('-date').values('date__year', 'date__month')\
                                                     .annotate(
                                                                count=Count('pk'),
                                                                year = F('date__year'),
                                                                survey_date = F('date'),
                                                                positive = twoDecimal((Cast(Sum(Case(
                                                                            When(sentiment='Positive',then=1),
                                                                            default=0,
                                                                            output_field=IntegerField()
                                                                            )),FloatField()))),#/Cast(Count('id'),FloatField()))*100),\
                                                                negative = twoDecimal((Cast(Sum(Case(
                                                                            When(sentiment='Negative',then=1),
                                                                            default=0,
                                                                            output_field=IntegerField()
                                                                            )),FloatField()))),
                                                                neutral = twoDecimal((Cast(Sum(Case(
                                                                            When(sentiment='Neutral',then=1),
                                                                            default=0,
                                                                            output_field=IntegerField()
                                                                            )),FloatField()))),
                                                                extreme = twoDecimal((Cast(Sum(Case(
                                                                            When(sentiment='Extreme',then=1),
                                                                            default=0,
                                                                            output_field=IntegerField()
                                                                            )),FloatField()))),
                                                                nss_abs = twoDecimal((F('positive')-F('negative')-F('extreme'))/Cast(Count('id'),FloatField())*100),
                                                                nss = Case(
                                                                            When(
                                                                                nss_abs__lt = 0,
                                                                                then = 0    
                                                                                ),
                                                                                default=F('nss_abs'),
                                                                                output_field=FloatField()
                                                                            )
                                                                  )
    gr_obj = pd.DataFrame(gr_obj)
    gr_obj['SURVEY_MONTH'] = gr_obj['survey_date'].apply(lambda x : datetime.strptime(str(x)[:10],'%Y-%m-%d').strftime('%b-%Y'))
    gr_obj['month'] = gr_obj['survey_date'].apply(lambda x : datetime.strptime(str(x)[:10],'%Y-%m-%d').strftime('%b-%y'))
    gr_obj = gr_obj.to_dict(orient='records')
    res = {
            'status':True,
            'status_code':200,
            'title':'OK',
            'message':'Data for nss overtime',
            'data':{
                    'nss_over_time':gr_obj
                    }
          }                                                
    return Response(res)


@api_view(['POST'])
def rating_over_time(request):
    data = request.data
    """
     token verification
    """
    user_id = 3
    gr_obj = google_reviews.objects.filter(user_id = user_id).order_by('-date').values('date__year', 'date__month')\
                                                     .annotate(
                                                                count=Count('pk'),
                                                                year = F('date__year'),
                                                                survey_date = F('date'),
                                                                avg_rating = twoDecimal(Avg('rating')),
                                                                
                                                                  )
    gr_obj = pd.DataFrame(gr_obj)
    gr_obj['SURVEY_MONTH'] = gr_obj['survey_date'].apply(lambda x : datetime.strptime(str(x)[:10],'%Y-%m-%d').strftime('%b-%Y'))
    gr_obj['month'] = gr_obj['survey_date'].apply(lambda x : datetime.strptime(str(x)[:10],'%Y-%m-%d').strftime('%b-%y'))
    gr_obj = gr_obj.to_dict(orient='records')
    res = {
            'status':True,
            'status_code':200,
            'title':'OK',
            'message':'Data for rating overtime',
            'data':{
                    'rating_over_time':gr_obj
                    }
          }      
    return Response(res)      


@api_view(['POST'])
def rating_sentiment_over_time(request):
    data = request.data
    """
     token verification
    """
    user_id = 3
    gr_obj = google_reviews.objects.filter(user_id = user_id).order_by('-date').values('date__year', 'date__month')\
                                                     .annotate(
                                                                count=Count('pk'),
                                                                year = F('date__year'),
                                                                survey_date = F('date'),
                                                                avg_rating = twoDecimal(Avg('rating')),
                                                                positive = twoDecimal((Cast(Sum(Case(
                                                                            When(sentiment='Positive',then=1),
                                                                            default=0,
                                                                            output_field=IntegerField()
                                                                            )),FloatField()))),#/Cast(Count('id'),FloatField()))*100),\
                                                                negative = twoDecimal((Cast(Sum(Case(
                                                                            When(sentiment='Negative',then=1),
                                                                            default=0,
                                                                            output_field=IntegerField()
                                                                            )),FloatField()))),
                                                                neutral = twoDecimal((Cast(Sum(Case(
                                                                            When(sentiment='Neutral',then=1),
                                                                            default=0,
                                                                            output_field=IntegerField()
                                                                            )),FloatField()))),
                                                                extreme = twoDecimal((Cast(Sum(Case(
                                                                            When(sentiment='Extreme',then=1),
                                                                            default=0,
                                                                            output_field=IntegerField()
                                                                            )),FloatField()))),
                                                                nss_abs = twoDecimal((F('positive')-F('negative')-F('extreme'))/Cast(Count('id'),FloatField())*100),
                                                                nss = Case(
                                                                            When(
                                                                                nss_abs__lt = 0,
                                                                                then = 0    
                                                                                ),
                                                                                default=F('nss_abs'),
                                                                                output_field=FloatField()
                                                                            )                                                                
                                                                  )
    gr_obj = pd.DataFrame(gr_obj)
    gr_obj['SURVEY_MONTH'] = gr_obj['survey_date'].apply(lambda x : datetime.strptime(str(x)[:10],'%Y-%m-%d').strftime('%b-%Y'))
    gr_obj['month'] = gr_obj['survey_date'].apply(lambda x : datetime.strptime(str(x)[:10],'%Y-%m-%d').strftime('%b-%y'))
    gr_obj = gr_obj.to_dict(orient='records')
    res = {
            'status':True,
            'status_code':200,
            'title':'OK',
            'message':'Data for rating overtime',
            'data':{
                    'rating_over_time':gr_obj
                    }
          }      
    return Response(res)























@api_view(['POST'])
def store_data(request):
    google_reviews.objects.all().delete()
    data = request.data
    user_id = 3
    df = pd.read_csv('Jayadeva_Hospital.csv')
    # return Response(df.shape[0])
    for i in range(df.shape[0]):
        name = df['name'][i]
        review = df['review'][i]
        rating = df['rating'][i]
        date = datetime.strptime(df['date'][i], "%Y-%m-%d")
        sentiment = df['sentiment'][i]

        gr_obj = google_reviews(
                                    user_id = user_id,
                                    name = name,
                                    review = review,
                                    rating = rating,
                                    date = date,
                                    sentiment = sentiment,
                                )
        gr_obj.save()
        print(i)
    return Response('done')
        
