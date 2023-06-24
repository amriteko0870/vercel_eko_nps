from django.shortcuts import render
from import_statements import *

# Create your views here.

@api_view(['GET'])
def index(request):
    user_data.objects.all().delete()
    # google_reviews.objects.filter(review = 'nan').update(review = "")
    return Response('done')

@api_view(['POST'])
def create_user(request):
    data = request.data
    try:
        username = data['username']
    except:
        res = {
                'status':False,
                'status_code':400,
                'title':'Bad Request',
                'message':'username is required'
              }
        return Response(res)
    try:
        email = data['email']
    except:
        res = {
                'status':False,
                'status_code':400,
                'title':'Bad Request',
                'message':'email is required'
              }
        return Response(res)

    try:
        org_name = data['org_name']
    except:
        res = {
                'status':False,
                'status_code':400,
                'title':'Bad Request',
                'message':'org_name is required'
              }
        return Response(res)
        
    try:
        password = data['password']
    except:
        res = {
                'status':False,
                'status_code':400,
                'title':'Bad Request',
                'message':'password is required'
              }
        return Response(res)
        
    # email validations
    if not validate_email(email):
        res = {
                'status':False,
                'status_code': 400,
                'title': 'Bad Request',
                'message': 'Email validation failed'
              }
        return Response(res)
    
    # email already exist check
    if not new_email_check(email):
        res = {
                'status':False,
                'status_code': 409,
                'title': 'Conflict',
                'message': 'Email already exist'
              }
        return Response(res)
    
    # organization alreay exist check
    if not new_organisation_check(org_name):
        res = {
                'status':False,
                'status_code': 409,
                'title': 'Conflict',
                'message': 'Organization already exist'
              }
        return Response(res)
    
    user_obj = user_data(
                            username = username,
                            email = email,
                            org_name = org_name,
                            password = make_password(password),
                            token = make_password(email+password)
                        )
    user_obj.save()
    res = {
            'status':True,
            'status_code':201,
            'title':'Created',
            'message':'User created successfully'
          }
    return Response(res)


@api_view(['POST'])
def login(request):
    data = request.data
    # email = data['email']
    # password = data['password']
    res = {
            'status':True,
            'status_code':200,
            'title':'OK',
            'message':'User authorized',
            }
    return Response(res)
    
    try:
        user = user_data.objects.get(email = email)
        if check_password(password,user.password):
            res = {
                    'status':True,
                    'status_code':200,
                    'title':'OK',
                    'message':'User authorized',
                    'user_data':{   
                                    'id':user.id,
                                    'username':user.username,
                                    'org_name':user.org_name,
                                    'email':user.email,
                                    'token':user.token
                                }
                  }
            return Response(res)
        else:
            res = {
                    'status':False,
                    'status_code':401,
                    'title':'Unauthorized',
                    'message':'Invalid credentials'
                  }
            return Response(res)
    except:
        res = {
                'status':False,
                'status_code':401,
                'title':'Unauthorized',
                'message':'Invalid credentials'
                }
        return Response(res)