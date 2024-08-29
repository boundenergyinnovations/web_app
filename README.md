# bei - web_app  

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Contributing](#contributing)

## Introduction
bei Founder/Lead Dev here,

Very long story short, I grew up seeing people taken advantage of in the late 90s early 00s with the SEO craze and other stuff when I first got into computers and saw that I could code things people were charging hundreds or thousands for. I was too young and too dumb to be able to do anything about it then. Well.. I'm not too young and hopefully not too dumb to do something about it now. I am seeing people/companies charging, and I am not exaggerating, over 1800% markup on services. Many sites and services are taking advantage of the AI hype and people.  I am building and releasing open source web apps, custom servers, scripts, chatbots, business software, etc. for people and small businesses to use. For small local businesses that maybe get a few users at a time, this will work just fine. People can: chat with your company info, easy builtin messaging, dynamic loading of videos/media. Easily customizable and easy to add functionality in code with Python. Basic rate limited is implemented (to protect against abuse of the chatbot). The idea is you have a bit of static info/text/an introduction at the top, a chat section to answer any questions about the site/person/topic with messaging built in, and a video section because people would rather have information delivered by video *look up the statistics of retention of a video vs a few paragraphs of text, lol. 

## Installation
NEED: AWS account, OpenAI account, api key, assistant id. If using Google Sheets version: gsheet id, gsheet json cred file eg. chatsheet-xxxxxx-xxxxxxx.json,
Start EC2 with Ubuntu and settings for access to public HTTP/HTTPS, will need to set networking.  
download and run setup_webapp_server.sh *n.t.s. get url and post here
```sh
./setup_webapp_server.sh
```

```sh
source /venv/bin/activate
```

```sh
export OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
export OPENAI_ASSISTANT_ID=asst_xxxxxxxx
export SHEET_ID=xxxxxxxxxx *if using the appropriate app version
```

install HTTPS SSL CERT with certbot:
```sh
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

Get the cert *replace example.com with your url:
```sh
sudo certbot --nginx -d example.com
```

Check the cert:
```sh
sudo certbot certificates
```


## Usage
TO TEST:
```sh
python3 web_app_xxx.py
```

TO RUN:
```sh
nohup python3 web_app_xxx.py &
```
*this allows you to close the terminal keep it running

While logged in you can run:
```sh
jobs
```
this will show it currently running, type the number to select, generally '1' then CTRL-C to stop.

Or: 
```sh
ps -aux
````
to show what's running, then:
```sh
kill #
```
where # is the PID. eg. 'kill 66123'


## Contributing
The more the merrier. Any issues, give context. 




