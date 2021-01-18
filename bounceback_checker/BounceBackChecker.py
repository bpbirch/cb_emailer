

def bounceBackChecker(
                    senderEmailList, 
                    emailPassword, 
                    bouncedPickleFileName, 
                    sendCountPickleFileName
                    ):
    """
    bounceBackChecker checks user inboxes for each email in senderEmailList for bounced emails
    This function is meant to be called after sending emails using sendEmailsFromDataFrame,
    so that we can determine which email addresses returned bounces to us

    The number of messages we check in each sender inbox has formula:

        numMessagesToCheck = sendCount//len(senderEmailList) + sendCount%100

    it approximates how many messages we sent from each account
    it will always overestimate and err on the side of checking too many
    we will check this number of messages at the top of each of our inboxes from senderEmailList

    Args:
        senderEmailList (list): list of sender emails that we want to rotate our sending through
        emailPassword (str): sender email password - this password must be the same for all emails in senderEmailList
        bouncedPickleFileName (str): file path name for pickled bounced email list
        sendCountPickleFileName (str): file path name for pickled sendCount

    Returns:
        bouncedList [list]: list of email addresses for which we got a bounce
    """
    # the following two pickle files should be empty in our first iteration, so just initialize to empty lists
    try:
        with open(sendCountPickleFileName, 'rb') as inputFile:
            sendCount = pickle.load(inputFile)
        print('sendcount:', sendCount)
    except:
        print('please specify a valid file name where sendCount is stored. this file should have been updated after calling sendEmailsFromDataFrame')    
        return # exit if no sendCount file was specified
    
    try:
        with open(bouncedPickleFileName, 'rb') as inputFile:
            bouncedList = pickle.load(inputFile)
    except:    
        bouncedList = []
    
    # this is number of messages we'll check in each inbox - it approximates how many messages we sent from each account
    # it will always overestimate and err on the side of checking too many
    # we will check this number of messages at the top of each of our inboxes from senderEmailList
    numMessagesToCheck = sendCount//len(senderEmailList) + sendCount%100 

    for senderEmail in senderEmailList:
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        # now authenticate:
        imap.login(senderEmail, emailPassword) # this actually returns an object: ('OK', [b'person@email.com authenticated (Success)'])
        # if you're using a Gmail account and the above code raises an error indicating 
        # that the credentials are incorrect, make sure you allow less secure apps on your account.
        # if everything has run smoothly till here, then you're logged into your account

        status, messages = imap.select('Inbox') # this selects which mailbox (spam, trash, etc.) we want to check
        nMessagesInInbox = int(messages[0])
        print('number in inbox:', nMessagesInInbox)
        for i in range(nMessagesInInbox, nMessagesInInbox-numMessagesToCheck, -1): # start from the top of our inbox and go through numMessagesToCheck
            try: # using error catching for cases when numMessagesToCheck > nMessagesInInbox
                res, msg = imap.fetch(str(i), '(RFC822)')
                validEmail = True
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        subject, encoding = decode_header(msg['Subject'])[0]
                        # print('subject:', subject)
                        # print('encoding:', encoding)
                        if isinstance(subject, bytes):
                            # if bytes, decode to str:
                            subject = subject.decode(encoding)
                        # now decode email from sender
                        From, encoding = decode_header(msg.get('From'))[0]
                        # print('From:', From.split())
                        # print('from again:', From)
                        # print('encoding:', encoding)
                        if isinstance(From, bytes):
                            From = From.decode(encoding)
                        # print('Subject:', subject) # we can see that we're not even getting to this print
                        # here is where we're actually checking if we got a bounceback
                        print('this is the subject:', subject)
                        failures = ['Delivery Status Notification (Failure)', # may need to dynamically update this list of failures messages
                                    'Delivery Status Notification (Delay)',
                                    'You have reached a dead-end']
                        if any(fail in subject for fail in failures):
                            # note that for this condition, I may need to add additional logic, since maybe not all bouncebacks are in this form
                            # print('THIS WAS A BOUNCEBACK!')
                            if msg.is_multipart():
                                for part in msg.walk():
                                    content_type = part.get_content_type()
                                    # print('content type:', content_type)
                                    content_disposition = str(part.get('Content-Disposition')) # In a regular HTTP response, the Content-Disposition response header is a header indicating if the content is expected to be displayed inline in the browser, that is, as a Web page or as part of a Web page, or as an attachment, that is downloaded and saved locally.
                                    try:
                                        # get email body:
                                        body = part.get_payload(decode=True).decode()
                                        if body != '':
                                            match = re.search(r"[\w\.-]+@[\w\.-]+(?:\.[\w]+)+", body)
                                            if match:
                                                # print(match.group())
                                                bouncedEmail = match.group()
                                                bouncedList.append(bouncedEmail)
                                        # print('message body type:', type(body))
                                        # print('first part of message body:', body[:20])
                                        # print('body length:', len(body))
                                    except:
                                        pass 
            except:
                pass                             
        
        bouncedList = list(set(bouncedList)) # this is what we'll send to sendEmailsFromDataFrame
        # next, pickle the list so we store it persistently
        with open(bouncedPickleFileName, 'wb') as outputFile:
            pickle.dump(bouncedList, outputFile)

    return bouncedList