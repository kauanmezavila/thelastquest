# How i can DEV in The Last Quest?

## Structure

The game uses:

- Barebones: for some logics,
- Textual: for interface,
- Pygame: for sounds,

## Fast-Guide

"I want to create a..."

- [Class](#class)
- [Item](#item)
- [Quest](#quests)

### Class

- Go on `422:SPECIALIZATIONS = {}` and add one like this:

```python
"pyromancer": {
        "name": "Pyromancer",
        "hp": 100,
        "mana": 120,
        "intelligence": 15,
        "bonus_damage": 5,
        "description": "A mage specialized in destructive fire magic.",
},
```

- Now in `457:STARTING_SKILLS = {}` the starting skill:

```python
"pyromancer": ["fireball", "punch"],
```

- The skills in `465:SPELLS = {}`:

```python
"fireball": {
    "name": "Fireball",
    "cost": 15,
    "damage": 28,
    "type": "damage",
    "description": "The oldest solution to every problem",
},
```

- Now, skill tree on `690:SKILL_TREES = {}` like this:

```python
"pyromancer": {
        "fireball": {
            "name": "Fireball",
            "description": "Learn the basics of destructive fire magic.",
            "level": 1,
            "spell_id": "fireball",
            "requires": [],
        },
        "punch": {
            "name": "Punch",
            "description": "The basical humam hability",
            "level": 1,
            "spell_id": "punch",
            "requires": [],
        },
        "meditation": {
            "name": "Meditation",
            "description": "Your mind flows like never!",
            "level": 1,
            "spell_id": "meditation",
            "requires": [],
        },
        "focus": {
            "name": "Focus",
            "description": "Your body flows like the Eldoria rivers!",
            "level": 1,
            "spell_id": "focus",
            "requires": [],
        },
        "inferno": {
            "name": "Inferno",
            "description": "Unlock a more devastating form of fire magic.",
            "level": 2,
            "spell_id": "inferno",
            "requires": ["fireball"],
        },
        "lavahound": {
            "name": "Lava Hound",
            "description": "Master the art of summoning molten creatures.",
            "level": 3,
            "spell_id": "lavahound",
            "requires": ["inferno"],
        },
        "firealign": {
            "name": "Fire Alignment",
            "description": "Recanalizes your mana into a fire variable",
            "level": 3,
            "spell_id": "firealign",
            "requires": ["lavahound"],
        },
        "firetornado": {
            "name": "Fire Tornado",
            "description": "Combine fire and wind into a destructive vortex.",
            "level": 4,
            "spell_id": "firetornado",
            "requires": ["inferno"],
        },
        "phoenix": {
            "name": "Phoenix Rebirth",
            "description": "Harness the legendary regenerative power of the phoenix.",
            "level": 5,
            "spell_id": "phoenix",
            "requires": ["lavahound"],
        },
        "bakuhatsu": {
            "name": "BAKUHATSU",
            "description": "ULTIMATE: EXPLOSION! A crimson-eyed wizard would be proud >:3",
            "level": 6,
            "spell_id": "bakuhatsu",
            "requires": ["firetornado", "lavahound", "phoenix", "firealign"],
        },
    },
```

### Item

- Go on `197:ITEMS = {}` and add like this:

```python
"minor_health_potion": {
        "name": "Minor Health Potion",
        "description": "A small vial that restores your vitality when used.",
        "item_type": "CONSUMABLE",
        "value": 15,
        "weight": 0.2,
        "stackable": True,
        "max_stack": 10,
        "consumable": True,
        "effect": {"hp": 30},
},
```

### Quests

- Add a new location on `395:LOCATIONS = {}` like this:

```python
"eldoria_village": {
        "name": "Eldoria Village",
        "description": "A peaceful village surrounded by ancient hills. No creatures are present here, but the villagers are wary of the dark forces that lurk beyond the hills.",
        "width": 20,
        "height": 20,
        "encounters": False,
        "connections": {"north": "gray_forest", "south": "bastion"},
},
```

- Then add a new quest on `350:QUEST = {}` like this:

```python
"elder_request": {
        "title": "A Message for The Bastion",
        "origin": "eldoria_village",
        "description": "The Elder asks you to carry Eldoria's warning beyond the village.",
        "objectives": [
            {
                "text": "Go talk with Camelot in the Bastion",
                "event": "talk",
                "location": "bastion",
                "count": 1,
            },
        ],
        "reward": {"xp": 205, "items": [{"id": "medium_health_potion", "quantity": 1}]},
},
```

- Now, on `14:DIALOGUES = {}`, make the dialogue that will be made on the location:

```python
"eldoria_village": {
        "speaker": "Elder Maerwen",
        "title": "Keeper of Eldoria",
        "portrait": "(I remenber he since i was 12, what a kind and wise man!)",
        "quest_id": "elder_request",
        "quest_states": {
            "available": {
                "lines": [
                    "{name}, {class_name}, son of Edwin... Is good to see you again.",
                    "The old roads have begun to whisper again",
                    "Im worried that some heretics mages have been opening new hell holes...",
                    "Both Camelot and Resee reported creatures...",
                    "Im worried that those creatures must may doing some problems",
                    "I was already in my way to the florest to help Resee...",
                    "But if our two work on this problem, the fast we can resolve it",
                    "Would you help this old man?",
                ],
                "choices": [
                    {
                        "text": "Yes!",
                        "reply": "Wonderful {name}! Go talk with Camelot in the Bastion! He reported some creatures in the night.",
                        "action": "accept_quest",
                    },
                    {
                        "text": "Well, i haved others plans for today...",
                        "reply": "Hmph, no worries {name}, the wisest path is yours...",
                    },
                ],
            },
            "active": {
                "lines": ["What is you doing here {name}?", "Have you talked to Camelot, {name}?"],
                "choices": [
                    {
                        "text": "I'll keep moving.",
                        "reply": "May the ancestors guide you, little {class_name}...",
                    }
                ],
            },
            "completed": {
                "lines": ["Camelot sent word, {name}... Wonderful."],
                "choices": [
                    {
                        "text": "It was really easy.",
                        "reply": "Then there is still hope for Eldoria. Thank you, mage.",
                    }
                ],
            },
        },
        "lines": [
            "(You hear Elder Maerwen murmuring with itself)",
        ],
        "choices": [
            {
                "text": "Elder?",
                "reply": "Oh! the light may be with you {name}!",
            },
        ],
    },
```
