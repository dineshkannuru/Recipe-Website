from django.shortcuts import render,HttpResponse,redirect
import boto3
from boto3.dynamodb.conditions import Key, Attr


# Create your views here.
def explore(request):
    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('recipe')
    fe = Attr('Region').contains('Indian')
    names=[]
    imglinks=[]
    rids=[]
    response = dynamoTable.scan(
        FilterExpression=fe,
        )
    for i in response['Items']:
        names+=[i['name']]
        imglinks+=[i['Imglink']]
        rids+=[i['R_id']]
    return render(request, 'home/explore.html',{'data':zip(names,imglinks,rids)})


def recipe(request, id):
    # FROM here, details of link descrip, steps, so..so..so..

    # TO HERE
    print(id)
    print(type(id))
    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('recipe')
    response = dynamoTable.query(
    KeyConditionExpression=Key('R_id').eq(int(id))
    )
    #data extraction

    print(response['Items'][0]['servings'])
    print(response['Items'][0]['Maketime'])
    print(response['Items'][0]['Chefname'])
    print(response['Items'][0]['ingreditents'])

    servings=response['Items'][0]['servings']
    ingredients=response['Items'][0]['ingreditents']
    chefname=response['Items'][0]['Chefname']
    img=response['Items'][0]['Imglink']
    maketime=response['Items'][0]['Maketime']
    region=response['Items'][0]['Region']
    steps=response['Items'][0]['steps']
    name=response['Items'][0]['name']

    data = {'servings':servings,
            'ingredients':ingredients,
            'chefname':chefname,
            'img':img,
            'maketime':maketime,
            'region':region,
            'steps':steps,
            'name':name}

    return render( request, 'home/recipe.html', data)

def base(request):
    return render(request, 'home/base.html')

def register(request):
    return render(request,'register/login.html')


def registered(request):
    first=request.POST['First']
    last=request.POST['Last']
    email=request.POST['email']
    password=request.POST['password']

    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('Users')
    fe = Attr('email').eq(email)
    response=dynamoTable.scan(FilterExpression=fe)

    if (response['Items']==[]):
        response=dynamoTable.scan()
        if (response['Items']==[]):
            sno=1
        else:
            sno=len(response['Items'])+1
        dynamoTable.put_item(
        Item={
        'uid':str(sno),
        'fname':first,
        'lname':last,
        'email':email,
        'password':password,
        'lat':'80',
        'long':'35',
        }
        )
            # response=dynamoTable.get_item(
            # Key={
            # 'fname':'Yashwanth',
            # 'email':'yashukikkuri@gmail.com'
            # }
            # )

    else:
        # sno=len(response['Items'])+1
        print('email already exists')

    return HttpResponse("hii")

def home(request):
    return render(request, 'home/index.html')

def login(request):
    print("####################")
    flag = 0
    email=request.POST['email']
    password=request.POST['password']
    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('Users')
    fe = Attr('email').eq(email)
    response=dynamoTable.scan(FilterExpression=fe)
    if (response['Items']==[]):
        res = 'You have not registered yet. Please register first to continue'
        flag = 1
        print("register first")
    else:
        print(response['Items'][0]['password'])
        if(response['Items'][0]['password'] == password):
            res = 'Log in now'
            print('You are ready to go in')
        else:
            print("Got you bitch")
            res = 'The password you have entered is wrong'
            flag = 1
    return render(request, 'register/login.html', {'res':res, 'flag':flag})



def search(request):
    return render(request,'search/search.html')
