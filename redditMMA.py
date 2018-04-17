import praw, pprint,operator, sys
#Code in order to take care of unrecognized character error such as emojis
#UnicodeEncodeError: 'UCS-2' 
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

def sortedString(sortedList):
    returnString = ''
    for tuple in sortedList:
        if(tuple[1] >= 3):
            #Making the translation in order to prevent unicodeEncodeError
            returnString += (str(tuple[0]).translate(non_bmp_map) + ': ' + str(tuple[1]).translate(non_bmp_map)+ '\n')
    return returnString

#=============================MAIN===========================

#Initializing the reddit object
reddit = praw.Reddit(client_id = 'F_gwC51M8pKYkQ',
                     client_secret = 'SNgPPPVz8uWKABOcGH5tNjreGyQ',
                     user_agent = '<pc>:<F_gwC51M8pKYkQ>:<V1.0> (by /u/<montyredditpython>)')
mma = reddit.subreddit('MMA')
words = {}
commonWords = open('commonWords.txt','r')
wordDictionary = commonWords.readlines()

#reddit.subreddit takes a subreddit argument and returns 
numPosts = 200
for posts in mma.hot(limit=numPosts):
    #print(type(posts))
    parser = str(posts.title).split()
    for word in parser:
        if(word.isalnum() or "'" in word):
            words.setdefault(word, 0)
            words[word]+=1

#Converting the dictionary into a list of tuples
#itemgetter function simply grabs the value at the indicated index of the tuple
sortedWords = sorted(words.items(), key=operator.itemgetter(1), reverse = True)
print(sortedString(sortedWords))
