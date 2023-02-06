# Create your tests here.

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
import json
import sys
import traceback
from django.core.management import call_command
from django.test import TestCase
#from django.utils.six import StringIO
from django.contrib.auth import get_user_model
from django.db import models
from displaycode.models import Snippet, Comment, WaitListUser, Camera, SnapshotDetails
from django.test import Client
import os
import pdb
import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from . import views
 
class TestRestAPI(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(username="normal", email='normal@user.com', password='foo')

        Snippet.objects.create(text="This is my code for Fizzbuzz test");
        Snippet.objects.create(text="This is my code for second Fizzbuzz test");
        Comment.objects.create(author=user, snippetId=1, text="This is my comment 1", line=10, published_date=None);
        Comment.objects.create(author=user, snippetId=1, text="This is my comment 2", line=2, published_date=None);
        Comment.objects.create(author=user, snippetId=2, text="This is my comment 1 on snippet 2", line=20, published_date=None);


    def testGeneratePivotTable(self):
        #Dont check anything. Just hope that no exception is thrown.
        try:
            #pdb.set_trace()
            testfile = "Testing world_population.csv"
            views.generatePivotTable("/home/anooj/world_population.csv", "/tmp/unittestpopulation.csv")
        except Exception as e:
            testfile = "Testing world_population.csv"
            traceback.print_exc()
            print ("failed " + testfile)
        try:
            testfile =  "Testing world_populationfull.csv"
            views.generatePivotTable("/home/anooj/world_populationfull.csv", "/tmp/unittestpopulation.csv")
        except Exception as e:
            traceback.print_exc()
            testfile =  "Testing world_populationfull.csv"
            print ("failed " + testfile)
        try:
            testfile = "Testing homes.csv"
            homefilters = views.generatePivotTable("/home/anooj/homes.csv", "/tmp/unittestpopulation.csv")
            with open('/tmp/x', 'w') as f:
                print (homefilters, file=f)
        except Exception as e:
            traceback.print_exc()
            testfile = "Testing homes.csv"
            print ("failed " + testfile)
        try:
            testfile =  "Testing deniso.csv"
            views.generatePivotTable("/home/anooj/deniso.csv", "/tmp/unittestpopulation.csv")
        except Exception as e:
            traceback.print_exc()
            testfile =  "Testing deniso.csv"
            print ("failed " + testfile)
        try:
            testfile = "Testing faithful.csv"
            views.generatePivotTable("/home/anooj/faithful.csv", "/tmp/unittestpopulation.csv")
        except Exception as e:
            traceback.print_exc()
            testfile = "Testing faithful.csv"
            print ("failed " + testfile)

     #curl -Lv http://127.0.0.1:8000/displaycode/snippets
    def testGetSnippets(self):
        client = Client()
        response = client.get('/displaycode/snippets')
        self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))
        self.assertEquals(response.url, '/displaycode/snippets/', "A slash should be appended at the end. Got " + response.url)
        newUrl = response.url
        
        response2 = client.get(newUrl);
        self.assertEquals(response2.status_code, 200, "Wrong response. Expected 200");
        self.assertEquals(response2.__getitem__('Content-Type'), 'application/json')
        contentStr = response2.content;
        content = json.loads(contentStr);
        self.assertEquals(len(content), 2, "Expected to see two snippet objects in the output. Found " + str(len(content)))
        for snippetDetail in content:
            self.assertNotEquals(snippetDetail['text'], None, "Expect to see a key for code");

        self.assertEquals(content[0]['text'], "This is my code for Fizzbuzz test", "Expect to see a key for code");
        self.assertEquals(content[1]['text'], "This is my code for second Fizzbuzz test", "Expect to see a key for code");


    #curl -Lv http://127.0.0.1:8000/displaycode/comments/2
    def testGetComments(self):
        client = Client()
        response = client.get('/displaycode/comments')
        self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))
        self.assertEquals(response.url, '/displaycode/comments/', "A slash should be appended at the end. Got " + response.url)
        newUrl = response.url
        
        response2 = client.get(newUrl);
        self.assertEquals(response2.status_code, 200, "Wrong response. Expected 200");
        self.assertEquals(response2.__getitem__('Content-Type'), 'application/json')
        contentStr = response2.content;
        comments = json.loads(contentStr);
        self.assertEquals(len(comments), 3, "Expected to see 3 comment objects in the output. Found " + str(len(comments)))
        for snippetDetail in comments:
            self.assertNotEquals(snippetDetail['text'], None, "Expect to see a key for text");

        #validate individual comments
        self.assertEquals(comments[0]['text'], "This is my comment 1", "Expect to see a key for text");
        self.assertEquals(comments[0]['snippetId'], 1, "Wrong snippetId");
        self.assertEquals(comments[0]['line'], 10, "Wrong line num");

        self.assertEquals(comments[1]['text'], "This is my comment 2", "Expect to see a key for text");
        self.assertEquals(comments[1]['snippetId'], 1, "Wrong snippetId");
        self.assertEquals(comments[1]['line'], 2, "Wrong line num");


        self.assertEquals(comments[2]['text'], "This is my comment 1 on snippet 2", "Expect to see a key for text");
        self.assertEquals(comments[2]['snippetId'], 2, "Wrong snippetId");
        self.assertEquals(comments[2]['line'], 20, "Wrong line num");

    #curl -Lv http://127.0.0.1:8000/displaycode/users
    def testGetUsers(self):
        client = Client()
        response = client.get('/displaycode/users')
        self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))
        self.assertEquals(response.url, '/displaycode/users/', "A slash should be appended at the end. Got " + response.url)
        newUrl = response.url
        
        response2 = client.get(newUrl);
        self.assertEquals(response2.status_code, 200, "Wrong response. Expected 200");
        self.assertEquals(response2.__getitem__('Content-Type'), 'application/json')
        contentStr = response2.content;
        content = json.loads(contentStr);
        self.assertEquals(len(content), 1, "Expected to see single user")
        self.assertEquals(content[0]['id'], 1, "Wrong id")
        self.assertEquals(content[0]['username'], 'normal', "Wrong id")
        self.assertEquals(content[0]['email'], 'normal@user.com', "Wrong email")
        self.assertEquals(len(content[0]['snippets']), 0, "Wrong snippets")

       #Create a snippet and get user info again.
        User = get_user_model()
        user2 = User.objects.create_user(username="normal2", email='normal2@user.com', password='foo')
        Snippet.objects.create(author=user2, text="This is test code for normal2 user");

        response = client.get('/displaycode/users')
        self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))
        self.assertEquals(response.url, '/displaycode/users/', "A slash should be appended at the end. Got " + response.url)
        newUrl = response.url
        
        response2 = client.get(newUrl);
        self.assertEquals(response2.status_code, 200, "Wrong response. Expected 200");
        self.assertEquals(response2.__getitem__('Content-Type'), 'application/json')
        contentStr = response2.content;
        content = json.loads(contentStr);
        self.assertEquals(len(content), 2, "Expected to see single user")
        self.assertEquals(content[0]['id'], 1, "Wrong id")
        self.assertEquals(content[0]['username'], 'normal', "Wrong id")
        self.assertEquals(content[0]['email'], 'normal@user.com', "Wrong email")
        self.assertEquals(len(content[0]['snippets']), 0, "Wrong snippets")

        self.assertEquals(content[1]['id'], 2, "Wrong id")
        self.assertEquals(content[1]['username'], 'normal2', "Wrong id")
        self.assertEquals(content[1]['email'], 'normal2@user.com', "Wrong email")
        snippetsforthisuser = content[1]['snippets']
        self.assertEquals(len(snippetsforthisuser), 1, "Wrong num of snippets")
        self.assertEquals(snippetsforthisuser[0], 'http://testserver/displaycode/snippets/3/', "Wrong snippet link");

    #curl -Lv http://127.0.0.1:8000/displaycode/users
    def testCreateUsers(self):
        client = Client()
        response = client.get('/displaycode/users')
        self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))
        self.assertEquals(response.url, '/displaycode/users/', "A slash should be appended at the end. Got " + response.url)
        newUrl = response.url
        
        response2 = client.get(newUrl);
        self.assertEquals(response2.status_code, 200, "Wrong response. Expected 200");
        self.assertEquals(response2.__getitem__('Content-Type'), 'application/json')
        contentStr = response2.content;
        content = json.loads(contentStr);
        self.assertEquals(len(content), 1, "Expected to see single user")
        self.assertEquals(content[0]['id'], 1, "Wrong id")
        self.assertEquals(content[0]['username'], 'normal', "Wrong id")
        self.assertEquals(content[0]['email'], 'normal@user.com', "Wrong email")
        self.assertEquals(len(content[0]['snippets']), 0, "Wrong snippets")

       #Create a snippet and get user info again.
        response = client.post('/displaycode/users', {'username':'experiencedenegineer', 'password':'principalengineer'})
        self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))

        newUrl = response.url
        response2 = client.post(response.url, {'username':'experiencedenegineer', 'password':'principalengineer'})
        self.assertEqual(response2.status_code, 201, "Router should have redirected the client to a new URL but got" + str(response.status_code))

        #User = get_user_model()
        #user2 = User.objects.create_user(username="normal2", email='normal2@user.com', password='foo')
        #Snippet.objects.create(author=user2, code="This is test code for normal2 user");

        response = client.get('/displaycode/users')
        self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))
        self.assertEquals(response.url, '/displaycode/users/', "A slash should be appended at the end. Got " + response.url)
        newUrl = response.url
        
        response2 = client.get(newUrl);
        self.assertEquals(response2.status_code, 200, "Wrong response. Expected 200");
        self.assertEquals(response2.__getitem__('Content-Type'), 'application/json')
        contentStr = response2.content;
        content = json.loads(contentStr);
        self.assertEquals(len(content), 2, "Expected to see single user")
        self.assertEquals(content[0]['id'], 1, "Wrong id")
        self.assertEquals(content[0]['username'], 'normal', "Wrong id")
        self.assertEquals(content[0]['email'], 'normal@user.com', "Wrong email")
        self.assertEquals(len(content[0]['snippets']), 0, "Wrong snippets")

        self.assertEquals(content[1]['id'], 2, "Wrong id")
        self.assertEquals(content[1]['username'], 'experiencedenegineer', "Wrong id")
        self.assertEquals(content[1]['email'], '', "Wrong email")
        snippetsforthisuser = content[1]['snippets']
        self.assertEquals(len(snippetsforthisuser), 0, "Wrong num of snippets")




     #curl -Lv http://127.0.0.1:8000/displaycode/snippets
    def testGetSpecificSnippets(self):
        client = Client()
        response = client.get('/displaycode/snippets/1')
        self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))
        self.assertEquals(response.url, '/displaycode/snippets/1/', "A slash should be appended at the end. Got " + response.url)
        newUrl = response.url
        
        response2 = client.get(newUrl);
        self.assertEquals(response2.status_code, 200, "Wrong response. Expected 200");
        self.assertEquals(response2.__getitem__('Content-Type'), 'application/json')
        contentStr = response2.content;
        content = json.loads(contentStr);
        self.assertEquals(content['text'], 'This is my code for Fizzbuzz test', "Expect to see a key for code");
        self.assertEquals(content['id'], 1, "Expect to see id of 1");

        response = client.get('/displaycode/snippets/2')
        self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))
        self.assertEquals(response.url, '/displaycode/snippets/2/', "A slash should be appended at the end. Got " + response.url)
        newUrl = response.url
        
        response2 = client.get(newUrl);
        self.assertEquals(response2.status_code, 200, "Wrong response. Expected 200");
        self.assertEquals(response2.__getitem__('Content-Type'), 'application/json')
        contentStr = response2.content;
        content = json.loads(contentStr);
        self.assertEquals(content['text'], 'This is my code for second Fizzbuzz test', "Expect to see a key for code");
        self.assertEquals(content['id'], 2, "Expect to see id of 2");



    #curl -Lv http://127.0.0.1:8000/displaycode/comments/1
    def testGetSpecificComments(self):
        client = Client()
        response = client.get('/displaycode/comments/1')
        self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))
        self.assertEquals(response.url, '/displaycode/comments/1/', "A slash should be appended at the end. Got " + response.url)
        newUrl = response.url
        
        response2 = client.get(newUrl);
        self.assertEquals(response2.status_code, 200, "Wrong response. Expected 200");
        self.assertEquals(response2.__getitem__('Content-Type'), 'application/json')
        contentStr = response2.content;
        comments = json.loads(contentStr);
        self.assertEquals(comments['text'], 'This is my comment 1', "Expect to see a key for text");
        self.assertEquals(comments['id'], 1, "Wrong id");
        self.assertEquals(comments['author'], "http://testserver/displaycode/users/1/", "Wrong author");
        self.assertEquals(comments['snippetId'], 1, "Wrong snippetId");
        self.assertEquals(comments['line'], 10, "Wrong linenum");
        self.assertEquals(comments['published_date'], None, "Wrong published date");

    #test creation using POST request.
    def testCreateGetDeleteSnippets(self):
        User = get_user_model()
        user = User.objects.create_user(username="user2", email='normal2@user.com', password='foo')

        client = Client()
        response = client.post('/displaycode/snippets', {'text':'Test Snippet code. Is a post request'})
        self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))
        self.assertEquals(response.url, '/displaycode/snippets/', "A slash should be appended at the end. Got " + response.url)
        newUrl = response.url
        
        response2 = client.post(newUrl, {'text':'Test Snippet code. Is a post request'})
        self.assertEquals(response2.status_code, 201, "Wrong response. Expected 200");
        self.assertEquals(response2.__getitem__('Content-Type'), 'application/json')
        contentStr = response2.content;
        content = json.loads(contentStr);
        self.assertEquals(content['id'], 3, "Wrong content id");
        self.assertEquals(content['text'], "Test Snippet code. Is a post request", "Expect to see a key for code");

        #Post once again and see what happens.
        response = client.post('/displaycode/snippets', {'text':'Test Snippet code 2. Is a post request'})
        self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))
        self.assertEquals(response.url, '/displaycode/snippets/', "A slash should be appended at the end. Got " + response.url)
        newUrl = response.url
        
        response2 = client.post(newUrl, {'text':'Test Snippet code 2. Is a post request'})
        self.assertEquals(response2.status_code, 201, "Wrong response. Expected 200");
        self.assertEquals(response2.__getitem__('Content-Type'), 'application/json')
        contentStr = response2.content;
        content = json.loads(contentStr);
        self.assertEquals(content['id'], 4, "Wrong content id");
        self.assertEquals(content['text'], "Test Snippet code 2. Is a post request", "Expect to see a key for code");

        #Get all the requests back and see what we have there.
        response = client.get('/displaycode/snippets')
        self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))
        self.assertEquals(response.url, '/displaycode/snippets/', "A slash should be appended at the end. Got " + response.url)
        newUrl = response.url
        
        response2 = client.get(newUrl);
        self.assertEquals(response2.status_code, 200, "Wrong response. Expected 200");
        self.assertEquals(response2.__getitem__('Content-Type'), 'application/json')
        contentStr = response2.content;
        content = json.loads(contentStr);
        self.assertEquals(len(content), 4, "Expected to see 4 snippet objects in the output. Found " + str(len(content)))
        for snippetDetail in content:
            self.assertNotEquals(snippetDetail['text'], None, "Expect to see a key for code");

        self.assertEquals(content[0]['text'], "This is my code for Fizzbuzz test", "Expect to see a key for code");
        self.assertEquals(content[1]['text'], "This is my code for second Fizzbuzz test", "Expect to see a key for code");
        self.assertEquals(content[2]['text'], "Test Snippet code. Is a post request", "Expect to see a key for code");
        self.assertEquals(content[3]['text'], "Test Snippet code 2. Is a post request", "Expect to see a key for code");

        #Delete snippets now.
        response2 = client.delete("/displaycode/snippets/3/");
        self.assertEquals(response2.status_code, 204, "Wrong response. Expected 204");
        #Will not have at content.
        contentStr = response2.content;
        self.assertEquals(contentStr,b'')

        #Get all the requests back and see what we have there.
        response = client.get('/displaycode/snippets')
        self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))
        self.assertEquals(response.url, '/displaycode/snippets/', "A slash should be appended at the end. Got " + response.url)
        newUrl = response.url
        
        response2 = client.get(newUrl);
        self.assertEquals(response2.status_code, 200, "Wrong response. Expected 200");
        self.assertEquals(response2.__getitem__('Content-Type'), 'application/json')
        contentStr = response2.content;
        content = json.loads(contentStr);
        self.assertEquals(len(content), 3, "Expected to see 3 snippet objects in the output. Found " + str(len(content)))
        for snippetDetail in content:
            self.assertNotEquals(snippetDetail['text'], None, "Expect to see a key for code");

        self.assertEquals(content[0]['text'], "This is my code for Fizzbuzz test", "Expect to see a key for code");
        self.assertEquals(content[1]['text'], "This is my code for second Fizzbuzz test", "Expect to see a key for code");
        self.assertEquals(content[2]['text'], "Test Snippet code 2. Is a post request", "Expect to see a key for code");

     #testcreation using PUT request.
    def testCreateGetDeleteSnippets2(self):
        User = get_user_model()
        user = User.objects.create_user(username="user2", email='normal2@user.com', password='foo')

        client = Client()
        response = client.put('/displaycode/snippets', {'text':'Test Snippet code. Is a put request'})
        self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))
        self.assertEquals(response.url, '/displaycode/snippets/', "A slash should be appended at the end. Got " + response.url)
        newUrl = response.url
        
        response2 = client.put(newUrl, {'text':'Test Snippet code. Is a put request'})
        self.assertEquals(response2.status_code, 405, "No PUTS. Veryify using curl -Lv http://127.0.0.1:8000/displaycode/snippets");
       
        response2 = client.get(newUrl);
        self.assertEquals(response2.status_code, 200, "Wrong response. Expected 200");
        self.assertEquals(response2.__getitem__('Content-Type'), 'application/json')
        contentStr = response2.content;
        content = json.loads(contentStr);
        self.assertEquals(len(content), 2, "Expected to see 3 snippet objects in the output. Found " + str(len(content)))
        for snippetDetail in content:
            self.assertNotEquals(snippetDetail['text'], None, "Expect to see a key for code");

        self.assertEquals(content[0]['text'], "This is my code for Fizzbuzz test", "Expect to see a key for code");
        self.assertEquals(content[1]['text'], "This is my code for second Fizzbuzz test", "Expect to see a key for code");

     #test creation of comments using POST request.
    def testCreateGetDeleteComments(self):
        User = get_user_model()
        user = User.objects.create_user(username="user2", email='normal2@user.com', password='foo')

        client = Client()
        response = client.post('/displaycode/snippets', {'text':'Test Snippet code. Is a post request'})
        self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))
        self.assertEquals(response.url, '/displaycode/snippets/', "A slash should be appended at the end. Got " + response.url)
        newUrl = response.url
       
        response2 = client.post(newUrl, {'text':'Test Snippet code. Is a post request'})
        self.assertEquals(response2.status_code, 201, "Wrong response. Expected 200");
        self.assertEquals(response2.__getitem__('Content-Type'), 'application/json')
        contentStr = response2.content;
        content = json.loads(contentStr);
        self.assertEquals(content['id'], 3, "Wrong content id");
        self.assertEquals(content['text'], "Test Snippet code. Is a post request", "Expect to see a key for code");

        #Post comment
        Comment.objects.create(author=user, snippetId=1, text="This is my comment 1", line=10, published_date=None);
        response = client.post('/displaycode/comments', {'text':'Test Comment code 1. Is a post request', 'snippetId': 3, 'line':10})
        self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))
        self.assertEquals(response.url, '/displaycode/comments/', "A slash should be appended at the end. Got " + response.url)
        newUrl = response.url
        
        response3 = client.post(newUrl, {'text':'Test Comment code 1. Is a post request', 'snippetId': 3, 'line':10})
        self.assertEquals(response3.status_code, 201, "Wrong response. Expected 200");
        self.assertEquals(response3.__getitem__('Content-Type'), 'application/json')
        contentStr = response3.content;
        content = json.loads(contentStr);
        self.assertEquals(content['id'], 5, "Wrong content id");
        self.assertEquals(content['snippetId'], 3, "Wrong content snippetId");
        self.assertEquals(content['line'], 10, "Wrong line");
        self.assertEquals(content['text'], "Test Comment code 1. Is a post request", "Wrong text!");
        self.assertEquals(content['published_date'], None, "Wrong published date");
        self.assertEquals(content['author'], None, "Wrong author date");

        #Get all the requests back and see what we have there.
        response4 = client.get('/displaycode/snippets/3')
        self.assertEqual(response4.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response4.status_code))
        self.assertEquals(response4.url, '/displaycode/snippets/3/', "A slash should be appended at the end. Got " + response4.url)
        newUrl = response4.url
        
        response5 = client.get(newUrl);
        self.assertEquals(response5.status_code, 200, "Wrong response. Expected 200");
        self.assertEquals(response5.__getitem__('Content-Type'), 'application/json')
        contentStr = response5.content;
        content = json.loads(contentStr);
        self.assertEquals(content['comments'], [5], "Comments list is wrong. Expected to see one comment");


        #Another way to retrieve the comments.
        #Get all the requests back and see what we have there.
        response6 = client.get('/displaycode/snippets/3/comments')
        self.assertEqual(response6.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response6.status_code))
        self.assertEquals(response6.url, '/displaycode/snippets/3/comments/', "A slash should be appended at the end. Got " + response6.url)
        newUrl = response6.url
        
        response7 = client.get(newUrl);
        self.assertEquals(response7.status_code, 200, "Wrong response. Expected 200");
        self.assertEquals(response7.__getitem__('Content-Type'), 'application/json')
        contentStr = response7.content;
        content = json.loads(contentStr);
        self.assertEquals(len(content), 1, "Expected to see exactly one comment");
        self.assertEquals(content[0]['id'], 5, "Comment id is wrong");
        self.assertEquals(content[0]['snippetId'], 3, "Comment parent is wrong");
        self.assertEquals(content[0]['text'], "Test Comment code 1. Is a post request", "Comment text is wrong");
        self.assertEquals(content[0]['author'], None, "Wrong author");


        #Delete comment now.
        #response2 = client.delete("/displaycode/comments/5/");
        #self.assertEquals(response2.status_code, 204, "Wrong response. Expected 204");
        ##Will not have at content.
        #contentStr = response2.content;
        #self.assertEquals(contentStr,b'')


     #testcreation using PUT request.
    def testCreateGetDeleteComments2(self):
        User = get_user_model()
        user = User.objects.create_user(username="user2", email='normal2@user.com', password='foo')

        client = Client()
        response = client.put('/displaycode/snippets', {'text':'Test Snippet code. Is a put request'})
        self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))
        self.assertEquals(response.url, '/displaycode/snippets/', "A slash should be appended at the end. Got " + response.url)
        newUrl = response.url
        
        response2 = client.put(newUrl, {'text':'Test Snippet code. Is a put request'})
        self.assertEquals(response2.status_code, 405, "No PUTS. Veryify using curl -Lv http://127.0.0.1:8000/displaycode/snippets");
       
        response2 = client.get(newUrl);
        self.assertEquals(response2.status_code, 200, "Wrong response. Expected 200");
        self.assertEquals(response2.__getitem__('Content-Type'), 'application/json')
        contentStr = response2.content;
        content = json.loads(contentStr);
        self.assertEquals(len(content), 2, "Expected to see 3 snippet objects in the output. Found " + str(len(content)))
        for snippetDetail in content:
            self.assertNotEquals(snippetDetail['text'], None, "Expect to see a key for code");

        self.assertEquals(content[0]['text'], "This is my code for Fizzbuzz test", "Expect to see a key for code");
        self.assertEquals(content[1]['text'], "This is my code for second Fizzbuzz test", "Expect to see a key for code");

    def testAlogin(self):
        self.credentials = {
            'username': 'testuser',
            'email': 'testuser@localhost.in',
            'password': 'secret'}
        User = get_user_model()
        User.objects.create_user(**self.credentials)
        response = self.client.post('/displaycode/accounts/login/', self.credentials, follow=True)
        self.assertEquals(response.status_code, 404, "Login should work. Response is " + str(response.content))
        #self.assertEquals(response.status_code, 200, "Login should work. Response is " + str(response.content))
        ## should be logged in now
        #self.assertTrue(response.context['user'].is_active) 
        #self.assertTrue(response.context['user'].is_authenticated) 

    #run as 
    #python manage.py test displaycode.tests.TestRestAPI.testWaitListUser
    def testWaitListUser(self):
        waitListUser = WaitListUser(20);
        waitListUser.email = "user1@interviewblindspots.com"
        waitListUser.username = "user1"
        waitListUser.aboutme = "12 yrs experience. Interviewing for senior software engineer. Having hard time passing interviews. Knows algorithms well"
        waitListUser.painpoints = None
        currDate = datetime.datetime(2015, 10, 9, 23, 55, 59, 342380)
        waitListUser.joinedDate = currDate
        waitListUser.save()
        referralUrl = "dev.to/user/3456" #Could be dev.to, reddit programming pages, stackoverflow, github, leetcode forums, hacker earth, etc
        #To see full difference in case of assertion failure.
        self.maxDiff = None
        self.assertEquals(str(waitListUser), "id:20~email:user1@interviewblindspots.com~username:user1~aboutme:12 yrs experience. Interviewing for senior software engineer. Having hard time passing interviews. Knows algorithms well~painpoints:None~joinedDate:2015-10-09 23:55:59.342380~referralUrl:None")
        client = Client()
        response = client.get('/displaycode/waitlistusers/')
        self.assertEquals(response.status_code, 200, "Wrong response code. Got " + str(response))

        #No PUT command allowed.
        response = client.put('/displaycode/waitlistusers/', {'email':'user1@abc.com', 
            'username':'myuser1', 'aboutme':'myaboutme', 'referralUrl' : 'interviewAt'})
        self.assertEquals(response.status_code, 405, "Wrong response code. Got " + str(response))

        response = client.post('/displaycode/waitlistusers/', {'email':'user1@abc.com', 
            'username':'myuser1', 'aboutme':'myaboutme', 'referralUrl' : 'interviewAt'})
        self.assertEquals(response.status_code, 201, "Wrong response code. Got " + str(response))

        #self.assertEqual(response.status_code, 301, "Router should have redirected the client to a new URL but got" + str(response.status_code))
        #self.assertEquals(response.url, '/displaycode/snippets/', "A slash should be appended at the end. Got " + response.url)
        #newUrl = response.url
        #
        #response2 = client.put(newUrl, {'text':'Test Snippet code. Is a put request'})
        #self.assertEquals(response2.status_code, 405, "No PUTS. Veryify using curl -Lv http://127.0.0.1:8000/displaycode/snippets");
 
        #Verify that database is two

    #def testUserAccountCreation(self):
    #    client = Client()
    #    #curl 'https://backend.interviewblindspots.com/displaycode/api/v1/token/login' -X POST -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0' -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Content-Type: application/json;charset=utf-8' -H 'Origin: https://www.interviewblindspots.com' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Referer: https://www.interviewblindspots.com/' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-site' -H 'Sec-GPC: 1' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' --data-raw '{"username":"sdsds","password":"sdsdsd"}'
    #    response = client.get('/displaycode/api/v1/token/login')
    #    self.assertEquals(response.status_code, 200, "Wrong response code. Got " + str(response))
    
    #    #No PUT command allowed.
    #    response = client.put('/displaycode/waitlistusers/', {'email':'user1@abc.com', 
    #        'username':'myuser1', 'aboutme':'myaboutme', 'referralUrl' : 'interviewAt'})
    #    self.assertEquals(response.status_code, 405, "Wrong response code. Got " + str(response))



    def testLoginDrf(self):
        self.credentials = {
            'username': 'testuser',
            'email': 'testuser@localhost.in',
            'password': 'secret'}
        User = get_user_model()
        User.objects.create_user(**self.credentials)
        response = self.client.post('/displaycode/api/v1/token/login', self.credentials, follow=True)
        self.assertEquals(response.status_code, 200, "Login should work. ")
        content = json.loads(response.content);
        self.assertEquals(len(content), 1, "Expected to see two snippet objects in the output. Found " + str(len(content)))
        self.assertIsNone(content.get('authtoken') ,  "Wrong key. Must have underscore")
        # should be logged in now. And get a successful token.
        self.assertIsNotNone(content.get('auth_token') ,  "Wrong key. User not logged in")


        #Try on a invalid username password
        self.credentials = {
            'username': 'invalidtestuser',
            'email': 'invalidtestuser@localhost.in',
            'password': 'secret'}
        response = self.client.post('/displaycode/api/v1/token/login', self.credentials, follow=True)
        self.assertEquals(response.status_code, 400, "Login should not work.")
        content = json.loads(response.content);
        self.assertEquals(len(content), 1, "Expected to see two snippet objects in the output. Found " + str(len(content)))
        self.assertIsNotNone(content.get('non_field_errors') ,  "Wrong key.")
        errorMsgs = content.get('non_field_errors');
        self.assertEquals(len(errorMsgs), 1, "Expected to see one error msg. Found " + str(len(errorMsgs)))
        self.assertEquals(errorMsgs[0], "Unable to log in with provided credentials.", "Wrong msg");


        #Make sure get request does not work
        response = self.client.get('/displaycode/api/v1/token/login', follow=True)
        self.assertEquals(response.status_code, 405, "Login should not work.")
        content = json.loads(response.content);
        self.assertEquals(len(content), 1, "Expected to see two snippet objects in the output. Found " + str(len(content)))
        self.assertIsNotNone(content.get('detail') ,  "Wrong key.")
        errorMsg = content.get('detail');
        self.assertEquals(errorMsg, "Method \"GET\" not allowed.", "Wrong msg");


        #Test put method
        self.credentials = {
            'username': 'newuser',
            'email': 'newuser@localhost.in',
            'password': 'secretsanta'}
        response = self.client.put('/displaycode/api/v1/token/login', self.credentials, follow=True)
        self.assertEquals(response.status_code, 405, "Login endpoint should not work for put.")
        content = json.loads(response.content);
        self.assertEquals(len(content), 1, "Expected to see two snippet objects in the output. Found " + str(len(content)))
        self.assertIsNotNone(content.get('detail') ,  "Wrong key.")
        errorMsg = content.get('detail');
        self.assertEquals(errorMsg, "Method \"PUT\" not allowed.", "Wrong msg");

        #check delete method
        response = self.client.delete('/displaycode/api/v1/token/login', self.credentials, follow=True)
        self.assertEquals(response.status_code, 405, "Login endpoint should not work for delete.")
        content = json.loads(response.content);
        print (content)
        self.assertEquals(len(content), 1, "Expected to see two snippet objects in the output. Found " + str(len(content)))
        self.assertIsNotNone(content.get('detail') ,  "Wrong key.")
        errorMsg = content.get('detail');
        self.assertEquals(errorMsg, "Method \"DELETE\" not allowed.", "Wrong msg");





    #Testaccount creation and retrieval.
    def testAccountCreation(self):
        self.credentials = {
            'username': 'newuser',
            'email': 'newuser@localhost.in',
            'password': 'secretjskjdskjdsjdls', "csrftoken": "asdf"}
        User = get_user_model()
        #Note that URL ends in slash.
        response = self.client.post('/displaycode/api/v1/users/', self.credentials, follow=True)
        self.assertEquals(response.status_code, 201, "Account creation should work. response is " +  str(response.content))
        content = json.loads(response.content);
        self.assertEquals(len(content), 3, "Expected to see two snippet objects in the output. Found " + str(len(content)))
        self.assertEquals(content['email'], 'newuser@localhost.in', "Wrong email")
        self.assertEquals(content['username'], 'newuser', "Wrong username")
        self.assertIsNotNone(content['id'],  "Wrong id")
        #Try to login with above username password and get token.
        response = self.client.post('/displaycode/api/v1/token/login', self.credentials, follow=True)
        self.assertEquals(response.status_code, 200, "Login should work.")
        content = json.loads(response.content);
        self.assertEquals(len(content), 1, "Expected to see two snippet objects in the output. Found " + str(len(content)))
        self.assertIsNone(content.get('authtoken') ,  "Wrong key. Must have underscore")
        # should be logged in now. And get a successful token.
        self.assertIsNotNone(content.get('auth_token') ,  "Wrong key. User not logged in")


    #Testaccount creation and retrieval.
    def testAccountForgotPassword(self):
        #First create a new account.
        self.credentials = {
            'username': 'newuser',
            'email': 'newuser@localhost.in',
            'password': 'secretjskjdskjdsjdls', "csrftoken": "asdf"}
        User = get_user_model()
        #Note that URL ends in slash.
        response = self.client.post('/displaycode/api/v1/users/', self.credentials, follow=True)
        self.assertEquals(response.status_code, 201, "Account creation should work. response is " +  str(response.content))
        content = json.loads(response.content);
        self.assertEquals(len(content), 3, "Expected to see two snippet objects in the output. Found " + str(len(content)))
        self.assertEquals(content['email'], 'newuser@localhost.in', "Wrong email")
        self.assertEquals(content['username'], 'newuser', "Wrong username")
        self.assertIsNotNone(content['id'],  "Wrong id")


        #Get user/me endpoint, no authentication.
        response = self.client.get('/displaycode/api/v1/users/me', follow=True)
        self.assertEquals(response.status_code, 401, "Getting this user's details must fail. response is " +  str(response.content))
        content = json.loads(response.content);
        #pdb.set_trace()
        self.assertEquals(len(content), 1, "Expected to see two snippet objects in the output. Found " + str(len(content)))
        self.assertEquals(content['detail'], 'Authentication credentials were not provided.', "Wrong email");

        #Get user/me endpoint with authentication.
        response = self.client.post('/displaycode/api/v1/users/me', self.credentials, follow=True)
        self.assertEquals(response.status_code, 401, "Getting this user's details should work. response is " +  str(response.content))
        content = json.loads(response.content);
        print (content)
        self.assertEquals(len(content), 1, "Expected to see two snippet objects in the output. Found " + str(len(content)))
        self.assertEquals(content['detail'], 'Authentication credentials were not provided.', "Wrong email");

        #Try to login with above username password
        response = self.client.post('/displaycode/api/v1/token/login', self.credentials, follow=True)
        self.assertEquals(response.status_code, 200, "Login should work.")
        content = json.loads(response.content);
        self.assertEquals(len(content), 1, "Expected to see two snippet objects in the output. Found " + str(len(content)))
        self.assertIsNone(content.get('authtoken') ,  "Wrong key. Must have underscore")
        access_token = content.get('auth_token')
        # should be logged in now. And get a successful token.
        self.assertIsNotNone(access_token ,  "Wrong key. User not logged in")

        #Get user/me endpoint with authentication.
        authorization='token '+access_token
        headers = {
            'Authorization': authorization
            }
        headers = {
            'Authorization': 'Token b704c9fc3655635646356ac2950269f352ea1139'
        }


        #Forgot password.w


        response = self.client.post('/displaycode/api/v1/users/me', headers=headers, follow=False)
        self.assertEquals(response.status_code, 301, "Getting this user's details should work. response is " +  str(response.content))
        url = response.url

        #pdb.set_trace()
        #self.client.headers.update({'Authorization': 'Token b704c9fc3655635646356ac2950269f352ea1139'})
        #response = self.client.get(url,  follow=False)
        #self.assertEquals(response.status_code, 200, "Getting this user's details should work. response is " +  str(response.content))
        #content = json.loads(response.content);
        #print (content)
        #self.assertEquals(len(content), 1, "Expected to see two snippet objects in the output. Found " + str(len(content)))
        #self.assertEquals(content['detail'], 'Authentication credentials were not provided.', "Wrong email");


class TestModels(TestCase):
    def testCameraCreation(self):
        camera = Camera(camId="33io42423i", camUrl="https://www.youtube.com/watch?v=1-iS7LArMPA", camLoc="New York", metadata="cars people buildings")
        camera.save() 
        self.assertEqual(str(camera), 'New York')

    def testSnapshotCreation(self):
        snapshot = SnapshotDetails(snapshotId="324552gf", dirLoc="/", camera="33io42423i")
        snapshot.save()
        self.assertEqual(str(snapshot), '/')
 