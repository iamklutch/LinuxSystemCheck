#!/usr/bin/env python3

import re
import csv

errors = dict()
per_user = dict()

#regex filters: find error after ticky: ERROR
find_error = (r' ticky: ERROR ([\w ]*)')
#regex filter: find username between parenthases, include ones with periods in them
find_user = (r' \(([\w]*.?[\w]*)\)')
#regex filter: find type after ticky: in all caps INFO or ERROR
find_action = (r' ticky: ([A-Z]*)')

syslog_file = open('syslog.log', 'r')
file = syslog_file.readlines()
    

def count_errors(file):
    for line in file:
        error_list = re.findall(find_error, line)
        if error_list == None or error_list == []:
            continue
        error = error_list[0].strip()
        #iterate and count the errors
        if error in errors:
            errors[error] += 1
        else:
            errors[error] = 1
    print(errors)
    #sort the dictionary into a tuple by descending value
    sorterror = sorted(errors.items(), key=lambda item:item[1], reverse = True)
    print(sorterror)
    create_error_csv(sorterror)


def count_users(file):
    ''' Finds the user name and also what 
    action is associated with
    their user name then counts the 
    actions as a two item list: info, error'''
    for line in file:
        user = re.findall(find_user, line)
        action = re.findall(find_action, line)
        if user == None or user == []:
            continue
        username = user[0].strip()
        actionname = action[0].strip()

        use_count = per_user.get(username)
        #create a dictionary with a key and a list as the value
        if username in per_user:
            if actionname == 'INFO':
                use_count[0] += 1
            elif actionname == 'ERROR':
                use_count[1] += 1
            per_user[username] = use_count
        else:
            if actionname == 'INFO':
                per_user[username] = [1, 0]
            elif actionname == 'ERROR':
                per_user[username] = [0, 1]
    # need to sort, but it creates a tuple, so you can't use key, value
    sorter = sorted(per_user.items())
    create_user_csv(sorter)

def create_user_csv(rows):
    with open('user_statistics.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Username', 'INFO', 'ERROR'])
        for item in rows:
            print(item[0], item[1])
            # tuple has name and a list of count for info and errors
            name = item[0]
            itemlist = item[1]
            info = itemlist[0]
            err = itemlist[1]
            writer.writerow([name, info, err])
        
def create_error_csv(rows):
    with open('error_message.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Error', 'Count'])
        for item in rows:
            writer.writerow([item[0], item[1]])

count_errors(file)
count_users(file)

syslog_file.close()
