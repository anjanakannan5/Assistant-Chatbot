import re
import long_responses as long
import emoji
import wikipedia
import requests
from bs4 import BeautifulSoup

#check probability that the message is the corresponding message
def message_probability(user_message,  recognised_words,  single_response=False,  required_words=[]):
    message_certainity=0
    has_required_words=True
    
    for word in user_message:
        if word in recognised_words:
            message_certainity+=1
    percentage=float(message_certainity) / float(len(recognised_words))

    #checks if the required words are there in the string
    if len(required_words)!=0:
        for word in required_words:
            if word not in user_message:
                has_required_words=False
                break
    if has_required_words or single_response:
        return int(percentage*100)
    else:
        return 0
#checks for message probability and returns the possible response
def check_all_messages(message):
    highest_prob_list={}
    
    #single response generation according to probability
    def response(bot_response,  list_of_words,  single_response=False,  required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words,  single_response,  required_words)

    #response
    response(f"Thank you ! {emoji.emojize(':folded_hands:')}",["nice","helpful"], single_response=True)
    response(f"Aww, that's really sweet ! {emoji.emojize(':red_heart:')}",["i","love","you"], required_words=["love","you"]) 
    response(f'Hello ! {emoji.emojize(":waving_hand:")}',["hello","hi","hey","hai","sup","hii","vanakkam","namaskaram"], single_response=True)
    response("I'm doing fine, and you ?",["how","are","you","doing"], required_words=["how"])
    response(f"Anytime! Let me know if you need anything else {emoji.emojize(':grinning_face:')}",["thank","thanks"], single_response=True)
    response(f"Okay {emoji.emojize(':thumbs_up:')}",["okie","okay","ok","kay","done"],single_response=True)
    response(long.R_EATING,["what","you","eat"], required_words=["you","eat"])
    response(long.NAME,["what","is","your","name"], required_words=["your","name"])
    response(long.HELP,["can","help","me"], single_response=True,  required_words=["help","me","can"])
    response(long.EXIT,["bye","bubye","bubyee","byeee"], single_response=True,required_words=["bye"]) 
    
    best_match = max(highest_prob_list,  key = highest_prob_list.get )
    if highest_prob_list[best_match]<1:
        return long.unknown()
    else:
        return best_match

#gets response from check message function
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

while True:
    response = get_response(input('You: '))
    if response==long.EXIT:
        print('Bot: ' + response)
        break
    else:
        print('Bot: ' + response)
          
