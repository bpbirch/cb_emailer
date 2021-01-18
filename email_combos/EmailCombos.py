

def emailCombinations(personName, companyName, domainName):
    """
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

    Args:
        personName (string): typically will be of form 'first last'
        companyName (string): company name associated with personName
        domainName (string): domain name for emails associated with companyName
        validate (bool): defaults to True. If validate == True, then Real Email api is used to validate email addresses

    Raises:
        ValueError: if nonalphanumeric characters are included in personName

    Returns:
        (list):  A list of [personName, companyName, [list of emails]]
    """
    cleanedName = re.sub('[^0-9a-zA-Z\s]+', '', personName) # strip non alphanumeric, nonwhitespace chars from name
    if len(cleanedName.split()) > 2:
        first = cleanedName.split()[0]
        allThree = "".join(cleanedName.split())
        middleAndRest = ''.join(cleanedName.split()[1:])
        firstInitialMiddleRest = cleanedName.split()[0][0] + middleAndRest 
        emailList = [f'{user}@{domainName}' for user in 
            [first, 
            allThree, 
            middleAndRest, 
            firstInitialMiddleRest]]
        return [cleanedName, companyName, emailList]
    elif len(cleanedName.split()) == 2:
        [f, l] = cleanedName.split()
        firstLast = f + l
        first = f
        firstInitialLast = f[0] + l
        last = l
        firstDotLast = f + '.' + l
        firstUnderscoreLast = f + '_' + l
        lastFirst = l + f
        lastFirstInitial = l + f[0]
        lastDotFirst = l + '.' + f
        lastUnderscoreFirst = l + '_' + f
        emailList = [f'{user}@{domainName}' for user in 
            [firstLast, 
            firstDotLast,
            first, 
            firstInitialLast, 
            last, 
            firstUnderscoreLast, 
            lastFirst, 
            lastFirstInitial, 
            lastDotFirst, 
            lastUnderscoreFirst]]
        return [cleanedName, companyName, emailList]
    elif len(cleanedName.split()) == 1:
        first = f'{cleanedName}@{domainName}'
        emailList = [first]
        return [cleanedName, companyName, emailList]