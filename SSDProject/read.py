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
from csvtojson import *
from processing import *

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

    '''
    The final_list will have dictionary in the following format:
    {	'Sender': '"email.com" <name@email.com>', 
        'Subject': 'Lorem ipsum dolor sit ametLorem ipsum dolor sit amet', 
        'Date': 'yyyy-mm-dd', 
        'Snippet': 'Lorem ipsum dolor sit amet'
        'Message_body': 'Lorem ipsum dolor sit amet'}
    The dictionary can be exported as a .csv or into a databse
    '''

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
    reminderTitle, reminderDate, reminderTime=dataProcessing()
    return reminderTitle, reminderDate, reminderTime

