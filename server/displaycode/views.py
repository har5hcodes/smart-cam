# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
#from rest_framework.decorators import action
from rest_framework.response import Response
#from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from displaycode.serializers import UserSerializer, SnippetSerializer, CommentSerializer, WaitListUserSerializer, CameraSerializer,  SnapshotDetailsSerializer
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden

from displaycode.models import Snippet, Comment, WaitListUser, Camera, SnapshotDetails
from users.models import CustomUser
from .forms import CommentForm
from .forms import SnippetForm
import pdb
import json
from django.http import JsonResponse

import urllib.request
import uuid;
import os
import random
import io
import logging
import sys
import traceback
import shutil

logging.basicConfig(level=logging.INFO)

# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

#import django.contrib.auth.models.AnonymousUser
#import django.contrib.auth.models.User
from django.contrib.auth import get_user
from django.views import generic

class SnippetListView(generic.ListView):
    model = Snippet
    template_name = 'allsnippets_list.html'


@csrf_exempt
def loadSnippet(request, snippetId=None):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if request.user.is_authenticated():
                comment.author = request.user
            else:
                firstUser = CustomUser.objects.all()[:1].get()
                comment.author =  firstUser
                #AnonymousUser
            comment.published_date = timezone.now()
            comment.save()
            #return redirect('post_detail', pk=post.pk)

    readFromDisk = False
    if readFromDisk:
        text = """<h1>welcome to my app !</h1>"""
        myfilename="/Users/raghuramg/wsfun/interviewcodereview/templates/codereview.template.html"
        with open(myfilename, 'r') as myfile:
            codelines = myfile.readlines()
    else:
        #Read code from the database
        if (snippetId is not None):
            currSnippet = Snippet.objects.filter(id=snippetId).get()
        else:
            currSnippet = Snippet.objects.all()[:1].get()
        codelines = currSnippet.text.split('\n')

    commentForm = CommentForm()
    snippetForm = SnippetForm()
    return render(request, 'codereview.template.html', {'snippetId':currSnippet.id,'codelines':codelines,'commentForm':CommentForm,'snippetForm':snippetForm})

@csrf_exempt
def addSnippet(request):
    form = SnippetForm()
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            if request.user.is_authenticated():
                snippet.author = request.user
            else:
                firstUser = CustomUser.objects.all()[:1].get()
                snippet.author =  firstUser
                #AnonymousUser
            #snippet.published_date = timezone.now()
            snippet.save()
            return redirect('loadSnippet', snippetId=snippet.id)

        return redirect('loadSnippet');

class SnippetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Snippet.objects.all()#.order_by('-date_joined')
    serializer_class = SnippetSerializer
    permission_classes = [permissions.AllowAny]
    #permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def comments(self, request, pk=None):
        user = self.get_object()
        commentsQuerySet = Comment.objects.filter(snippetId=pk)
        #data = serializers.serialize('json', list(objectQuerySet), fields=('fileName','id'))

        mylist = list()
        mystr = ""
        for comment in commentsQuerySet:
            serializer = CommentSerializer(comment, context={'request': request})
            #print (serializer.data)
            mylist.append(serializer.data);
        return HttpResponse(json.dumps(mylist), content_type='application/json')


class SearchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Snippet.objects.all()#.order_by('-date_joined')
    serializer_class = SnippetSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get']
    #permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        query = request.GET.get('q')
        if (query is None):
            return HttpResponseBadRequest('Search query is empty', status=405)
        NUMSEARCHRESULTS = 10;
        queryset = Snippet.objects.all().filter(text__contains=query)[0:NUMSEARCHRESULTS]
        serializer = SnippetSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def comments(self, request, pk=None):
        user = self.get_object()
        commentsQuerySet = Comment.objects.filter(snippetId=pk)
        #data = serializers.serialize('json', list(objectQuerySet), fields=('fileName','id'))

        mylist = list()
        mystr = ""
        for comment in commentsQuerySet:
            serializer = CommentSerializer(comment, context={'request': request})
            #print (serializer.data)
            mylist.append(serializer.data);
        return HttpResponse(json.dumps(mylist), content_type='application/json')


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Comment.objects.all()#.order_by('-date_joined')
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return self.User.objects.all()

class WaitListUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = WaitListUser.objects.all()#.order_by('-date_joined')
    serializer_class = WaitListUserSerializer
    permission_classes = [permissions.AllowAny]

#https://joel-hanson.medium.com/drf-how-to-make-a-simple-file-upload-api-using-viewsets-1b1e65ed65ca
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import UploadSerializer

import csv
#import pd #TODO: Replace with csv kit
import json

