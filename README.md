# cb_emailer
This module utilizes targeted company searches on crunchbase pro to compile a CSV of copmanies, which is then used to contact founders within each company by implementing a series of pandas DataFrames, functions, classes, and dictionaries. The final product can be used by either recruiters, sales, or job seekers to contact personnel
within tech companies. A UI needs to be implemented to make the this module client accessible, but the backend
is completely functional, insofar as we're able to compile a CSV on CrunchBase, derive a pandas dataframe from 
that CSV, synthesize emails of founders from that dataframe, and then contact those founders with customized emails.

The main functionality of this module utilizes a EAFP (Easier to Ask for Forgiveness than Permission) style, particularly as it pertains to reading from pickled files. So we use Try Except patterns, Trying to read from a pickled file name, and catching the exception and initializing an object to a default value if that file name does not yet exist.

Regarding why pickling is done on some objects / values instead of storing state in a class instance: This program can run for very long periods, and if for some reason outside of our control, the program is halted, I wanted us to be able to pick up where we left of; hence, I'm pickling values that need to be stored between invocations of sendEmailsFromDataFrame and bounceBackChecker.

Once an entire dataframe is cycled through, with emails being sent to personnel within those companies, a dictionary
is implemented with the main key being location that was associated with that dataframe (hence, crunchbase searches 
should be conducted based on location when utilizing this program). The value for that key is a dictionary whose
entries are individual companies, which have subdictionaries storing employee info. This dictionary is then 
added as a document to a collection in mongoDB (for longterm persistence, mongoDB / PyMongo is utilized).

***
Notes/Documentation on classes and functions:
***
    addCompanyToNoContacts is used to add companies not to be contacted to our persistent list
    You can pass either a string form of a company name, or a list of string form company names to be added
    company names are converted to lower case using .lower() so they can be compared with company names that may have incorrect casing in sendEmailsFromDataFrame

***
    bounceBackChecker checks user inboxes for each email in senderEmailList for bounced emails
    This function is meant to be called after sending emails using sendEmailsFromDataFrame,
    so that we can determine which email addresses returned bounces to us

    The number of messages we check in each sender inbox has formula:

        numMessagesToCheck = sendCount//len(senderEmailList) + sendCount%100

    it approximates how many messages we sent from each account
    it will always overestimate and err on the side of checking too many
    we will check this number of messages at the top of each of our inboxes from senderEmailList

***
    addDomainsToDataFrame will add a 'Domain' column to new dataframe

***
    foundersToListInDataFrame converts founders column to list form, since values in that column are originally strings

***
    emailCombinations will take in a person's name in string form, and will create relevant email
    combinations based on that name. Names can be one name, first and last, or more than two names.
    Based on first / first last / more than three name input, the email combinations that are 
    produced will be different. 

    A list of [personName, companyName, [list of emails]] is then returned. As an example, for 
    personName = 'bill gates', companyName='microsoft', and domainName = 'microsoft.com', we get:

    ['bill gates', 
    'microsoft', [
        'billgates@microsoft.com', 
        'bill.gates@microsoft.com', 
        'bill@microsoft.com', 
        'bgates@microsoft.com', 
        'gates@microsoft.com', 
        'bill_gates@microsoft.com', 
        'gatesbill@microsoft.com', 
        'gatesb@microsoft.com', 
        'gates.bill@microsoft.com', 
        'gates_bill@microsoft.com']]

***
    emailPartitionsMap takes in a list of emails from which we wish to send, and creates a pseudo partition
    from these emails, using integer division by 100
    These partition values are then mapped to our senderEmailList

    So for example, if we had three emails: [em1, em2, em3], then the mapping would be:
    (33, em1), (66, em2), (99, em3)

    The purpose of this function is to be able to rotate through sender email addresses after a 
    certain number of sends, in this case the size of each partition is 33, so that is the length after
    which we will rotate emails (the rotation happens in further functions)

***
    emailFromPartition takes a mapping created by findPartitions, and based on sendCount, determines 
    which email should be used

***
    sendEmails will send an email to all emails associated with a person
    It returns a dictionary of form {employeeName, companyName, email:(list of all emails)} 

***
    emailJobs is a function that is used to email jobs/careers email addresses for companies in a dataframe

***
    outLookSender is not utilized in this module - but wrote the function in case we want to send from an outlook account in the future

***
    emailTextHTML function will create and return email text and html to be sent via email

***
    AttributeRepr is a class whose purpose is to make __repr__ pretty for subclasses that inherit from it.
    It accesses self.__dict__.itms() to return pairs of attName:attValue

***
    Employee class models an employee in a company. This class is mainly utilized in this module
    as it pertains to Founders values in our main dataframe

***
    Company class instances represent one row from a Pandas Dataframe,
    which also means that we will convert them to dicts to represent on document in a mongoDB collection

    Not providing @property, getter, setter methods for attributes becaue 
    we will not be modifying attributes within instances of this class

***
    dictFromEmployee will take in an Employee class instance as an argument, and return a dict representation of that employee
    The goal here is to introduce a dict representation to make our objects compatible with mongoDB 

***
    dictFromCompanyClass takes in an instance of Class Company and converts it to a dict
    Main goal is to allow for insertion of a company dict as a document in mongoDB collection

***
    companyDictFromDF takes in an entire dataframe, and creates a dictionary whose keys
    are the company names in that dataframe, and values are an instance of diftFromCompany (a single company dictionary)

***
    sendEmailsFromDataFrame will call sendEmails and emailJobs for each company in a dataframe

***
    runMain combines the rest of the functionality in these modules to implement the actual program