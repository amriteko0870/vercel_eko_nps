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

@api_view(['POST'])
def nps_upload_button_status(request):
    user_id = 3
    """
    Token Validation
    """
    try:
        f = file_uploading_status.objects.get(user_id = user_id)
        res = {
                'status':False,
                'status_code':226,
                'title':'IM Used',
                'message':'Processing',
                'hover_text': f.status
        }
    except:
        res = {
                'status':True,
                'status_code':200,
              }
    return Response(res)
@api_view(['POST'])
def file_upload(request):
    data = request.data
    user_id = 3
    """
    Token Validation
    """
    #file upload check

    try:
        f = file_uploading_status.objects.get(user_id = user_id)
        res = {
                'status':False,
                'status_code':226,
                'title':'IM Used',
                'message':f"Previous file already being processed. Status - {f.status}"
              }
        return Response(res)
    except:
        pass
    try:
        file = request.FILES['file']
    except:
        res = {
                'status':False,
                'status_code':400,
                'title':'Bad Request',
                'message':'file is required'
              } 
        return Response(res)

    # file size validation
    file_size = round(file.size/1024,2)
    if file_size > 19999:
        res = {
                'status':False,
                'status_code':413,
                'title':'Content Too Large',
                'message':'File size exceeds 20MB'
              }
        return Response(res)
    
    # file extension validation
    ext = file.name.split('.')[-1]
    if ext == 'csv':
        df = pd.read_csv(file)
    elif ext == 'xlsx':
        df = pd.read_excel(file)
    else:
        res = {
                'status':False,
                'status_code':422,
                'title':'Unprocessable Content',
                'message':f'file extension should be .csv or .xlsx but your file was .{ext}'
              }
        return Response(res)
    # Column name validation
    df.columns = df.columns.str.lower()
    file_columns = list(df.columns)
    if 'review' not in file_columns:
        res = {
                'status':False,
                'status_code':417,
                'title':'Expectation Failed',
                'message':'review column is not present in file as expected'
              }
        return Response(res)
    
    if 'nps' not in file_columns:
        res = {
                'status':False,
                'status_code':417,
                'title':'Expectation Failed',
                'message':'nps column is not present in file as expected'
              }
        return Response(res)
    
    if 'date' not in file_columns:
        res = {
                'status':False,
                'status_code':417,
                'title':'Expectation Failed',
                'message':'date column is not present in file as expected'
              }
        return Response(res)
    
    # date column validation
    df['date_validator'] = df['date'].apply(date_validator)
    wrong_date = df.loc[df['date_validator'] == 0]
    print(str(df['date'][0]))
    if len(wrong_date) > 0:
        res = {
                'status':False,
                'status_code':406,
                'title':'Not Acceptable',
                'message':'Expected dateformat for date column is YYYY-mm-dd but got different in some cases'
              }
        return Response(res)
    Thread(target=file_upload_process, args=(user_id,df,file.name,file_size,)).start()
    res = {'status':True,
           'message':'File uploaded successfully'}
    return Response(res)




@api_view(['POST'])
def net_promoter_score(request):
    data = request.data
    """
    Token Validation
    """

    user_id = 3
    nd_obj = nps_data.objects.filter(user_id = user_id).values().order_by('-date')
    total = nd_obj.count()
    net_promoter = nd_obj.filter(nps__gt=8).count()
    net_passive = nd_obj.filter(nps__gt = 6, nps__lt = 9).count()
    net_detractor = nd_obj.filter(nps__lt = 7).count()
    try:
       net_promoter_percentage  = round(net_promoter*100/total,2)
    except:
       net_promoter_percentage = 0
    try:
       net_passive_percentage  = round(net_passive*100/total,2)
    except:
       net_passive_percentage = 0
    try:
       net_detractor_percentage  = round(net_detractor*100/total,2)
    except:
       net_detractor_percentage = 0
    # return Response([net_promoter_percentage,net_passive_percentage,net_detractor_percentage])

    nps = net_promoter_percentage - net_detractor_percentage
    nps = round(nps,2) if nps > 0 else 0

    nps_res = {
                        "nps": {
                            "nps_score": nps,
                            "promoters": net_promoter_percentage,
                            "total_promoters": net_promoter,
                            "passive": net_passive_percentage,
                            "total_passive": net_passive,
                            "detractors": net_detractor_percentage,
                            "total_detractors": net_detractor
                        },
                        "nps_pie": [
                                        {
                                            "label": "Promoters",
                                            "percentage": net_promoter_percentage,
                                            "color": "#00AC69"
                                        },
                                        {
                                            "label": "Passives",
                                            "percentage": net_passive_percentage,
                                            "color": "#939799"
                                        },
                                        {
                                            "label": "Detractors",
                                            "percentage": net_detractor_percentage,
                                            "color": "#DB2B39"
                                        }
                        ]
                    }
    res = {
            'status':True,
            'status_code':200,
            'title':'OK',
            'message':'NPS card data',
            'data':nps_res
            }
    return Response(res)