#Given a CSV file, read it in, aggregate along each column. Return a Json object.
#Json object keys:
#       filters
#       modified_file : Returns the modified file with spaces and double quotes removed.
def generatePivotTable(filename):
    logging.basicConfig(level=logging.INFO)
    output = io.StringIO()
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        csv_writer = csv.writer(output)
        result = dict();
        pivotTable= dict();
        allcolumns =  csv_reader.fieldnames
        numColumns = len(allcolumns)
        newcolumns = []
        for column in allcolumns:
            column = column.strip().replace('"','')
            newcolumns.append(column)
            #logging.debug (column)
            #create a dictionary for each column
            pivotTable[column] = dict(); #new dictionary.

        csv_writer.writerow(newcolumns)
        result['columnHeadings'] = newcolumns

        line_count = 0
        newrows = []
        for row in csv_reader:
            newrow = []
            #remove any and all bad rows. TODO: Inform user about these bad lines and
            #tell them to fix it.
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                #TODO: I think this check is not required.
                line_count += 1
                continue
            isBadRow = False #are there any bad values in the row.
            for column in allcolumns:
                val = row[column]
                if val is None:
                    isBadRow = True
                    break
                column = column.strip().replace('"','')
                #logging.debug (column)
                val = val.strip().replace('"','')
                newrow.append(val)
                if val in pivotTable[column]:
                    pivotTable[column][val] = pivotTable[column][val] + 1;
                else:
                    pivotTable[column][val] = 1
            line_count += 1
            if (not isBadRow):
                csv_writer.writerow(newrow)
                newrows.append(newrow)

        result["modifiedfilecontent"] = output.getvalue()
        result['values'] = newrows
        result["filters"] = pivotTable
        pivotTableJson = json.dumps(pivotTable, indent = 4)
        logging.debug(result)
        logging.info(f'Processed {line_count} lines.')
        return result


# ViewSets define the view behavior.
class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file_uploaded = request.FILES.get('file')
        name = file_uploaded.name
        contentType = file_uploaded.content_type
        outSuffix = "upload_" +str(uuid.uuid4())
        outFilename = "/tmp/" +outSuffix
        destination = open(outFilename, 'wb+')
        for chunk in file_uploaded.chunks():
            destination.write(chunk)
        destination.close()  # File should be closed only after all chuns are added

        #Read it back, assuming its csv file and then generate pivot tables.
        pivotTableJson = generatePivotTable(outFilename);

        #response = "POST API and you have uploaded a {} file of type {} . Wrote out {}".format(name, content_type, outfilename)
        response=pivotTableJson;
        return Response(response)

def download_to_local(self, url):
    name, _ = urlretrieve(url)
    self.signed_file.save("{timestamp}.pdf".format(timestamp=timezone.now().strftime('%Y-%m-%d%/%H-%M-%S')), File(open(name, 'rb')))

