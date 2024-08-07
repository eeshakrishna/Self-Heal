from twilio.rest import Client

def e(user_email, mongo):
    name=get_name(user_email,mongo)
    account_sid = "your sid"
    auth_token = "your token"
    client = Client(account_sid, auth_token)
    twilio_number = "your twilio account number"
    sentence= f"Self Harm detected kindly contact {name} "

    emergency_contact_number=get_emergency_contact_number(user_email, mongo)   



    message_body = sentence
    message = client.messages.create(
        body=message_body,
        from_=twilio_number,
        to='+91'+emergency_contact_number
        )
    print("entry 4")
    print(f"SMS sent to {emergency_contact_number}. SMS SID: {message.sid}")

    return None



def get_emergency_contact_number(user_email, mongo):
    # Assuming 'users' is the collection name in MongoDB where user data is stored
    # Change it according to your actual collection name
    user_data = mongo.db.users.find_one({'email': user_email})
    if user_data:
        return user_data.get('emergency_contact')
    else:
        return 
    

def get_name(user_email, mongo):
    # Assuming 'users' is the collection name in MongoDB where user data is stored
    # Change it according to your actual collection name
    user_data = mongo.db.users.find_one({'email': user_email})
    if user_data:
        return user_data.get('name')
    else:
        return None
