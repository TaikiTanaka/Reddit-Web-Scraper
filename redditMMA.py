import praw, pprint,operator, sys
#Code in order to take care of unrecognized character error such as emojis
#UnicodeEncodeError: 'UCS-2' 
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

#===========================FUNCTION DECLARATIONS============

#returns the string of the sorted list of words
def sortedString(sortedList):
    returnString = ''
    for tuple in sortedList:
        if(tuple[1] >= 3):
            #Making the translation in order to prevent unicodeEncodeError
            returnString += (str(tuple[0]).translate(non_bmp_map) + ': ' + str(tuple[1]).translate(non_bmp_map)+ '\n')
    return returnString

#asks the user for which subreddit to ask
def getSubreddit(reddit):
    userInput = input('Which subreddit would you like to analyze?\n')
    return reddit.subreddit(userInput)

def getNumPosts():
    numPosts = input('How many posts would you like to search?\n')
    if(numPosts.isalpha()):
        if (str(numPosts).lower() == 'max'):
            return 0;
    try:
        val = int(numPosts)
    except ValueError:
        print("Not a valid number")
    return int(numPosts)

def generateCommon():
    commonWords = open('commonWords.txt','r')
    #Generate a list of all of the lines
    wordlist = commonWords.readlines()
    dictionaryList = {}
    for word in wordlist:
        dictionaryList.setdefault(word.strip().upper(),'')
    #print(dictionaryList)
    return dictionaryList

def generateWordMap(numPosts, subreddit):
    count = 0
    
    wordMap = {}

    if(numPosts == 0):
        for posts in subreddit.hot(limit=None):
            count+=1
            parser = str(posts.title).split()
            for word in parser:
                if (word.upper() not in commonWords) and (word.isalpha() or "'" in word):
                    wordMap.setdefault(word, 0)
                    wordMap[word]+=1
    else:
        for posts in subreddit.hot(limit=numPosts):
            count+=1
            parser = str(posts.title).split()
            for word in parser:
                if (word.upper() not in commonWords) and (word.isalpha() or "'" in word):
                    wordMap.setdefault(word, 0)
                    wordMap[word]+=1
    print('\n\n'+ 'Iterated through ' + str(count) +' posts\n\n')
    
    #Converting the dictionary into a LIST of tuples sorted according the frequency of the word
    #itemgetter function simply grabs the value at the indicated index of the tuple
    sortedWords = sorted(wordMap.items(), key=operator.itemgetter(1), reverse = True)
    return sortedWords

    

#=============================MAIN===========================

#Initializing the reddit object
reddit = praw.Reddit(client_id = 'F_gwC51M8pKYkQ',
                     client_secret = 'SNgPPPVz8uWKABOcGH5tNjreGyQ',
                     user_agent = '<pc>:<F_gwC51M8pKYkQ>:<V1.0> (by /u/<montyredditpython>)')

subreddit = getSubreddit(reddit)
numPosts = getNumPosts()
commonWords = generateCommon()
wordMap = generateWordMap(numPosts,subreddit)

print(sortedString(wordMap))
