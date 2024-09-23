# bei - web_app  

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Contributing](#contributing)

## Introduction
Many sites and services are taking advantage of the AI hype and people.  We are building and releasing open source web apps, custom servers, scripts, chatbots, business software, etc. for people and small businesses to use. For small local businesses that maybe get a few users at a time, this will work just fine. Users can: chat with your company info, message in the chat interface, dynamically load videos/media. Easily customizable and easy to add functionality in code with Python. Basic rate limited is implemented (to protect against abuse of the chatbot). The idea is you have a bit of static info/text/an introduction at the top, a chat section to answer any questions about the site/person/topic with messaging built in, and a video section because people would rather have information delivered by video *look up the statistics of retention of a video vs a few paragraphs of text, lol.  

Web App Install::  
[![Web App Install](https://img.youtube.com/vi/jS-0qPwYQ3w/0.jpg)](https://www.youtube.com/watch?v=jS-0qPwYQ3w)


App Files, 3 ways to recieve messages:  
web_app_gsheet.py    -- Google Sheets, messages automatically populate in your sheet.  
web_app_localmsg.py  -- Creates a file in the same directory as the app and stores messages with timestamp  
web_app_no_sheet.py  -- Add your own message functionality or leave out

Work in progress: hotel_airtable_app.py   -- It's working, need to set Airtable ids, and table name in system variable or live crazy and set in file. Includes Google Sheets and OpenAI assistant vector database integrations. Set your sheet creds json file and sheet id in app file. The exapmle app checks name and phone number in the database, if there is a match retrieve the reservation. Edit as needed.

We are using the app, if you wish to see a similar demo: https://boundenergyinnovations.com


## Installation
NEED: AWS account, OpenAI account, api key, assistant id. If using Google Sheets version: gsheet id, gsheet json cred file eg. chatsheet-xxxxxx-xxxxxxx.json,

Start EC2/server with Ubuntu and settings for access to public HTTP/HTTPS, will need to set networking/VPC <-- video incomming.  

Create dir:
```sh
mkdir app_dir
cd app_dir
```

Run setup script:
```sh
sh <(curl https://raw.githubusercontent.com/boundenergyinnovations/web_app/main/setup_webapp_server.sh || wget -O - https://raw.githubusercontent.com/boundenergyinnovations/web_app/main/setup_webapp_server.sh)
```

Edit Ngninx config:
```sh
cd /etc/nginx/sites-available/
sudo nano gradio
```
Put your public IP or domain name in the file

Reload Nginx:
```sh
sudo systemctl reload nginx
```

Move back home and go virtual:
```sh
cd ~/app_dir
source venv/bin/activate
```

Install reqs:
```sh
pip install -r requirements.txt
```
Set keys/ids:
```sh
export OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
export OPENAI_ASSISTANT_ID=asst_xxxxxxxx
export SHEET_ID=xxxxxxxxxx *if using the appropriate app version
```

OPTIONAL:
Install HTTPS SSL CERT with certbot:
```sh
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

Get the cert *replace example.com with your url and don't forget to edit the Nginx config in /etc/nginx/sites-available/:
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




