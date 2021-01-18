from numpy.core.numeric import NaN
import numpy as np
import pandas as pd
import pickle

from EmailSenders import sendEmails
from EmailPartitions import emailPartitionsMap, emailFromPartition

def sendEmailsFromDataFrame(
                            df, 
                            retainedCompany, 
                            senderName, 
                            senderEmailList, 
                            emailPassword, 
                            senderTitle, 
                            senderCompany, 
                            senderCompanyHomePage, 
                            senderPhone, 
                            iterationPickleFileName, 
                            sendCountPickleFileName,
                            validEmailsPickleFileName,
                            bouncedPickleFileName,
                            noContactCompanyListPickleFileName, 
                            noContactPersonListPickleFileName, 
                            port=465, 
                            returnHTML=True
                            ):
    """
    sendEmailsFromDataFrame will call sendEmails and emailJobs for each company in our dataframe

    Args:
        df (Pandas DataFrame): dataframe of companies for which we want to email jobs/careers addresses
        retainedCompany (str): company with which you've been working a recent retention
        senderName (str): preferably of 'first last' format, but can be just 'first'
        senderEmailList (list): list of sender emails that we want to rotate our sending through
        emailPassword (str): sender email password - this password must be the same for all emails in senderEmailList
        senderTitle (str): sender job title (eg 'Senior Software Engineer')
        senderCompany (str): current company of sender
        senderCompanyHomePage (str): URL for sender's current company
        senderPhone (str): phone number of sender
        iterationPickleFileName (str): pickle file path name for pickled iteration count
        sendCountPickleFileName (str): pickle file path name for pickled sendCount
        validEmailsPickleFileName (str): pickle file path name for pickled validEmails
        bouncedPickleFileName (str): pickle file path name for pickled bounced emails
        noContactCompanyListPickleFileName (str): path name for pickled no contact company list
        noContactPersonListPickleFileName (str): file path name for pickled no contact person list
        defaultSenderEmail (str): if defaultSenderEmail is defined, then emails are sent from this email, 
            rather than rotating through list of emails in senderEmailList
        port (int, optional): [description]. Defaults to 465.
        returnHTML (bool, optional): if True, an HTML version of message will be sent in addition to plain text version. Defaults to True.

    Returns:
        sendCount: number of emails sent in call of sendEmailsFromDataFrame
    """

    try:
        with open(noContactCompanyListPickleFileName, 'rb') as inputFile:
            noContactCompanyList = pickle.load(inputFile)   
    except:
        noContactCompanyList = []
    
    try:
        with open(noContactPersonListPickleFileName, 'rb') as inputFile:
            noContactPersonList = pickle.load(inputFile)
    except:
        noContactPersonList = []
        
    try:
        with open(validEmailsPickleFileName, 'rb') as inputFile:
            validEmailsList = pickle.load(inputFile)
    except:
        validEmailsList = []
    
    try:
        with open(iterationPickleFileName, 'rb') as inputFile:
            iterationCount = pickle.load(inputFile)
    except:
        iterationCount = 0

    try:
        with open(bouncedPickleFileName, 'rb') as inputFile:
            bouncedList = pickle.load(inputFile)
    except:
        bouncedList = []

    # removed bounced logic here, because it's handled below
    # the only way we deal with bounedList is after our first iteration, at which time we have a bounceList to pass to our function
    
    # the following helps us create a mapping between a mapping of emails, and a partition of 100
    # we do this because we want to be able to alternate between different send over addresses to avoid being limited
    # so for instance if we had 4 emails, we would want to be able to send: 
    # for sendCount%100<=25: emailA,
    # for sendCount%100<=50: emailB,
    # for sendCount%100<=75: emailC,
    # for sendCount%100<=100: emailD
    emailMap = emailPartitionsMap(senderEmailList)

    sendCount = 0 # this will be the number of emails we check in our inbox for bouncebacks
    for i in range(len(df)):
        # the following line is how we map our sendCount to which email address we should send from
        print('sendCount:', sendCount)
        senderEmail = emailFromPartition(emailMap, sendCount)
        print('senderEmail:', senderEmail)
        companyName = df['Organization Name'][i]
        if companyName.lower() in noContactCompanyList:
            pass
        try:
            if iterationCount == 0:
                # got rid of the following because we used emailJobs() instead
                domainName = df['Domain'][i]
                # adding functionality to automatically email jobs page for iteration == 0
                jobsEmails = [prefix + '@' + domainName for prefix in ['jobs', 'careers']]
                # email all the jobs pages for that copmany
                # got rid of the following because we used emailJobs instead
                sendEmails(        
                    'guys', # addressing general company, so use 'guys' instead of individual name
                    retainedCompany,
                    companyName,
                    jobsEmails,
                    senderName,
                    senderEmail,
                    emailPassword,
                    senderTitle,
                    senderCompany,
                    senderCompanyHomePage,
                    senderPhone,
                    port=port,
                    returnHTML = returnHTML     
                    )        
                sendCount += 2                 

            # enter here, regardless of iterationCount size:     
            employeeInfo = df['employeeInfoList'][i]
            # print('employeeInfo:', employeeInfo)
            for person in employeeInfo:
                # print('person:', person)
                # wait between 5 and 15 seconds
                # reintroduce the next line once finished testing
                # time.sleep(np.random.uniform(5,15)) # we already called time.sleep in sendEmails, so don't need it here
                receiverName = person['_firstName'] # I think I should rewrite this so we're dealing with dictionaries of people, not lists
                companyName = person['_companyName'] # redefining here to ensure companyName matches person's actual company, but this is probably redundant
                if iterationCount == 0: # this is when we're running our first email for each person
                    try:
                        eml = [person['_emailList'][0]] # place inside brackets so email just becomes a one-item list
                        if eml in noContactPersonList: # don't send if person is in no contact
                            pass
                        sendCount += 1
                        sendEmails(        
                            receiverName,
                            retainedCompany,
                            companyName,
                            eml,
                            senderName,
                            senderEmail,
                            emailPassword,
                            senderTitle,
                            senderCompany,
                            senderCompanyHomePage,
                            senderPhone,
                            port=port,
                            returnHTML = returnHTML     
                            )
                    except: # in case there is no person[2][0]
                        pass
                else:
                    prevEmail = person['_emailList'][iterationCount-1]
                    print('previous email:', prevEmail)
                    # the following line needs to be synced with everything else, 
                    # because if bouncedList is empty, we can't really do any testing,
                    # because our program will stop there
                    if prevEmail in bouncedList: 
                        print(f'{prevEmail} was in bounced.')
                        try:
                            eml = [person['_emailList'][iterationCount]] # place inside brackets so eml just becomes a one-item list
                            if eml in noContactPersonList:
                                pass                               
                            sendCount += 1
                            sendEmails(        
                                receiverName,
                                retainedCompany,
                                companyName,
                                eml,
                                senderName,
                                senderEmail,
                                emailPassword,
                                senderTitle,
                                senderCompany,
                                senderCompanyHomePage,
                                senderPhone,
                                port=port,
                                returnHTML = returnHTML     
                                )
                        except Exception as e: # in case there is no person[2][0]
                            print(e) # this is most often going to be 'list index out of range', for when we reach the end of a person's email list                    
                    
                        '''
                        note that the following functionality doesn't work
                        it continues to repeatedly update validEmails for a person because it's looking at email-1 for each run through
                        need to fix this to make it so that adds a PERSON to a peopleValidEmailsFound list
                        '''
                    else:
                        if pd.isnull(person['_validEmail']):
                            print(f'previous email ({prevEmail}) was not found in bouncebacks - adding {prevEmail} to validEmailsList')
                            validEmailsList.append(prevEmail)
                            person['_validEmail'] = prevEmail # add previous email to valid emails list
                            # so the above logic means that if we did not get a bounceback from the previous email,
                            # then make that previous email the valid email in our person / dict in our DF
        except:
            pass
    iterationCount += 1 # increase iteration count by one
    '''
    This should become:
    with open(validEmailsPickleFileName, 'wb') as outputFile:
        pickle.dump(validEmailsList, outputFile)
    '''
    with open(validEmailsPickleFileName, 'wb') as outputFile:
        pickle.dump(validEmailsList, outputFile) # add valid emails to valid email list
    with open(iterationPickleFileName, 'wb') as outputFile:
        pickle.dump(iterationCount, outputFile) # save iterationCount so we remember where we are
    with open(sendCountPickleFileName, 'wb') as outputFile:
        pickle.dump(sendCount, outputFile)
    return sendCount # tell us how many emails were sent, so we know how many emails to check in inbox