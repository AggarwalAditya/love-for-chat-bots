import requests
import json
import time
import nltk
import pyowm


owm = pyowm.OWM('f4dc60af14fc8f8ce18f2bfa0ba853e8')

TOKEN='345918107:AAE6pzYzqBsdsLHq5ryOe3FZBhuOYkDwZBU'
URL= "https://api.telegram.org/bot{}/".format(TOKEN)



def get_url(url):
    response=requests.get(url)
    content=response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content=get_url(url)
    js=json.loads(content)
    return js

def get_updates():
    url=URL+"getUpdates"
    js=get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates=len(updates['result'])
    last_update=num_updates-1
    text=updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text,chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

# text, chat = get_last_chat_id_and_text(get_updates())
# print(send_message(text, chat))


def generate_weather(text):
    words = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(words)
    namedEnt = nltk.ne_chunk(tagged, binary=False)
    var = ""
    for i in namedEnt:
        if "GPE" in str(i):
            var = str((str(i)[5:].split('/')[0]))
            print("weather nikal rha hu")
            observation = owm.weather_at_place(var)
            w = observation.get_weather()
            answer= "Hey Bro ! The weather is of "+var+" is: \n"+str(w.get_temperature('celsius'))+"\n"+str(w.get_wind())+"\n"+str(w.get_humidity() )
        else:
            print("kuch nahi hua")
            answer="hello"
    return answer


def main():
    last_textchat = (None, None)
    while True:
        text, chat = get_last_chat_id_and_text(get_updates())
        if (text, chat) != last_textchat:
            answer=generate_weather(text)
            #print(answer)
            send_message(answer, chat)
            print()
            last_textchat = (text, chat)
        time.sleep(0.5)

if __name__=='__main__':
    main()