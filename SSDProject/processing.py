import json
import pandas as pd
import datefinder


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