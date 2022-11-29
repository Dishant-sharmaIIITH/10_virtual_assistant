from flask import Flask,render_template,request,redirect,url_for,jsonify,Blueprint
from flask_executor import Executor
from bson.objectid import ObjectId
import speech_recognition as spr 
import time
import webbrowser
import playsound
import os
import random
from flask_assistant import ask,Assistant
from gtts  import gTTS
import pymongo
from spc import speak,record_voice,respond,record_notes,response_notes,record_rem


# Importing required libraries
from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup
import re
import time
import dateutil.parser as parser
from datetime import datetime
import datetime
import csv
import json
import json
import pandas as pd
import datefinder
	
# from read import *

app=Flask(__name__)
executor = Executor(app)
client=pymongo.MongoClient('mongodb://127.0.0.1:27017/')

recog=spr.Recognizer()

# def speak(answer):
#     tts=gTTS(text=answer,lang='en')
#     r=random.randint(1,100000)
#     file_name='audio-'+str(r)+'.mp3'
#     tts.save(file_name)
#     playsound.playsound(file_name)
#     print(file_name)
#     os.remove(file_name)










# speak("Hello My name is aagyaa i am your virtual assistant, Please press the mic button from right corner to enabe me in voice mode")
# while 1:
#     voice=record_voice()
#     respond(voice)
        

email=""



def hello():
    ask('Hello bolo')

def say():
    speak("Hello, My name is aagyaa, I am your virtual assistant, Please press the mic button from right corner to enable me in voice mode.")





mydb=client['User_info']
table=mydb.User_info
reminder_collection=mydb.reminder
note_collection=mydb.note

# speak("Hello, My name is aagyaa, I am your virtual assistant, Please press the mic button from right corner to enabe me in voice mode")

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/remainder')
def showremainder():
    return render_template('remainder.html')

@app.route('/dashboard/aagyaa',methods=['POST'])
def haagyaa():
    print('aagyaa')
    speak('How Can I Help You')
    lock=[1,'null']
    while lock[0]:
        voice=record_voice()
        lock=respond(voice)
        if(lock[1]!='null'):
            return render_template(lock[1])

@app.route('/notes/aagyaa',methods=['POST'])
def notesaagyaa():
    print('aagyaa')
    
    ret=[]
    speak('Please Enter title')
    temp=''
    while temp=='':
        temp=record_rem()
    ret.append(temp)
    temp=''
    speak('OK, Please Enter text')
    while temp=='':
        temp=record_rem()
    ret.append(temp)
    speak('Ok')
    return redirect(url_for('add_note_voice',title=ret[0],text=ret[1]))

@app.route('/remainder/aagyaa',methods=['POST'])
def remainderaagyaa():
    print('aagyaa')
    ret=[]
    speak('Please Enter task')
    temp=''
    while temp=='':
        temp=record_rem()
    ret.append(temp)
    temp=''
    speak('OK, Please Enter DATE')
    while temp=='':
        temp=record_rem()
    ret.append(temp)
    temp=''
    speak('OK, Please Enter time')
    while temp=='':
        temp=record_rem()
    ret.append(temp)
    speak('Ok')
    return redirect(url_for('add_reminder_voice',tag=ret[0],date=ret[1],time=ret[2]))


@app.route('/add_reminder_voice/<tag>/<date>/<time>')
def add_reminder_voice(tag,date,time):
    # reminder_collection=mongo.db.reminder
    user_logged=table.find_one({'isLoggedIn':True})
    
    email=user_logged['email']
    reminder_title=tag
    reminder_date=date
    reminder_time=time
    # reminder_info=request.form.get('reminder-info')
    # reminder_frequency=request.form.get('reminder-frequency')
    reminder_collection.insert_one({'user_email':email,'title':reminder_title, 'date':reminder_date, 'time':reminder_time, 'complete':False})
    return redirect('/dashboard/showReminder')

@app.route('/add_note_voice/<title>/<text>')
def add_note_voice(title,text):
    user_logged=table.find_one({'isLoggedIn':True})
    email=user_logged['email']
    note_title=title
    note_text=text
    note_collection.insert_one({'user_email':email, 'title':note_title, 'text':note_text})
    return redirect('/dashboard/notes')


    
    