@api_view(['POST'])
def netSentimentCard(request):
    data = request.data
    """
     token verification
    """
    user_id = 3
    nd_obj = nps_data.objects.filter(user_id = user_id).values().order_by('-date')
    total = nd_obj.count()
    sentiment_positive = nd_obj.filter(sentiment='Positive').count()
    sentiment_neutral = nd_obj.filter(sentiment='Neutral').count()
    sentiment_negative = nd_obj.filter(sentiment='Negative').count()
    sentiment_extreme = nd_obj.filter(sentiment='Extreme').count()

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
    nd_obj = nps_data.objects.filter(user_id = user_id).values().order_by('-date')
    surveyed = nd_obj.count()
    comments = nd_obj.exclude(review = '').count()
    alerts = nd_obj.filter(sentiment = 'Extreme').count()

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
    nd_obj = nps_data.objects.filter(user_id = user_id).exclude(review = "").values('id','review','nps','date','sentiment').order_by('-date')
    if len(nd_obj)>0:
        nd_obj = pd.DataFrame(nd_obj)
        nd_obj['date'] = nd_obj['date'].apply(lambda x : datetime.strptime(str(x)[:10],'%Y-%m-%d').strftime('%b %Y'))
        nd_obj['nps_type'] = nd_obj['nps'].apply(nps_type)
        nd_obj = nd_obj.to_dict(orient='records')
    else:
        nd_obj = []    
    return Response(nd_obj)

@api_view(['POST'])
def all_alerts(request):
    data = request.data
    """
     token verification
    """
    user_id = 3
    nd_obj = nps_data.objects.filter(user_id = user_id,sentiment='Extreme').exclude(review = "").values('id','review','nps','date','sentiment').order_by('-date')
    if len(nd_obj)>0:
        nd_obj = pd.DataFrame(nd_obj)
        nd_obj['date'] = nd_obj['date'].apply(lambda x : datetime.strptime(str(x)[:10],'%Y-%m-%d').strftime('%b %Y'))
        nd_obj['nps_type'] = nd_obj['nps'].apply(nps_type)
        nd_obj = nd_obj.to_dict(orient='records')
    else:
        nd_obj = []
    return Response(nd_obj)


@api_view(['POST'])
def nss_over_time(request):
    data = request.data
    """
     token verification
    """
    user_id = 3
    nd_obj = nps_data.objects.order_by('-date').values('date__year', 'date__month')\
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
    nd_obj = pd.DataFrame(nd_obj)
    nd_obj['SURVEY_MONTH'] = nd_obj['survey_date'].apply(lambda x : datetime.strptime(str(x)[:10],'%Y-%m-%d').strftime('%b-%Y'))
    nd_obj['month'] = nd_obj['survey_date'].apply(lambda x : datetime.strptime(str(x)[:10],'%Y-%m-%d').strftime('%b-%y'))
    nd_obj = nd_obj.to_dict(orient='records')
    res = {
            'status':True,
            'status_code':200,
            'title':'OK',
            'message':'Data for net cards',
            'data':{
                    'nss_over_time':nd_obj
                    }
          }                                                
    return Response(res)


@api_view(['POST'])
def nps_over_time(request):
    data = request.data
    data = request.data
    """
     token verification
    """
    user_id = 3
    nd_obj = nps_data.objects.order_by('-date').values('date__year', 'date__month')\
                                               .annotate(
                                                    count = Count('pk'),
                                                    year = F('date__year'),
                                                    survey_date = F('date'),
                                                    promoter = twoDecimal((Cast(Sum(Case(
                                                                When(nps__range=[9,10],then=1),
                                                                default=0,
                                                                output_field=IntegerField()
                                                                )),FloatField()))),\
                                                    passive =  twoDecimal((Cast(Sum(Case(
                                                                When(nps__range=[7,8],then=1),
                                                                default=0,
                                                                output_field=IntegerField()
                                                                )),FloatField()))),\
                                                    detractor = twoDecimal((Cast(Sum(Case(
                                                                When(nps__range=[0,6],then=1),
                                                                default=0,
                                                                output_field=IntegerField()
                                                                )),FloatField()))),\
                                                    nps_abs = twoDecimal(
                                                        ((F('promoter')-F('detractor'))/(F('promoter')+F('passive')+F('detractor')))*10),
                                                    nps = Case(
                                                            When(
                                                                nps_abs__lt = 0,
                                                                then = 0    
                                                                ),
                                                                default=F('nps_abs'),
                                                                output_field=FloatField()
                                                              )
                                                )
    nd_obj = pd.DataFrame(nd_obj)
    nd_obj['SURVEY_MONTH'] = nd_obj['survey_date'].apply(lambda x : datetime.strptime(str(x)[:10],'%Y-%m-%d').strftime('%b-%Y'))
    nd_obj['month'] = nd_obj['survey_date'].apply(lambda x : datetime.strptime(str(x)[:10],'%Y-%m-%d').strftime('%b-%y'))
    nd_obj = nd_obj.to_dict(orient='records')
    res = {
            'status':True,
            'status_code':200,
            'title':'OK',
            'message':'Data for nps overtime',
            'data':{
                    'nps_over_time':nd_obj
                    }
          }                                                
    return Response(res)


