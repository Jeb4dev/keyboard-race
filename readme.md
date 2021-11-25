# Keyboard race

## Purpose
This project was made as part of the weekly programming challenge hosted by [DevJam].
The project was made for learning purposes. Made by Jeb and mihett05.

[Live Demo](https://keyboard-race.firebaseapp.com/)
![image](https://user-images.githubusercontent.com/76889226/143478303-71de98b9-2af2-4eab-b67d-9161566c1af8.png)
![image](https://user-images.githubusercontent.com/76889226/143478777-e4d8a6ce-afed-4b07-8894-6feb4607920d.png)



## About the Challenge
#### 🛠 Difficulty Level: Intermediate 
📅 Start: November 19th<br>
📅 Deadline: November 25th 16:00 (4PM) GMT

#### 📝 Project Description
Typing practice displays a word which you must then type within a specific interval of time

##### 📑User Stories
- [x] User can click a 'Start Practice' button to start the practice session.
- [x] When a practice session starts, the timer starts increasing
- [x] User is shown a word
- [x] User can type the word in a text input box
- [x] If a user enters an incorrect letter, the text input box is cleared
- [x] If a user enters all letters correctly, then the text input box is cleared and a new word is shown
- [x] User can click "End Practice" button to end the session.
- [x] When the session ends, the typing speed is shown (words per minute)


##### 🌟 Bonus features (optional)
- [x] Text box is not cleared when a wrong letter is typed instead  as the user is writing the word, the correct letters are marked  as green and the incorrect letters are marked as red
- [x] User can see their statistics across multiple session
- [ ] Users can login and see how their score compared with others (leaderboard)
- [x] Users can compete with others


## Tech

#### Frameworks and libraries:

- [Flask] - Micro web framework written in python.
- [Flask-Socketio](https://flask-socketio.readthedocs.io/en/latest/)  Flask-SocketIO gives Flask applications access to low latency bi-directional communications between the clients and the server.
- [Flask-Restful](https://flask-restful.readthedocs.io/en/latest/) - Flask-RESTful is an extension for Flask that adds support for quickly building REST APIs.
- [React](https://reactjs.org/) - A JavaScript library for building user interfaces.
- [Vite](https://vitejs.dev/) - Next Generation Frontend Tooling.
#### Deployment
- [Firebase](https://firebase.google.com/) - Firebase helps you build and run successful apps.
- [Heroku](https://www.heroku.com) - Heroku is a cloud platform as a service supporting several programming languages.

## Installation and running

This app requires [python 3.7+](https://www.python.org/downloads/) to run.

Clone git repo
```sh
git clone https://github.com/JesperKauppinen/keyboard-race.git
```

After cloning or downloading this git repo, install required python libraries

```sh
pip install -r requirements.txt
```

run app.py
```sh
python app.py
```
### Deployment
App is hosted in heroku (backend) and firebase (frontend).


## Development

Want to contribute? Great!
Give feedback, suggest new features, maybe even create pull request.


## Credits
- Google for [rocket](https://emojipedia.org/rocket/) emoji.

## License

MIT

   [Flask]: <https://flask.palletsprojects.com/en/2.0.x/>
   [DevJam]: <https://discord.gg/nZBxGEudY6>
