

def emailPartitionsMap(senderEmailList):
    """
    emailPartitionsMap takes in a list of emails from which we wish to send, and creates a pseudo partition
    from these emails, using integer division by 100
    These partition values are then mapped to our senderEmailList

    So for example, if we had three emails: [em1, em2, em3], then the mapping would be:
    (33, em1), (66, em2), (99, em3)

    The purpose of this function is to be able to rotate through sender email addresses after a 
    certain number of sends, in this case the size of each partition is 33, so that is the length after
    which we will rotate emails (the rotation happens in further functions)

    Args:
        senderEmailList (list): list of email addresses

    Returns:
        emailMapping [list]: list of tuples in form: [(33, em1), (66, em2), (99, em3), ...]
    """
    n = len(senderEmailList)
    partitions = [100//n*i for i in range(1, n+1)]  
    emailMapping = list(zip(partitions, senderEmailList))
    return emailMapping


def emailFromPartition(emailpartition, sendCount):
    """ 
    emailFromPartition takes a mapping created by findPartitions, and based on sendCount, determines 
    which email should be used

    Args:
        emailpartition (list): list of tuples returned from emailParititionMap
        sendCount (int): integer that we will use in our emailPartition to determine which
                            email we will send from, based on sendcount

    Returns:
       emailToUse [str]: emailToUse, based on our sendCount and emailPartition
    """
    for partitionEmailPair in emailpartition:
        # we avoid writing if elif logic by just iterating through emailPartition and making this comparison:
        if sendCount%100 <= partitionEmailPair[0]: #partitionEmailPair is a tuple
            emailToUse = partitionEmailPair[1]
            return emailToUse
