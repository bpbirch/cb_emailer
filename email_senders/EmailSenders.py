

def sendEmails(
    receiverName,
    retainedCompany,
    companyName,
    emailList,
    senderName,
    senderEmail,
    emailPassword,
    senderTitle,
    senderCompany,
    senderCompanyHomePage,
    senderPhone,
    port=465,
    returnHTML = True    
    ):
    """
    sendEmails will send an email to all emails associated with a person
    It returns a dictionary of form {employeeName, companyName, email:(list of all emails)} 

    Args:
        receiverName (str): name of person receiving email
        retainedCompany (str): company that you most recently were retained by
        companyName (str): name of company associated with receiverName
        emailList ([type]): [description]
        senderName (str): name of person sending email
        senderEmail (str): email of sender
        emailPassword ([type]): [description]
        senderTitle (str): job title of person sending email
        senderCompany (str): name of company associated with sending person
        senderCompanyHomePage (str): company homepage of sender
        senderPhone (str): phone associated with sender
        soughtPosition (str): job position sender is seeking
        gitHubPage (str): github page of sender
        port (int, optional): port to be used for email. Defaults to 465.

    Returns:
        emailDict [dict]: dictionary of form {employeeName, companyName, email:(list of all emails)}
    """

    for emailToTry in emailList: 
        # change back the next line after testing
        time.sleep(np.random.uniform(5,15)) # I introduced this because I was being rate limited, and I want to see if this will help avoid that - it seems to help
        print(f'trying {emailToTry}')
        message = MIMEMultipart('alternative')
        message['Subject'] = f'Engineering Positions at {companyName}' # change this back when ready to send actual emails
        message['From'] = senderEmail
        message['To'] = emailToTry # note that this only affects the headers - it does not affect to whom the message gets sent to

        [text, html] = emailTextHTML(receiverName, retainedCompany, companyName, senderName, senderTitle, senderCompany, senderEmail, senderCompanyHomePage, senderPhone, returnHTML=returnHTML)


        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        message.attach(part1)
        message.attach(part2)

        # create a secure SSL context
        context = ssl.create_default_context()

        # now loop over each email message and extract what we need:
        with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
            # Using with smtplib.SMTP_SSL() as server: makes sure that the connection is automatically closed at the end of the indented code block. If port is zero, or not specified, .SMTP_SSL() will use the standard port for SMTP over SSL (port 465).
            server.login(senderEmail, emailPassword)
            server.sendmail(senderEmail, 'bryanbaarch@gmail.com', message.as_string())
            # the above line is how we actually change whom the message is sent to


def outLookSender(receiverAddress, receiverName, retainedCompany, companyName, senderName, senderTitle, senderCompany, senderEmail, senderCompanyHomePage, senderPhone, returnHTML=False):
    subj = f'Engineers from {retainedCompany} Search'
    if returnHTML:
        [text, html] = emailTextHTML(receiverName, retainedCompany, companyName, senderName, senderTitle, senderCompany, senderEmail, senderCompanyHomePage, senderPhone, returnHTML=returnHTML)
    else:
        [text] = emailTextHTML(receiverName, retainedCompany, companyName, senderName, senderTitle, senderCompany, senderEmail, senderCompanyHomePage, senderPhone, returnHTML=returnHTML)
    outlook = app('Microsoft Outlook')
    msg = outlook.make(
        new=k.outgoing_message,
        with_properties={
            k.subject: subj,
            k.plain_text_content: text
        }
    )

    msg.make(
        new=k.recipient,
        with_properties={
            k.email_address: {
                k.name: receiverName,
                k.address: receiverAddress
            }
        }
    )

    msg.send()


def emailJobs(
    df, 
    retainedCompany, 
    senderName, 
    defaultSenderEmail, 
    emailPassword, 
    senderTitle, 
    senderCompany, 
    senderCompanyHomePage, 
    senderPhone, 
    noContactCompanyListPickleFileName, 
    port=465, 
    returnHTML=True
    ):
        """
        emailJobs is a function that is used to email jobs/careers email addresses for companies in a dataframe

        Args:
            df (Pandas DataFrame): dataframe of companies for which we want to email jobs/careers addresses
            retainedCompany (str): company with which you've been working a recent retention
            senderName (str): preferably of 'first last' format, but can be just 'first'
            defaultSenderEmail (str): email address from which we want to send from
            emailPassword (str): sender email password
            senderTitle (str): sender job title (eg 'Senior Software Engineer')
            senderCompany (str): current company of sender
            senderCompanyHomePage (str): URL for sender's current company
            senderPhone (str): phone number of sender
            noContactCompanyListPickleFileName (str): path name that we want to pickle our no contact company list to
            port (int, optional): port to send from. Defaults to 465.
            returnHTML (bool, optional): if True, an HTML version of message will be sent in addition to plain text version. Defaults to True.

        """
        try:
            with open(noContactCompanyListPickleFileName, 'rb') as inputFile:
                noContactCompanyList = pickle.load(inputFile)   
        except:
            noContactCompanyList = []

        for i in range(len(df)):
            companyName = df['Organization Name'][i]
            if companyName.lower() in noContactCompanyList:
                pass
            try:
                domainName = df['Domain'][i]
                jobsEmails = [prefix + '@' + domainName for prefix in ['jobs', 'careers']]
                # email all the jobs pages for that copmany
                sendEmails(        
                    'guys', # addressing general company, so use 'guys' instead of individual name
                    retainedCompany,
                    companyName,
                    jobsEmails,
                    senderName,
                    defaultSenderEmail,
                    emailPassword,
                    senderTitle,
                    senderCompany,
                    senderCompanyHomePage,
                    senderPhone,
                    port=port,
                    returnHTML = returnHTML     
                    )   
            except:
                pass     