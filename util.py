import eventlet
boto3 = eventlet.import_patched('boto3')

import envs
import os

#import boto3
import json


def validate_username(username):
    if not username[0].isalnum() or not username[-1].isalnum():
        return 0
    for c in username:
        if not c.isalnum():
            if c != '.' and c != '_' and c != '-':
                return 0
    return 1

def validate_password(password):
    for c in password:
        if c == " ":
            return 0
    if len(password) < 6:
        return 0
    if password.isalpha():
        return 0
    if password.isnumeric():
        return 0
    return 1



def validate_email(email):
    pos_AT = 0
    count_AT = 0
    count_DT = 0
    if email[0] == '@' or email[-1] == '@':
        return 0
    if email[0] == '.' or email[-1] == '.':
        return 0
    for c in range(len(email)):
        if email[c] == '@':
            pos_AT = c
            count_AT = count_AT + 1
    if count_AT != 1:
        return 0
        
    username = email[0:pos_AT]
    if not username[0].isalnum() or not username[-1].isalnum():
        return 0
    for d in range(len(email)):
        if email[d] == '.':
            if d == (pos_AT+1):
                return 0
            if d > pos_AT:
                word = email[(pos_AT+1):d]
                #print(word)
                if not word.isalnum():
                    return 0
                pos_AT = d
                count_DT = count_DT + 1
    if count_DT < 1 or count_DT > 2:
        return 0
        
    return 1


def sendLambdaMail(email, code):
    p = {"email": email, "code": code}
    AWS_REGION = "ap-south-1"
    
    try:
        client = boto3.client('lambda', region_name=AWS_REGION)
        response = client.invoke(
            FunctionName="sendemail",
            InvocationType="RequestResponse",
            Payload=json.dumps(p)
        )
    except:
        return False
    
    r = response["Payload"].read().decode()
    if r == "true":
        return True
    else:
        return False