#Fetches a CSV or Excel file from a URL and does the same processing as UploadViewSet
class FetchDataViewSet(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        if request.method=="POST":
            key=request.data["key"]
            # handle file not exist case here
        else:
            errResponse = HttpResponseNotFound('<h1>Not a POST request</h1>')
            return errResponse;

        print ("key is")
        print (key)
        #clean URL.
        #For now, I am the only user. I will only give good inputs
        cleanUrl = key;

        outSuffix = "upload_" +str(uuid.uuid4())
        outFilename = "/tmp/" +outSuffix
        destination = outFilename;
        #pdb.set_trace()
        #with urllib.request.urlopen(cleanUrl) as response:
        #    #with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        #    if True:
        #        shutil.copyfileobj(response.content, destination)
        urllib.request.urlretrieve(cleanUrl, destination)

        #TODO: Make sure uploaded file is a csv or excel file.

        #Read it back, assuming its csv file and then generate pivot tables.
        pivotTableJson = generatePivotTable(destination);

        #response = "POST API and you have uploaded a {} file of type {} . Wrote out {}".format(name, content_type, outfilename)
        response=pivotTableJson;
        return Response(response)

# ViewSets define the view behavior.
class RandomPicViewSet(ViewSet):
    #serializer_class = UploadSerializer

    def list(self, request):
        #directory="/home/anooj/fallpics"
        directory="/home/anooj/outputjpgs"
        count = 0;
        filenames = []
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                filenames.append(f)
                count = count + 1
        index = random.randint(1,count)
        print ("index is " + str(index))
        index = index -1;
        filenameToServe = filenames[index]
        print ("file being served is " + filenameToServe)

        try:
            with open(filenameToServe, 'rb') as f:
               file_data = f.read()

            # sending response
            response = HttpResponse(file_data, content_type='img/jpeg')
            response['Content-Disposition'] = 'attachment; filename="foo.jpeg"'
        except IOError:
            # handle file not exist case here
            response = HttpResponseNotFound('<h1>File not exist</h1>')

        return response

    def create(self, request):
        return Response("POST API");

#directory="/home/anooj/fallpics"
directory="/home/anooj/outputjpgs"
#directory="/home/anooj/outputjpgs/new/"
#list of pics with metdata.
class ListPicsViewSet(ViewSet):
    #serializer_class = UploadSerializer

    def list(self, request):
        print ("ListPicsViewSet in list")
        count = 0;
        filenames = []
        result = dict()
        imgdetails = []
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            #if (not "2022_16_00_" in f):
            #    continue

            # checking if it is a file
            if os.path.isfile(f):
                imgdetail = dict();
                filenames.append(f)
                imgdetail["name"]=filename;
                imgdetail["size"] = "30x89"
                #TODO: Url encode this path
                imgUrl = "https://backend.interviewblindspots.com/displaycode/pic/"+filename;
                print ("img url is " + imgUrl)
                imgdetail["url"] = imgUrl;
                DEFAULT_CATEGORY = "RandomPicture"
                category = DEFAULT_CATEGORY

                #try: #try calling degirum APIs. If it fails, no big deal. Just continue without erroring out.
                #    import degirum as dg         # import DeGirum PySDK package

                #    zoo = dg.connect_model_zoo() # connect to DeGirum public model zoo
                #    #print(zoo.list_models())     # print all available models in the model zoo
                #
                #    # load mobilenet_ssd model for CPU;
                #    # model_name should be one returned by zoo.list_models()
                #    model_name = "mobilenet_v2_ssd_coco--300x300_quant_n2x_cpu_1"
                #    model = zoo.load_model(model_name)
                #
                #    # perform AI inference of an image specified by URL
                #    inferenceResult = model(imgUrl)
                #    #print(inferenceResult)                # print numeric results
                #    if (inferenceResult is not None and inferenceResult._inference_results is not None
                #            and len(inferenceResult._inference_results) > 0 and inferenceResult._inference_results[0]["label"] is not None):
                #        category = inferenceResult._inference_results[0]["label"]
                #    #pdb.set_trace()
                #except Exception:
                #    print(traceback.format_exc())
                #    #continue as if nothing happened

                imgdetail["keywords"] = "trees, cars, human"
                imgdetail["categories"] = category
                imgdetail["location"] = "santa monica"
                imgdetail["viewcount"] = "100M views"
                imgdetails.append(imgdetail)
                count = count + 1
                if (count > 20):
                    break

        result["pics"] = imgdetails
        return Response(result)
        index = random.randint(1,count)
        print ("index is " + str(index))
        index = index -1;
        filenameToServe = filenames[index]
        print ("file being served is " + filenameToServe)

        try:
            with open(filenameToServe, 'rb') as f:
               file_data = f.read()

            # sending response
            response = HttpResponse(file_data, content_type='img/jpeg')
            response['Content-Disposition'] = 'attachment; filename="foo.jpeg"'
        except IOError:
            # handle file not exist case here
            response = HttpResponseNotFound('<h1>File not exist</h1>')

        return response

    def retrieve(self, request, pk=None):
        print ("in retrieve")
        print ("pk is " + pk)

    def create(self, request):
        return Response("POST API");

#adpoted from SnippetViewSet
class PicDetailViewSet(viewsets.ViewSet):
    lookup_value_regex = '[0-9_a-zA-Z.]+'
    """
    API endpoint that allows users to be viewed or edited.
    """
    def retrieve(self, request, pk=None):
        print ("hi there");
        print ("pk is " + str(pk))
        count = 0;
        filenames = []
        for filename in os.listdir(directory):
            if (pk == filename):
                print ("found file asked for")
                filenameToServe  = os.path.join(directory, filename)
                # checking if it is a file
                if not os.path.isfile(filenameToServe):
                    #return not found error
                    break;
                print ("file being served is " + filenameToServe)

                try:
                    with open(filenameToServe, 'rb') as fp:
                        file_data = fp.read()
                        #send to degirum server?

                        # sending response
                        response = HttpResponse(file_data, content_type='image/jpeg')
                        #response['Content-Disposition'] = 'attachment; filename="foo.jpeg"'
                    pass
                except IOError:
                    # handle file not exist case here
                    response = HttpResponseNotFound('<h1>File not exist</h1>')
                return response

        response = HttpResponseForbidden('<h1>Some internal error. Dont bother pinging again</h1>')
        return response



#AllowAny
#IsAuthenticated
#IsAdminUser
#IsAuthenticatedOrReadOnly

class CameraViewSet(viewsets.ModelViewSet): 
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer


class SnapshotDetailsViewSet(viewsets.ModelViewSet): 
    queryset = SnapshotDetails.objects.all()
    serializer_class = SnapshotDetailsSerializer