interest=""
@app.route('/send_user_info',methods=['POST'])
def send_user_info():
    global interest
    interest=request.form.get('interest')
    name=request.form.get('name')
    email=request.form.get('email')
    password=request.form.get('password')
    result=table.count_documents({'email':email})
    if(result!=0):
        return render_template('signup.html')
    else:
        table.insert_one({'email':email,'name':name,'password':password, 'interest':interest, 'isLoggedIn':False})
        # reminder_collection.insert_one({'email':email,'name':name,'password':password})
        return render_template('login.html')

    # return "Your email is {} and your password is {}".format(email,password)
    # return render_template('signup.html')

@app.route("/topicOfInterest",methods=['POST','GET'])
def TOI():
    user_logged=table.find_one({'isLoggedIn':True})
    email=user_logged['email']
    interest=user_logged['interest']
    if request.method == 'GET':
        message = {'TOI':interest}
        return jsonify(message)

@app.route('/login_valid',methods=['POST','GET'])
def login_valid():
    
    
    if request.method == 'POST':
        

        email=request.form.get('email')
        password=request.form.get('password')
        result=table.count_documents({'email':email,'password':password})
        if(result!=0):
            logged_user=table.find_one({'email':email})
            newvalues = { "$set": { 'isLoggedIn': True } }
            table.update_one(logged_user, newvalues)

           
            executor.submit(say)
            return render_template('dashboard.html')
        else:
            return render_template('login.html')
    if request.method == 'GET':
        user_logged=table.find_one({'isLoggedIn':True})
        email=user_logged['email']
        message = {'greeting':'Hello from Flask!','email':email}
        return jsonify(message)

@app.route('/dashboard/notes')
def shownotes():
    user_logged=table.find_one({'isLoggedIn':True})
    email=user_logged['email']
    notes=note_collection.find({'user_email':email})
    return render_template('notes.html',notes=notes)

@app.route('/add_note', methods=['POST'])
def add_note():
    user_logged=table.find_one({'isLoggedIn':True})
    email=user_logged['email']
    note_title=request.form.get('note-title')
    note_text=request.form.get('note-text')
    note_collection.insert_one({'user_email':email, 'title':note_title, 'text':note_text})
    return redirect('/dashboard/notes')
@app.route('/delete_note/<oid>')
def delete_note(oid):
    note_collection.delete_one({'_id':ObjectId(oid)})
    return redirect('/dashboard/notes')

@app.route('/dashboard')
def showdashboard():
    
    # speak("Hello, My name is aagyaa, I am your virtual assistant, Please press the mic button from right corner to enable me in voice mode.")
    return render_template('dashboard.html',interest=interest)

@app.route('/dashboard/showReminder')
def showReminder():
    # reminder_collection=mongo.db.reminder
    user_logged=table.find_one({'isLoggedIn':True})
    
    email=user_logged['email']

    reminderTitle, reminderDate, reminderTime = readFunction()
    
    
    for i in range(0, len(reminderDate)):
        reminder_title = reminderTitle[i]
        reminder_date = reminderDate[i]
        reminder_time = reminderTime[i]
        print(reminderTitle[i])
        print(reminderDate[i])
        print(reminderTime[i])
        reminder_collection.insert_one(
            {'user_email':email,'title': reminder_title, 'date': reminder_date, 'time': reminder_time, 'complete': False})

    reminders=reminder_collection.find({'user_email':email,'complete':False})
    return render_template('remainder.html', reminders=reminders)

	
@app.route('/view_complete_reminders')
def view_complete_reminders():
    user_logged=table.find_one({'isLoggedIn':True})
    email=user_logged['email']
    reminders=reminder_collection.find({'user_email':email,'complete':True})
    return render_template('completeReminders.html', reminders=reminders)


@app.route('/dashboard/gmail')
def showGmail():
    # reminder_collection=mongo.db.reminder
    # reminders=reminder_collection.find()
    return render_template('gmail.html')


