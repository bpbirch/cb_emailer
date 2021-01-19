from numpy.core.numeric import NaN
import pandas as pd
import numpy as np 
import time 
import pickle
from pymongo import ASCENDING, DESCENDING, MongoClient

from DFmodifers import addDomainsToDataFrame, foundersToListInDataFrame, addEmailsToDataFrame
from EmpCompDicts import companyDictFromDF
from EmailSenders import emailJobs
from BounceBackChecker import bounceBackChecker
from SendEmailsFromDF import sendEmailsFromDataFrame



def runMain(
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
    iterations = 10, # default to 10, since this is the length of most people's email list
    bigCompanyDictPickleFileName = 'Big_Company_Dictionary', # this should not be changed - it is our persistent dictionary storing company info with valid emails
    port=465, 
    returnHTML=True,
    onlyJobs = True
    ):
        """
        runMain combines the rest of the functionality in these modules to implement the actual program

        Args:
            csvFileName (str): file path name for CSV file that we will convert to pandas company dataframe
            retainedCompany (str): company with which you've been working a recent retention
            senderName (str): preferably of 'first last' format, but can be just 'first'
            senderEmailList (list): list of sender emails that we want to rotate our sending through
            defaultSenderEmail: sender email to be used if not sending a list of emails in senderEmailList
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
            iterations (int): number of times to cycle through sendEmailsFromDataFrame. defaults to 10, because that's how long most people's email lists are, when geenrated by emailCombinations
            bigCompanyDictPickleFileName (str): file path name to the dictionary that we use to store all company info persistently
                (note that this file name likely becomes irrelevant once we convert to mongoDB, since we'll replace this with a database)
            port (int, optional): port to send from. Defaults to 465
            returnHTML (bool, optional): if True, emails are sent with HTML attchment in addition to plain text. Defaults to True.
            onlyJobs (bool, optional): if True, only email jobs/careers emails in df, not individual/founder emails. Defaults to True.
        """
        start = time.perf_counter()
        # extract dataframe to work with
        companyDF = pd.read_csv(csvFileName)
        # following two lines are for testing
        # companyDF = companyDF.iloc[12:14,:].copy()
        # companyDF = companyDF.reset_index(drop=True)
        print(companyDF.head())
        # add domains to DF
        companyDF = addDomainsToDataFrame(companyDF)
        # convert founders from string to list of founders for each record
        companyDF = foundersToListInDataFrame(companyDF)
        # add Employee class instances, with emails, to DF
        companyDF = addEmailsToDataFrame(companyDF)
        # DF is now in manageable form

        try:
            with open(bigCompanyDictPickleFileName, 'rb') as inputFile:
                bigCompanyDict = pickle.load(inputFile)
        except:
            bigCompanyDict = {}
        # gather location name as key in bigCompanyDict
        location = companyDF['Headquarters Location'][0] 

        if onlyJobs: # this is if we want to ONLY email the jobs page
            emailJobs(
                companyDF, 
                retainedCompany, 
                senderName, 
                defaultSenderEmail, 
                emailPassword, 
                senderTitle, 
                senderCompany, 
                senderCompanyHomePage, 
                senderPhone, 
                noContactCompanyListPickleFileName, 
                port=port, 
                returnHTML=returnHTML
            )
        else:
            for _ in range(iterations): # iterations is 10: the number of emails created for most people
                sendEmailsFromDataFrame(
                    companyDF, 
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
                    noContactCompanyListPickleFileName, # don't need
                    noContactPersonListPickleFileName, # don't need 
                    port=port, 
                    returnHTML=returnHTML
                )


                # change this line back after testing
                time.sleep(180)# rest three minutes to allow delayed bouncebacks to arrive


                bounceBackChecker(
                    senderEmailList, 
                    emailPassword, 
                    bouncedPickleFileName, 
                    sendCountPickleFileName
                )

            # now that we've run through everything, create a companyDict:
            compDict = companyDictFromDF(companyDF)
            # now initialize an dictionary that we'll use as a document in our collection
            # this is the dictionary that we will upsert into our mongo collection
            currentDict = {'location':location} # so the main key that separates documents in our collection will be location
            # now make that dictionary a value for the key = location in our bigCompanyDict
            currentDict['companies'] = compDict
            # the following is stricly used for pickling persistence
            
            bigCompanyDict[location] = compDict
            # so now, for instance, we have bigCompanyDict['Atlanta, Georgia, United States'] = {'first company': Company class instance, containing employee Class instances in employeeInfoList}
            # now we need to write that dictionary persistently:
            with open(bigCompanyDictPickleFileName, 'wb') as outputFile:
                pickle.dump(bigCompanyDict, outputFile)
            
            # here is where we will be upserting a document for our location to mongoDB
            client = MongoClient(mongoServerString)
            # change the 
            db = client.get_database(dbName)
            comps = db.get_collection(collectionName)
            upsertResult = comps.update_one({'location':location}, {'$set':currentDict}, upsert=True)
            print(f'result from upsert to {collectionName} in {dbName}: {upsertResult.raw_result}')


        
        end = time.perf_counter() 
        duration = end - start 
        if onlyJobs:
            print('finished emailing jobs pages')
        else:
            print(f'time required for {len(companyDF)} companies: {duration} seconds')