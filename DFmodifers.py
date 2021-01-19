from numpy.core.numeric import NaN
import numpy as np 
from urllib.parse import urlparse
from EmailCombos import emailCombinations 
from EmpCompDicts import dictFromEmployee
from EmpCompClasses import Employee

def addDomainsToDataFrame(df):
    """
    addDomainsToDataFrame will add a 'Domain' column to new dataframe

    Args:
        df (pd.DataFrame): we will copy this DataFrame and return an augmented version with Domain column

    Returns:
        copyDF (pd.DataFrame): copy of df with Domain column added
    """
    urls = list(df['Website'].copy())
    copyDF = df.copy()
    domains = []
    for url in urls:
        try:
            fullDomain = urlparse(url).netloc 
            if 'www' in fullDomain:
                fullDomain = '.'.join(fullDomain.split('.')[1:])
            domains.append(fullDomain)
        except:
            domains.append(url)
    copyDF['Domain'] = domains
    return copyDF


def foundersToListInDataFrame(df):
    """
    foundersToListInDataFrame converts founders column to list form, since values in that column are originally strings

    Args:
        df (pd.DataFrame): dataframe we want to modify

    Returns:
        copyDF (pd.DataFrame): copy of df with 'Founders' column data type converted from str to list
    """
    founders = list(df['Founders'].copy())
    newFounders = []
    copyDF = df.copy()
    for founderGroup in founders:
        try:
            founderGroup = founderGroup.split(', ') # founders are comma separated in larger string
            newFounders.append(founderGroup)
        except:
            newFounders.append(founderGroup)
    copyDF['Founders'] = newFounders
    return copyDF


def addEmailsToDataFrame(df):
    """
    addEmailsToDataFrame takes in a dataframe of companies and adds relevant employee emails as a column labeled 'employeeInfoList'

    Args:
        df (Pandas DataFrame): dataframe of companies for which we want to add a column of employeeInfo

    Returns:
        dfCopy [Pandas DataFrame]: copy of DF, with employee dictionaries added as values in 
        'employeeInfoList' column
    """
    dfCopy = df.copy()
    employeeInfoList = []
    for i in range(len(dfCopy)):
        founders = dfCopy['Founders'][i]
        domain = dfCopy['Domain'][i]
        company = dfCopy['Organization Name'][i]
        try:
            emailPersonInfo = [emailCombinations(founder, company, domain) for founder in founders] # create email combinations

            employeeInstances = [Employee(*person) for person in emailPersonInfo] # create employee instances
            empDicts = [dictFromEmployee(emp) for emp in employeeInstances]
            employeeInfoList.append(empDicts) # converting to dict functionality here for mongoDB purposes
        except:
            employeeInfoList.append([np.nan])
    dfCopy['employeeInfoList'] = employeeInfoList
    return dfCopy