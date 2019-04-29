from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import boto3
from boto3.dynamodb.conditions import Key, Attr
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.conf.urls.static import static
import datetime

# Create your views here.

def search(request):
    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('ingredients')

    pe="#na"
    ean = { "#na": "name", }

    scan=dynamoTable.scan(
            ProjectionExpression=pe,
            ExpressionAttributeNames=ean
    )
    a=[]
    for i in scan['Items']:
        a.append(i['name'])

    d = []
    for x in range(len(a)):
        b = {}
        b['id'] = x
        b['value'] = a[x]
        d.append(b)
    return render(request, 'uploadforum/search.html',{'names':d})

def insert1(request):
    if request.method == "POST":
        ingredients = request.POST.getlist('ingredient')
        print("\ningredients:",ingredients)
    return render(request,'uploadforum/complected.html')



#@login_required
def insert(request):
    if request.method == "POST":
        Rname = request.POST['Rname']
        ingredients = request.POST.getlist('ingredient')
        quantity = request.POST.getlist('quantity')
        option = request.POST.getlist('option')
        Steps = request.POST.getlist('Steps')
        Servings = request.POST['Servings']
        Description = request.POST['Description']
        Maketime = request.POST['Maketime']
        myfile = request.FILES['sentFile']

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        f = request.FILES['sentFile']
        f="./media/"+str(myfile)
        s3 = boto3.client('s3')
        bucket = 'dbms2019'

        file_name = str(f)
        key_name = str(myfile)
        ###

        s3.upload_file(file_name, bucket, key_name)

        bucket_location = boto3.client('s3').get_bucket_location(Bucket=bucket)
        link = "https://s3-ap-southeast-1.amazonaws.com/{0}/{1}".format(
             bucket,
             key_name)
        dynamoDB = boto3.resource('dynamodb')
        dynamoTable = dynamoDB.Table('recipe')

        scan = dynamoTable.scan()
        count = len(scan['Items'])

        dynamoTable.put_item(
            Item={
                'R_id':int(count + 1),
                'name': Rname,
                'servings': Servings,
                'ingreditents': ingredients,
                'steps': Steps,
                'Region': 'Indian',
                'Maketime': Maketime,
                'Imglink': link,
                'Chefname': 'Anirudh',
                'Description': Description,
                }
        )

        dynamoTable = dynamoDB.Table('forum')
        scan = dynamoTable.scan()
        count2 = len(scan['Items'])
        now = datetime.datetime.now()


        dynamoTable.put_item(
            Item={

                'P_id': int(count2 + 1),
                'U_id': int(1),
                'R_id': int(count + 1),
                'date': str(str(now.day) + '/' + str(now.month) + '/' + str(now.year)),
                }
        )

    return render(request,'uploadforum/complected.html')


#@login_required
def home(request):
    return render(request,'uploadforum/fo.html')
