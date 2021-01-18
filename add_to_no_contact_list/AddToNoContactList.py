

def addCompanyToNoContacts(newNoContacts, noContactCompanyListPickleFileName='do_not_contact_company_list'):
    """
    addCompanyToNoContacts is used to add companies not to be contacted to our persistent list
    You can pass either a string form of a company name, or a list of string form company names to be added
    company names are converted to lower case using .lower() so they can be compared with company names that may have incorrect casing in sendEmailsFromDataFrame

    Note on the use of isinstance() below:
    Although Alex Martellli and others argue that we should focus on duck typing, or at least goose typing,
    instead of using isinstance, they also recognize that it is often necessary when distinguishing
    between a str and a list object, because both are sequences.
    ie, we can't achieve polymorphism here by just converting to list(newNoContacts),
    because if newNoContacts is a str rather than a tuple, then the behavior this will exhibit
    is definitely not what we want (from 'john', list('john') => ['j','o','h','n'] instead of ['john'])
    
    Args:
        newNoContacts (str or list): company name or list of company names to be added to no contact list. If str, company is appended. If list, company list is extended.
        noContactCompanyListPickleFileName (str): name of file we want to load and write to

    Returns:
        noContactCompanyList [list]: updated list of companies not to be contacted
    """
    try:
        with open(noContactCompanyListPickleFileName, 'rb') as inputFile:
            noContactCompanyList = pickle.load(inputFile)
            if isinstance(newNoContacts, str):
                noContactCompanyList.append(newNoContacts)
            if isinstance(newNoContacts, list):
                noContactCompanyList.extend(newNoContacts)
        with open(noContactCompanyListPickleFileName, 'wb') as outputFile:
            noContactCompanyList = list(set(noContactCompanyList)) # get rid of
            noContactCompanyList = [comp.lower() for comp in noContactCompanyList] # we're converting to lower case for comparison's sake in our sendEmailsFromDataFrame function
            pickle.dump(noContactCompanyList, outputFile)
    except:
        noContactCompanyList = []
        if isinstance(newNoContacts, str):
            noContactCompanyList.append(newNoContacts)
        if isinstance(newNoContacts, list):
            noContactCompanyList.extend(newNoContacts)
        with open(noContactCompanyListPickleFileName, 'wb') as outputFile:
            noContactCompanyList = list(set(noContactCompanyList))
            noContactCompanyList = [comp.lower() for comp in noContactCompanyList]
            pickle.dump(noContactCompanyList, outputFile)
    
    return noContactCompanyList