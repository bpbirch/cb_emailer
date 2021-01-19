

class AttributeRepr():
    """
    AttributeRepr is a class whose purpose is to make __repr__ pretty for subclasses that inherit from it.
    It accesses self.__dict__.itms() to return pairs of attName:attValue

    """
    def __repr__(self): 
        self.attStrings = f'<Class {self.__class__.__name__}>\n'
        for attribute, value in self.__dict__.items():
            if attribute != 'attStrings':
                self.attStrings += str({attribute:value}) + '\n'
        return self.attStrings


class Employee(AttributeRepr):
    """
    Employee class models an employee in a company. This class is mainly utilized in this module
    as it pertains to Founders values in our main dataframe

    Inherits __repr__ logic from AttRepr
    """
    def __init__(self, fullName, companyName, emailList):
        self._firstName = fullName.split()[0] 
        if len(fullName.split()) > 1:
            self._lastName = fullName.split()[-1]
        else:
            self._lastName = None 
        self._companyName = companyName 
        self._emailList = emailList
        self._validEmail = None 
    
    @property
    def firstName(self):
        return self._firstName
    @firstName.getter
    def firstname(self):
        return self._firstName
    @firstName.setter 
    def firstName(self, val):
        self._firstName = val 

    @property 
    def lastName(self):
        return self._lastName 
    @lastName.getter 
    def lastName(self):
        return self._lastName
    @lastName.setter
    def lastName(self, val):
        self._lastName = val

    @property
    def companyName(self):
        return self._companyName 
    @companyName.getter 
    def companyName(self):
        return self.companyName 
    @companyName.setter
    def companyName(self, val):
        self._compayName = val 

    @property
    def emailList(self):
        return self._emailList 
    @emailList.getter 
    def emailList(self):
        return self._emailList 
    @emailList.setter 
    def emailList(self, l):
        self._emailList = l
    
    @property 
    def validEmail(self):
        return self._validEmail
    @validEmail.getter 
    def validEmail(self):
        return self._validEmail
    @validEmail.setter 
    def validEmail(self, val):
        self._validEmail = val

  
class Company(AttributeRepr):
    """
    Company class instances represent one row from a Pandas Dataframe,
    which also means that we will convert them to dicts to represent on document in a mongoDB collection

    Not providing @property, getter, setter methods for attributes becaue 
    we will not be modifying attributes within instances of this class
    """
    def __init__(
        self,
        companyName, 
        URL, 
        industries,
        headquartersLocation, 
        description, 
        founders, 
        website,
        contactEmail, 
        fullDescription, 
        lastFundingDate,
        lastFundingType, 
        lastFundingAmount,
        lastFundingAmountCurrency, 
        lastFundingAmountCurrencyInUSD,
        Domain, 
        employeeInfoList):          
            self._companyName = companyName 
            self._url = URL 
            self._industries = industries 
            self._headquartersLocation = headquartersLocation 
            self._description = description 
            self._founders = founders 
            self._website = website 
            self._contactEmail = contactEmail 
            self._fullDescription = fullDescription 
            self._lastFundingDate = lastFundingDate 
            self._lastFundingType = lastFundingType 
            self._lastFundingAmount = lastFundingAmount
            self._lastFundingAmountCurrency = lastFundingAmountCurrency 
            self._lastFundingAmountCurrencyInUSD = lastFundingAmountCurrencyInUSD
            self._domain = Domain
            self._employeeInfoList = employeeInfoList