@app.route('/add_reminder', methods=['POST'])
def add_reminder():
    # reminder_collection=mongo.db.reminder

    user_logged=table.find_one({'isLoggedIn':True})
    
    email=user_logged['email']
    reminder_title=request.form.get('reminder-title')
    reminder_date=request.form.get('reminder-date')
    reminder_time=request.form.get('reminder-time')
    # reminder_info=request.form.get('reminder-info')
    # reminder_frequency=request.form.get('reminder-frequency')
    reminder_collection.insert_one({'user_email':email,'title':reminder_title, 'date':reminder_date, 'time':reminder_time, 'complete':False})
    return redirect('/dashboard/showReminder')

@app.route('/edit_reminder/<oid>')
def edit_reminder(oid):
    # reminder_collection=mongo.db.reminder
    reminder_item=reminder_collection.find_one({'_id':ObjectId(oid)})
    return render_template('editReminder.html', reminder=reminder_item)

@app.route('/delete_reminder/<oid>')
def delete_reminder(oid):

    app. logger. warning(oid)
    # reminder_collection=mongo.db.reminder
    reminder_collection.delete_one({'_id':ObjectId(oid)})
    return redirect('/dashboard/showReminder')


@app.route('/complete_reminder/<oid>')
def complete_reminder(oid):
    # reminder_collection=mongo.db.reminder
    # return("hello complete")
    reminder_item=reminder_collection.find_one({'_id':ObjectId(oid)})
    newvalues = { "$set": { 'complete': True } }
    reminder_collection.update_one(reminder_item, newvalues)
    return redirect('/dashboard/showReminder')

@app.route('/incomplete_reminder/<oid>')
def incomplete_reminder(oid):
    reminder_item=reminder_collection.find_one({'_id':ObjectId(oid)})
    newvalues = { "$set": { 'complete': False } }
    reminder_collection.update_one(reminder_item, newvalues)
    return redirect('/dashboard/showReminder')

@app.route('/edit_reminder_form/<oid>', methods=['POST'])
def edit_reminder_form(oid):
    # reminder_collection=mongo.db.reminder
    reminder_item=reminder_collection.find_one({'_id':ObjectId(oid)})
    reminder_title=request.form.get('reminder-title')
    reminder_date=request.form.get('reminder-date')
    reminder_time=request.form.get('reminder-time')
    reminder_info=request.form.get('reminder-info')
    reminder_frequency=request.form.get('reminder-frequency')
    newvalues = { "$set": { 'title': reminder_title , 'date': reminder_date, 'time': reminder_time, 'info': reminder_info, 'frequency': reminder_frequency} }
    reminder_collection.update_one(reminder_item, newvalues)
    return redirect('/dashboard/showReminder')

@app.route('/logout')
def logout():
    user_logged=table.find_one({'isLoggedIn':True})
    newvalues = { "$set": { 'isLoggedIn': False } }
    table.update_one(user_logged, newvalues)
    return render_template('login.html')

    

    
    #return "Your email is {} and your password is {}".format(email,password)

# @app.route('/signup_data_send',methods=['POST'])
# def signup_data_send():


