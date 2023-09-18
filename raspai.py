import os
import openai
import requests
import wget as wget
from datetime import datetime, timedelta
import calendar
from datetime import date
from bs4 import BeautifulSoup
import os, random
import time
from pygame import mixer




#date,day,time, and weather sent to gpt as variables
now = datetime.now()

current_time = now.strftime("%H:%M")
print(current_time)

# get today's date
d = date.today()

# get day name in english
strday = calendar.day_name[d.weekday()]
print(strday)

# enter city name
city = "YOUR_CITY"

# creating url and requests instance
url = "https://www.google.com/search?q=" + "weather" + city
html = requests.get(url).content

# getting raw data
soup = BeautifulSoup(html, 'html.parser')
temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

tempf = temp.replace('°F', '')

# formatting data
data = str.split('\n')
time = data[0]
sky = data[1]

# getting all div tag
listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
strd = listdiv[5].text

# getting other required data
pos = strd.find('Wind')
other_data = strd[pos:]

# printing all data
print("Temperature is", temp)

print("Sky Description: ", sky)
print(other_data)


#API calls to chatgpt and play.ht for dynamic tts based on above data + music
def gptttsfunction():
    import os, random
    #randomize song
    random_file = random.choice(os.listdir("Z:/Music/Morning"))
    # chatgpt call for custom prompt
    openai.api_key = "OPENAI_API_KEY"

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": "you're a disc jockey on a radio station called ras pie radio and you're playing on an alarm radio that just went off at" + current_time + " on a" + strday + "and the weather forecast is" + sky + temp + "and you're going to play"+random_file+", do not use hyphens and quotations marks, do not start the message with DJ: just be the DJ, do not put quotes around the song name and do not hyphenate any words, and limit it to 400 characters total, and do not say :music plays"}
        ]
    )

    gptmessage = completion.choices[0].message.content

    gptpmessage = gptmessage.strip('/"/n')

    print(gptpmessage)
    # play.ht call for TTS
    url = "https://play.ht/api/v2/tts"

    payload = {
        "quality": "premium",
        "output_format": "wav",
        "speed": 1,
        "sample_rate": 48000,
        "text": gptpmessage,
        "voice": "hunter"
    }
    ttsheaders = {
        "accept": "application/json",
        "content-type": "application/json",
        "AUTHORIZATION": "Bearer_TOKEN",
        "X-USER-ID": "KEY"
    }

    ttsresponse = requests.post(url, json=payload, headers=ttsheaders)

    # print (response.text)

    id1 = ttsresponse.json()['id']

    print(id1)

    # hacky fix to wait for job to be complete before passing job id url to wget

    base = 'https://play.ht/api/v2/tts/'
    base += id1
    id2 = '?format=event-stream'
    base += id2
    print(base)

    url = base

    headers = {
        "accept": "text/event-stream",
        "AUTHORIZATION": "Bearer_TOKEN",
        "X-USER-ID": "KEY"
    }

    getresponse = requests.get(url, headers=headers)

    print(getresponse.text)

    # downloadable link + wget to grab it
    url += id1

    ttsidheaders = {
        "accept": "application/json",
        "AUTHORIZATION": "Bearer_TOKEN",
        "X-USER-ID": "KEY"
    }

    response = requests.get(url, headers=ttsidheaders)

    urlf = response.json()["output"]["url"]

    radiovoice = wget.download(urlf)
    print(radiovoice)

    import os, random
    import time
    from pygame import mixer



    print(random_file)
    print("Z:/Music/Morning/" + random_file)
    mixer.init()
    mixer.music.load(radiovoice)
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(1)
    random_song = "Z:/Music/Morning/" + random_file
    mixer.music.load(random_song)
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(1)

gptttsfunction()
