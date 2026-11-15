# The Last Quest: A Tale of Eldoria

## Install it

```bash
git clone https://github.com/kauanmezavila/thelastquest
cd thelastquest
uv pip install --python .venv/bin/python -r requirements.txt
```

or one-line command:

```bash
git clone https://github.com/kauanmezavila/thelastquest && cd thelastquest && uv pip install --python .venv/bin/python -r requirements.txt
```

## Starting it

```bash
python main.py
```

## Audio

The game plays the MP3 tracks in `assets/themes/` as Eldoria's rotating soundtrack,
then chooses another theme when each track finishes. It also includes sound effects for menu actions,
character creation, dialogue, exploration, travel, battles, spells, healing, items,
hits, victories, and retreats. Audio is played with Pygame; systems without an audio
device can still run the game without sound. The generated WAV theme in `assets/audio/`
is used if no MP3 theme is available.

## The Story

You is a son of a lengedary mage called Edwin.

Your adventure starts in a village called Eldoria, you is just living your life when the Elder Maerwen talks about strange creatures around Eldoria mountains.

So Maerwen says to you go to the Bastion help Camelot, the captain of the Bastion.

After finishing your mission, you go explore the Gray Florest where you find a desesperate women trying to save her child of those creatures.

## What is ready

- Fight monsters
- Explore locations
- Unique classes and powers
- XP and skill tree system
- Invetory and itens
- Health and mana
- Missions
- Save progress

## FAQ

### I created my character, what i do now?

Whatever you want! Try talking with someone to get a mission, kill creatures, up your level and more!

### Why i can't find monsters in Eldoria?

Eldoria is a pacific village where the most powerful mages lives. Creatures don't want to pass near it

### I completed the task, where is the reward?

Try talking with the character that gave this task to you

### How many levels it has?

10 levels

### Alright, i reached level 10. What now?

Try other classes!

### I reached level 10 in all classes, full hability, what now?

The game is OpenSource! Try editing **contents.py** to add new itens, classes, habilitys and more!

### I edited the entire game code, what now?

Open a pull request on the main repo! I may probaly accept the new version as a new version of the game

### Btw, while looking in, i found a ultra cool cristal, why isn't in the main game?

I wasn't able to find somewhere to put it in the game :(

### Why don't have more missions?

Because i don't finded a way to make more tasks in the same location.

# Maintener

Maintened by Kauan Mezavila (ByKurebo)

# License

This project uses [MIT License](https://mit-license.org/)