def readFunction():

    # Creating a storage.JSON file with authentication details
    # we are using modify and not readonly, as we will be marking the messages Read
    SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

    user_id = 'me'
    label_id_one = 'INBOX'
    label_id_two = 'UNREAD'

    # Getting all the unread messages from Inbox
    # labelIds can be changed accordingly
    unread_msgs = GMAIL.users().messages().list(
        userId='me', labelIds=[label_id_one, label_id_two]).execute()

    # print(unread_msgs)
    # We get a dictonary. Now reading values for the key 'messages'
    mssg_list = unread_msgs['messages']
    print("Total unread messages in inbox: ", str(len(mssg_list)))

    final_list = []
    # finalBodyMessage = ""
    temp_dict = {}

    def parse_msg(msg):
        # global finalBodyMessage
        finalBodyMessage = ""
        for i in msg.get("payload").get("parts")[:-1]:
            # print(base64.urlsafe_b64decode(
            # i["body"]["data"].encode("ASCII")).decode("utf-8"))
            # return base64.urlsafe_b64decode(msg.get("payload").get("body").get("data").encode("ASCII")).decode("utf-8")
            finalBodyMessage += base64.urlsafe_b64decode(
                i["body"]["data"].encode("ASCII")).decode("utf-8")

        return finalBodyMessage

    for mssg in mssg_list:
        temp_dict = {}
        m_id = mssg['id']  # get id of individual message
        message = GMAIL.users().messages().get(userId=user_id, id=m_id,
                                               format="full").execute()  # fetch the message using API

        # finalBodyMessage = msg.get("snippet")
        # return msg.get("snippet")

        # global finalBodyMessage

        # print("finalBodyMessage(): ", parse_msg(message))
        payld = message['payload']  # get payload of the message
        # print(payld)
        # for k in payld:
        #     print(payld[k], '\n')
        headr = payld['headers']  # get header of the payload

        for one in headr:  # getting the Subject
            if one['name'] == 'Subject':
                msg_subject = one['value']
                temp_dict['Subject'] = msg_subject
            else:
                pass

        for two in headr:  # getting the date
            if two['name'] == 'Date':
                msg_date = two['value']
                date_parse = (parser.parse(msg_date))
                m_date = (date_parse.date())
                temp_dict['Date'] = str(m_date)
            else:
                pass

        for three in headr:  # getting the Sender
            if three['name'] == 'From':
                msg_from = three['value']
                temp_dict['Sender'] = msg_from
            else:
                pass

        temp_dict['Snippet'] = message['snippet']  # fetching message snippet

        try:

            # Fetching message body
            # mssg_parts = payld['body']  # fetching the message parts
            # print(mssg_parts)
            # part_one = mssg_parts[0]  # fetching first element of the part
            # part_body = part_one['body']  # fetching body of the message
            # part_data = mssg_parts['data']  # fetching data from the body
            # print("PART DATA: ",part_data)
            part_data = parse_msg(message)
            # decoding from Base64 to UTF-8
            # clean_one = part_data.replace("-", "+")
            # decoding from Base64 to UTF-8
            # clean_one = clean_one.replace("_", "/")
            # decoding from Base64 to UTF-8
            # clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))
            # soup = BeautifulSoup(clean_two, "lxml")
            soup = BeautifulSoup(part_data, "lxml")
            mssg_body = soup.body()
            # mssg_body is a readible form of message body
            # depending on the end user's requirements, it can be further cleaned
            # using regex, beautiful soup, or any other method
            # print(mssg_body)
            temp_dict['Message_body'] = mssg_body

            # temp_dict['Message_body'] = parse_msg(message)

        except:
            pass

        # print(temp_dict)
        # This will create a dictonary item in the final list
        final_list.append(temp_dict)

        # This will mark the messagea as read
        GMAIL.users().messages().modify(userId=user_id, id=m_id,
                                        body={'removeLabelIds': ['UNREAD']}).execute()

    print("Total messaged retrived: ", str(len(final_list)))

    # exporting the values as .csv
    with open('CSV_NAME.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['Sender', 'Subject', 'Date', 'Snippet', 'Message_body']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        for val in final_list:
            writer.writerow(val)

    def csv_to_json(csvFilePath, jsonFilePath):
        jsonArray = []

        # read csv file
        with open(csvFilePath, encoding='utf-8') as csvf:
            # load csv file data using csv library's dictionary reader
            csvReader = csv.DictReader(csvf)

            # convert each csv row into python dict
            for row in csvReader:
                # add this python dict to json array
                jsonArray.append(row)

        # convert python jsonArray to JSON String and write to file
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            jsonString = json.dumps(jsonArray, indent=4)
            jsonf.write(jsonString)

    csvFilePath = r'CSV_NAME.csv'
    jsonFilePath = r'data.json'
    csv_to_json(csvFilePath, jsonFilePath)

    def dataProcessing():
        with open("data.json") as f:
            data = json.load(f)
        index_labels = ['Sender', 'Subject', 'Date', 'Snippet', 'Subject']
        df = pd.DataFrame.from_records(data, index=index_labels)
        dataf = pd.json_normalize(data)
        messageBodyList = []
        reminderDate = []
        reminderTitle = []
        reminderTime = []
        for i in range(0, len(dataf)):
            messageBodyList.append(dataf.iloc[i][3])
        # print(messageBodyList[0])

        for i in range(0, len(dataf)):
            matches = list(datefinder.find_dates(messageBodyList[i]))
            # print(i)

            if len(matches) == 1:
                # date returned will be a datetime.datetime object, here we are only using the first match.
                date = matches[0].strftime("%d-%m-%Y")
                # date = matches[0].date()
                time = matches[0].strftime("%H:%M:%S")
                # time = matches[0].time()
                reminderTitle.append(dataf.iloc[i][1])
                # print("date: ", date)
                # print("time: ", time)
                reminderTime.append(time)
                reminderDate.append(date)
            else:
                pass

        # for i in range(0, len(reminderDate)):
        #     print(reminderTitle[i])
        #     print(reminderDate[i])
        #     print(reminderTime[i])
        # print(type(reminderDate[0]))
        # print(type(reminderTime[0]))
        # print(type(reminderTitle[0]))
        return reminderTitle, reminderDate, reminderTime
        # print(len(reminderTitle))
        # print(len(reminderDate))
        # print(len(reminderTime))


    # dataProcessing()

    reminderTitle, reminderDate, reminderTime = dataProcessing()
    return reminderTitle, reminderDate, reminderTime





events = []



@app.route('/calendar')
def calendar():
    return render_template("calendar.html", events = events)

@app.route('/add', methods=['GET', 'POST'])
def add_to_cal():
    global events
    if request.method == "POST":
        print("In new route")
        events= request.get_json()
        #print(events)
    return redirect("calendar.html")
   

if __name__=="__main__":   
    app.run(debug=True,threaded=True)








# from flask import Blueprint, render_template, redirect, url_for, request
# from bson.objectid import ObjectId

# from reminderapp.extensions import mongo

# main=Blueprint('main',_name_)

# @main.route('/')
# def index():
#     reminder_collection=mongo.db.reminder
#     reminders=reminder_collection.find()
#     return render_template('index.html', reminders=reminders)

# @main.route('/edit_reminder_form/<oid>', methods=['POST'])
# def edit_reminder_form(oid):
#     reminder_collection=mongo.db.reminder
#     reminder_item=reminder_collection.find_one({'_id':ObjectId(oid)})
#     reminder_title=request.form.get('reminder-title')
#     reminder_date=request.form.get('reminder-date')
#     reminder_time=request.form.get('reminder-time')
#     reminder_info=request.form.get('reminder-info')
#     reminder_frequency=request.form.get('reminder-frequency')
#     newvalues = { "$set": { 'title': reminder_title , 'date': reminder_date, 'time': reminder_time, 'info': reminder_info, 'frequency': reminder_frequency} }
#     reminder_collection.update_one(reminder_item, newvalues)
#     return redirect(url_for('main.index'))

# @main.route('/add_reminder', methods=['POST'])
# def add_reminder():
#     reminder_collection=mongo.db.reminder
#     reminder_title=request.form.get('reminder-title')
#     reminder_date=request.form.get('reminder-date')
#     reminder_time=request.form.get('reminder-time')
#     reminder_info=request.form.get('reminder-info')
#     reminder_frequency=request.form.get('reminder-frequency')
#     reminder_collection.insert_one({'title':reminder_title, 'date':reminder_date, 'time':reminder_time, 'info': reminder_info, 'frequency':reminder_frequency, 'complete':False})
#     return redirect(url_for('main.index'))

# @main.route('/complete_reminder/<oid>')
# def complete_reminder(oid):
#     reminder_collection=mongo.db.reminder
#     reminder_item=reminder_collection.find_one({'_id':ObjectId(oid)})
#     newvalues = { "$set": { 'complete': True } }
#     reminder_collection.update_one(reminder_item, newvalues)
#     return redirect(url_for('main.index'))

# @main.route('/delete_reminder/<oid>')
# def delete_reminder(oid):
#     reminder_collection=mongo.db.reminder
#     reminder_collection.delete_one({'_id':ObjectId(oid)})
#     return redirect(url_for('main.index'))

# @main.route('/edit_reminder/<oid>')
# def edit_reminder(oid):
#     reminder_collection=mongo.db.reminder
#     reminder_item=reminder_collection.find_one({'_id':ObjectId(oid)})
#     return render_template('editForm.html', reminder=reminder_item)