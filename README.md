# Wordle Discord Bot

A Discord bot that allows you to play a game of Wordle, as often as you want.

https://github.com/aquova/wordlebot

## Commands

This bot introduces a number of commands:

- `!wordle <GUESS>` to guess a new word. If no game is playing, it will start a new one. If it has been 1 hour since the game was started it will pick a new word and restart.
- `!wordle stats` to show your Wordle statistics.
- `!wordle restart` to start a new game. For stats purposes, this will count as failing to get the correct answer.
