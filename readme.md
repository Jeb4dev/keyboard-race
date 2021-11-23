# Keyboard race

## Purpose
This project was made as part of the weekly programming challenge hosted by [DevJam].
The project was made for learning purposes.

## About the Challenge
#### 🛠 Difficulty Level: Intermediate 
📅 Start: November 19th<br>
📅 Deadline: November 25th 16:00 (4PM) GMT

#### 📝 Project Description
Typing practice displays a word which you must then type within a specific interval of time

##### 📑User Stories
- [ ] User can click a 'Start Practice' button to start the practice session.
- [ ] When a practice session starts, the timer starts increasing
- [ ] User is shown a word
- [ ] User can type the word in a text input box
- [ ] If a user enters an incorrect letter, the text input box is cleared
- [ ] If a user enters all letters correctly, then the text input box is cleared and a new word is shown
- [ ] User can click "End Practice" button to end the session.
- [ ] When the session ends, the typing speed is shown (words per minute)


##### 🌟 Bonus features (optional)
- [ ] Text box is not cleared when a wrong letter is typed instead  as the user is writing the word, the correct letters are marked  as green and the incorrect letters are marked as red
- [ ] User can see their statistics across multiple session
- [ ] Users can login and see how their score compared with others (leaderboard)
- [ ] Users can compete with others


## Tech

#### Frameworks and libraries:

- [Flask] - Micro web framework


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


## Development

Want to contribute? Great!
Give feedback, suggest new features, maybe even create pull request.


## Credits


## License

MIT

   [Flask]: <https://flask.palletsprojects.com/en/2.0.x/>
   [DevJam]: <https://discord.gg/nZBxGEudY6>
