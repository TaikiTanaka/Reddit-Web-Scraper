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

#=============================MAIN===========================

#Initializing the reddit object
reddit = praw.Reddit(client_id = 'F_gwC51M8pKYkQ',
                     client_secret = 'SNgPPPVz8uWKABOcGH5tNjreGyQ',
                     user_agent = '<pc>:<F_gwC51M8pKYkQ>:<V1.0> (by /u/<montyredditpython>)')

mma = getSubreddit(reddit)
words = {}
commonWords = generateCommon()

#reddit.subreddit takes a subreddit argument and returns 
numPosts = getNumPosts()
for posts in mma.hot(limit=numPosts):
    #print(type(posts))
    parser = str(posts.title).split()
    for word in parser:
        if (word.upper() not in commonWords) and (word.isalpha() or "'" in word):
            words.setdefault(word, 0)
            words[word]+=1

#Converting the dictionary into a list of tuples
#itemgetter function simply grabs the value at the indicated index of the tuple
sortedWords = sorted(words.items(), key=operator.itemgetter(1), reverse = True)
print('\n\n' + sortedString(sortedWords))
