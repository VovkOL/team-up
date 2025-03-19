# TeamUp - Sports Training Platform

TeamUp is a web application built with Django that allows athletes to organize and join sports training sessions. 
Users can create profiles, manage friends, and participate in training events based on their location and sport preferences.

## Check it out

[TeamUp project deployed to Render](https://team-up.render.com/)

## Installation 

Python3 must be already installed

'''shell
git clone https://github.com/VovkOL/team-up
cd team-up
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver # start Django Server
'''

## Features
- **Athlete Profiles**: Users can create profiles with their location and view friends.
- **Training Sessions**: Create, update, and delete training sessions (for hosts) with details like sport type, date, location, and max participants.
- **Join/Leave Sessions**: Athletes can join or leave training sessions if there are available slots.
- **Friends System**: Add or remove friends to connect with other athletes.
- **Responsive Design**: Built with Bootstrap for a clean and mobile-friendly UI.

## Tech Stack
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite (default, can be switched to PostgreSQL)
- **Environment Management**: python-decouple for secure configuration
