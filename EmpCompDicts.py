from EmpCompClasses import Company

def dictFromEmployee(emp):
    """
    dictFromEmployee will take in an Employee class instance as an argument, and return a dict representation of that employee
    The goal here is to introduce a dict representation to make our objects compatible with mongoDB 

    Args:
        emp (Class Employee): an instance of Employee class

    Returns:
        empDict [dict]: dict representation of Employee class instance, with all relevant attributes
    """
    empDict = {attName:attVal for attName, attVal in emp.__dict__.items()}
    return empDict


def dictFromCompanyClass(comp):
    """
    dictFromCompanyClass takes in an instance of Class Company and converts it to a dict
    Main goal is to allow for insertion of a company dict as a document in mongoDB collection

    Args:
        comp (Class Company): Instance of Class Company

    Returns:
        compDict [dict]: dict representation of Company Class instance, which can then be inserted as document in mongoDB collection
    """
    compDict = {attName:attVal for attName, attVal in comp.__dict__.items()}
    return compDict


def companyDictFromDF(df):
    """
    companyDictFromDF takes in an entire dataframe, and creates a dictionary whose keys
    are the company names in that dataframe, and values are an instance of diftFromCompany (a single company dictionary)

    Args:
        df (Pandas DataFrame): Pandas Dataframe of companies which we want to convert to a dictionary

    Returns:
        dictOfAllComps [dict]: dictionary whose keys are the company names in that dataframe, and values are an instance of diftFromCompany (a single company dictionary)
    """
    dictOfAllComps = {}
    for i in range(len(df)):
        companyName = df['Organization Name'][i]
        company = Company(*df.loc[i,:])
        '''
        the following line is a major change I just made - look her if experencing issues
        '''
        cDict = dictFromCompanyClass(company) # now we're creating a single dictionary of company
        dictOfAllComps[companyName] = cDict # now we're inserting dictionaries as values inside our larger dictionary
    return dictOfAllComps