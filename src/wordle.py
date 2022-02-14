import random
from datetime import datetime, timedelta
import db
from words import WORDS, TARGETS

MAX_TIME = 60 * 60 # 1 hour

class Wordle:
    def __init__(self):
        self.games: dict[int, Game] = {}

    def restart(self, uid: int) -> bool:
        old = uid in self.games
        db.add_score(uid, 6, False)
        self.games[uid] = Game()
        return old

    def guess(self, uid: int, word: str) -> str:
        caps = word.lower()
        if caps not in WORDS and caps not in TARGETS:
            return f"{word} is not a valid word"

        if uid not in self.games:
            self.games[uid] = Game()

        start = self.games[uid].get_starttime()
        if (datetime.now() - start).seconds > MAX_TIME:
            self.games[uid] = Game()

        self.games[uid].guess(caps)
        return str(self.games[uid])

    def get_guesses(self, uid: int) -> str:
        if uid in self.games:
            guesses = self.games[uid].get_guesses()
            return "\n".join(guesses)
        else:
            return "Invalid word"

    def check_gameover(self, uid: int):
        if uid in self.games and self.games[uid].is_gameover():
            db.add_score(uid, self.games[uid].num_guesses(), self.games[uid].did_win())
            del self.games[uid]

class Game:
    def __init__(self):
        self.start = datetime.now()
        self.word = random.choice(TARGETS)
        print(self.word)
        self.guesses = []
        self.emoji = []
        self.letters = {}
        self.won = False
        for c in self.word:
            if c not in self.letters:
                self.letters[c] = 1
            else:
                self.letters[c] += 1

    def __str__(self) -> str:
        output = ""
        gameover = self.is_gameover()
        if gameover:
            n = f"{self.num_guesses()}" if self.won else "X"
            output += f"{self.word} {n}/6\n\n"
        for e in self.emoji:
            output += e + '\n'

        if gameover:
            if self.won:
                output += "Well done!"
            else:
                output += "Better luck next time!"
        return output

    def is_gameover(self) -> bool:
        return len(self.guesses) == 6 or self.won

    def did_win(self) -> bool:
        return self.won

    def get_guesses(self) -> list[str]:
        return self.guesses

    def num_guesses(self) -> int:
        return len(self.guesses)

    def get_starttime(self) -> datetime:
        return self.start

    def guess(self, guess: str):
        self.guesses.append(guess)

        if guess == self.word:
            self.emoji.append(":green_square:" * 5)
            self.won = True
            return

        emoji = ""
        for i in range(5):
            e = self.get_emoji(guess, i)
            emoji += e
        self.emoji.append(emoji)

    def get_num_letters(self, c: str):
        if c not in self.letters:
            return 0
        else:
            return self.letters[c]

    def get_emoji(self, word: str, idx: int) -> str:
        letter = word[idx]
        target = self.word[idx]
        n = self.get_num_letters(letter)

        if letter == target:
            return ":green_square:"

        if n == 0:
            return ":black_large_square:"

        indices = [i for i in range(5) if letter == word[i]]
        if len(indices) == n:
            return ":yellow_square:"

        for i in range(n):
            j = indices[i]
            if j == idx:
                return ":yellow_square:"

        return ":black_large_square:"
