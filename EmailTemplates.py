


def emailTextHTML(receiverName, retainedCompany, companyName, senderName, senderTitle, senderCompany, senderEmail, senderCompanyHomePage, senderPhone, returnHTML=True):
    """
    emailTextHTML function will create and return email text and html to be sent via email

    Args:
        receiverName (str): name of person receiving email
        retainedName (str): company with which you've most recently been retained by - not used in this use example
        companyName (str): name of company associated with receiverName
        senderName (str): name of person sending email
        senderTitle (str): job title of person sending email
        senderCompany (str): name of company associated with sending person
        senderEmail (str): email of sender
        senderCompanyHomePage (str): company homepage of sender
        senderPhone (str): phone associated with sender
        returnHTML (bool): if True, then emailTextHTML returns an HTML message in addition to a plain text message

    Returns:
        [text, html] [str, html str]: 2-item list containing text version of email message and html version of email message
    """
    text = f'''
Hi {receiverName} -
Say some stuff about the company you're reaching out to here -  {companyName} - . Then say some other stuff.

    Best,
    {senderName}

    {senderName}
    {senderTitle} - {senderCompany}
    {senderPhone}
    {senderEmail}
    {senderCompanyHomePage}
    '''

    html = f'''
    <html>
    <body>
    <p>
    Hi {receiverName} - <br>
    Say some stuff about the company you're reaching out to here -  {companyName} - . Then say some other stuff.<br>

    <br>
    Best,<br>
    {senderName}<br>
    <br>
    {senderName}<br>
    {senderTitle} - {senderCompany}<br>
    {senderPhone}<br>
    {senderEmail}<br>
    {senderCompanyHomePage}
    </p>
    </body>
    </html>
    '''
    if returnHTML:
        return [text, html]
    else:
        return [text]