@api_view(['POST'])
def nps_vs_sentiment(request):
    data = request.data
    """
     token verification
    """
    user_id = 3
    nd_obj = nps_data.objects.filter(user_id = user_id).values()
    positive = nd_obj.values('sentiment').filter(sentiment = 'Positive')\
                                .annotate(
                                            promoter = twoDecimal((Cast(Sum(Case(
                                                        When(nps__range=[9,10],then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('pk'),FloatField()))*100),
                                            passive =  twoDecimal((Cast(Sum(Case(
                                                        When(nps__range=[7,8],then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('pk'),FloatField()))*100),
                                            detractor = twoDecimal((Cast(Sum(Case(
                                                        When(nps__range=[0,6],then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('pk'),FloatField()))*100)
                                        ).order_by('sentiment')
    
    negative = nd_obj.values('sentiment').filter(sentiment = 'Negative')\
                                .annotate(
                                            promoter = twoDecimal((Cast(Sum(Case(
                                                        When(nps__range=[9,10],then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('pk'),FloatField()))*100),
                                            passive =  twoDecimal((Cast(Sum(Case(
                                                        When(nps__range=[7,8],then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('pk'),FloatField()))*100),
                                            detractor = twoDecimal((Cast(Sum(Case(
                                                        When(nps__range=[0,6],then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('pk'),FloatField()))*100)
                                        ).order_by('sentiment')
    
    neutral = nd_obj.values('sentiment').filter(sentiment = 'Neutral')\
                                .annotate(
                                            promoter = twoDecimal((Cast(Sum(Case(
                                                        When(nps__range=[9,10],then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('pk'),FloatField()))*100),
                                            passive =  twoDecimal((Cast(Sum(Case(
                                                        When(nps__range=[7,8],then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('pk'),FloatField()))*100),
                                            detractor = twoDecimal((Cast(Sum(Case(
                                                        When(nps__range=[0,6],then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('pk'),FloatField()))*100)
                                        ).order_by('sentiment')
    
    extreme = nd_obj.values('sentiment').filter(sentiment = 'Extreme')\
                                .annotate(
                                            promoter = twoDecimal((Cast(Sum(Case(
                                                        When(nps__range=[9,10],then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('pk'),FloatField()))*100),
                                            passive =  twoDecimal((Cast(Sum(Case(
                                                        When(nps__range=[7,8],then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('pk'),FloatField()))*100),
                                            detractor = twoDecimal((Cast(Sum(Case(
                                                        When(nps__range=[0,6],then=1),
                                                        default=0,
                                                        output_field=IntegerField()
                                                        )),FloatField())/Cast(Count('pk'),FloatField()))*100)
                                        ).order_by('sentiment')
    
    if(len(list(positive)) == 0):
        positive = [{
                        "sentiment_label": "Positive",
                        "promoter": 0,
                        "passive": 0,
                        "detractor": 0
                    }]
    if(len(list(negative)) == 0):
        negative = [{
                        "sentiment_label": "negative",
                        "promoter": 0,
                        "passive": 0,
                        "detractor": 0
                    }]
    if(len(list(neutral)) == 0):
        neutral = [{
                        "sentiment_label": "neutral",
                        "promoter": 0,
                        "passive": 0,
                        "detractor": 0
                    }]
    if(len(list(extreme)) == 0):
        extreme = [{
                        "sentiment_label": "Extreme",
                        "promoter": 0,
                        "passive": 0,
                        "detractor": 0
                    }]
    final_data = list(positive)+list(negative)+list(neutral)+list(extreme)
    res = {
            'status':True,
            'status_code':200,
            'title':'OK',
            'message':'Data for nps Vs sentiment',
            'data':{
                    'nps_vs_sentiment':final_data
                    }
          }                                                
    return Response(res)


@api_view(['POST'])
def delete_records(request):
    user_id = 3
    try:
        f = file_uploading_status.objects.get(user_id = user_id)
        res = {
                'status':False,
                'status_code':226,
                'title':'IM Used',
                'message':f"Previous file already being processed. Please wait"
              }
        return Response(res)
    except:
        pass
    nps_data.objects.filter(uploading_status = True).delete()
    res = {
            'status':True,
            'message':'Records deleted sucessfully'
    }
    return Response(res)


@api_view(['POST'])
def upload_file_log(request):
    user_id = 3
    u = upload_log.objects.filter(user_id = user_id).values()
    u = pd.DataFrame(u)
    u['date'] = u['date_time'].apply(lambda x : str(x)[:10])
    u['time'] = u['date_time'].apply(lambda x : str(x)[11:19])
    u = u.to_dict(orient='records')
    return Response(u)


@api_view(['POST'])
def test_api(request):
    u = upload_log.objects.values()
    return Response(u)