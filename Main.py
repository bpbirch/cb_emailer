#%%
# user defined modules:
from MainLogic import runMain

#%%
if __name__ == '__main__':
    '''
    Fill in values for the following variables to to run

    csvFileName (str): #file path name for CSV file that we will convert to pandas company dataframe
    retainedCompany (str): #company with which you've been working a recent retention
    senderName (str): #preferably of 'first last' format, but can be just 'first'
    senderEmailList (list): #list of sender emails that we want to rotate our sending through
    defaultSenderEmail: #sender email to be used if not sending a list of emails in senderEmailList
    emailPassword (str): #sender email password - this password must be the same for all emails in senderEmailList
    senderTitle (str): #sender job title (eg 'Senior Software Engineer')
    senderCompany (str): #current company of sender
    senderCompanyHomePage (str): #URL for sender's current company
    senderPhone (str): #phone number of sender
    iterationPickleFileName (str): #pickle file path name for pickled iteration count
    sendCountPickleFileName (str): #pickle file path name for pickled sendCount
    validEmailsPickleFileName (str): #pickle file path name for pickled validEmails
    bouncedPickleFileName (str): #pickle file path name for pickled bounced emails
    noContactCompanyListPickleFileName (str): #path name for pickled no contact company list
    noContactPersonListPickleFileName (str): #file path name for pickled no contact person list
    iterations (int): #number of times to cycle through sendEmailsFromDataFrame. defaults to 10, because that's how long most people's email lists are, when geenrated by emailCombinations
    bigCompanyDictPickleFileName (str): #file path name to the dictionary that we use to store all company info persistently
        #(note that this file name likely becomes irrelevant once we convert to mongoDB, since we'll replace this with a database)
    port (int, optional): #port to send from. Defaults to 465
    returnHTML (bool, optional): #if True, emails are sent with HTML attchment in addition to plain text. Defaults to True.
    onlyJobs (bool, optional): #if True, only email jobs/careers emails in df, not individual/founder emails. Defaults to True.
    '''
    runMain(
        csvFileName, 
        retainedCompany, 
        senderName, 
        senderEmailList, 
        defaultSenderEmail,
        emailPassword, 
        senderTitle, 
        senderCompany, 
        senderCompanyHomePage, 
        senderPhone, 
        iterationPickleFileName, 
        sendCountPickleFileName,
        validEmailsPickleFileName,
        bouncedPickleFileName,
        noContactCompanyListPickleFileName,  # we don't need noContactCompanyList - just like other lists, just load from pickle
        noContactPersonListPickleFileName, # don't need
        mongoServerString,
        dbName,
        collectionName,
        port=port,
        returnHTML=returnHTML,
        onlyJobs=onlyJobs
        )

