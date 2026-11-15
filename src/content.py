STARTING_LOCATION = "eldoria_village"


DIALOGUE_UI = {
    "interact_label": "Speak with someone",
    "continue_label": "Continue",
    "return_label": "Return",
    "panel_title": "A CONVERSATION",
    "accent": "#d6ad44",
}

# Placeholders cheat-sheet:
# {name}, {level}, {hp}, {max_hp}, {mana}, {class_name}, {location_name}, {quest_status}, {quest_title}, {quest_progress}, {quest_reward_xp}
DIALOGUES = {
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
    "bastion": {
        "speaker": "Captain Camelot",
        "title": "Commander of The Bastion",
        "portrait": "(The Bastion captain, some Eldorians says that he already killed a dragon!)",
        "quest_id": "bastion_watch",
        "quest_states": {
            "available": {
                "lines": [
                    "A mage, good. Something has been testing the eastern wall after midnight this week.",
                    "(you talk about the creatures)",
                    "I see, well, our night watch almost losed a leg, and is scared of suprises for this night... again",
                    "So, i have been needing to kill those creatures for the last 5 days so the night watch would make his job. And yes, i am really tired...",
                    "Can you help me this night?",
                ],
                "choices": [
                    {
                        "text": "Yes, i can hadle it",
                        "reply": "Great! I will be in my room",
                        "action": "accept_quest",
                    },
                    {
                        "text": "I am a little weak to make this...",
                        "reply": "Oh... i see... well, be careful so...",
                    },
                ],
            },
            "active": {
                "lines": [
                    "The night watch is still waiting for you to clear the creatures nearby."
                ],
                "choices": [
                    {
                        "text": "I'll continue the hunt.",
                        "reply": "Good. Keep your eyes on the eastern wall.",
                    }
                ],
            },
            "completed": {
                "lines": [
                    "The eastern wall is quiet again. The watch owes you a debt."
                ],
                "choices": [
                    {
                        "text": "Glad to help.",
                        "reply": "Eldoria stands stronger with you beside us.",
                    }
                ],
            },
        },
        "lines": ["Hi little {class_name}!"],
        "choices": [
            {
                "text": "Hey!",
                "reply": "Be careful!",
            },
        ],
    },
    "gray_forest": {
        "speaker": "Resee, the Florest Guard",
        "title": "Guard of the Gray Forest",
        "portrait": "(Some Eldorians says that she lives here before Eldoria ever exists)",
        "quest_id": "the_florest_guardian",
        "quest_states": {
            "available": {
                "lines": [
                    "(You saw a woman fighthing some creatures)",
                    "Hey! {class_name}, come here!",
                    "Some creatures get my daugther. Take those while i search her!",
                ],
                "choices": [
                    {
                        "text": "O-ok!",
                        "reply": "You look new around here; do not answer if the woods call your name!",
                        "action": "accept_quest",
                    },
                    {
                        "text": "'(Fake a faint)",
                        "reply": "'Im scared' - (You think and fake a faint, the woman persecute some creatures).",
                    },
                ],
            },
            "active": {
                "lines": [
                    "WHAT YOU IS DOING HERE?? LOOK THE CREATURES BEHIND YOU! - (She shouts)"
                ],
                "choices": [
                    {
                        "text": "OH! SORRY!",
                        "reply": "(She kills a creature while look to you)",
                    }
                ],
            },
            "completed": {
                "lines": [
                    "Thanks {class_name}! My daugther is safe again!",
                    "Here a little reward to you!",
                ],
                "choices": [
                    {
                        "text": "You are welcome!",
                        "reply": "The forest, owes you a debt.",
                    }
                ],
            },
        },
        "lines": ["Hi little {class_name}!"],
        "choices": [
            {
                "text": "Hey!",
                "reply": "Be careful!",
            },
        ],
    },
}

QUEST_UI = {
    "button": "Quests",
    "title": "ACTIVE QUESTS",
    "empty": "No active quests yet. Speak with the locals to take on a quest.",
    "local_title": "TASKS HERE",
    "completed_title": "COMPLETED",
    "reward_format": "Reward: {xp} XP",
}

ITEMS = {
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
    "medium_health_potion": {
        "name": "Medium Health Potion",
        "description": "A medium vial that restores your vitality when used.",
        "item_type": "CONSUMABLE",
        "value": 25,
        "weight": 0.7,
        "stackable": True,
        "max_stack": 5,
        "consumable": True,
        "effect": {"hp": 80},
    },
    "large_health_potion": {
        "name": "Large Health Potion",
        "description": "A large vial that restores your vitality when used.",
        "item_type": "CONSUMABLE",
        "value": 30,
        "weight": 1,
        "stackable": True,
        "max_stack": 3,
        "consumable": True,
        "effect": {"hp": 120},
    },
    "green_cristal": {
        "name": "Green Cristal",
        "description": "A strange green cristal... you feel ancestor vital energy there",
        "item_type": "CONSUMABLE",
        "value": 999,
        "weight": 0.1,
        "stackable": False,
        "consumable": True,
        "effect": {
            "hp": 999,
            "mana": 100,
            "bonus_damage": 5,
        },
    },
    "minor_mana_potion": {
        "name": "Minor Mana Potion",
        "description": "A small vial that restores your mana when used.",
        "item_type": "CONSUMABLE",
        "value": 15,
        "weight": 0.2,
        "stackable": True,
        "max_stack": 10,
        "consumable": True,
        "effect": {"mana": 30},
    },
    "medium_mana_potion": {
        "name": "Medium Mana Potion",
        "description": "A medium vial that restores your mana when used.",
        "item_type": "CONSUMABLE",
        "value": 25,
        "weight": 0.7,
        "stackable": True,
        "max_stack": 5,
        "consumable": True,
        "effect": {"mana": 80},
    },
    "large_mana_potion": {
        "name": "Large Mana Potion",
        "description": "A large vial that restores your mana when used.",
        "item_type": "CONSUMABLE",
        "value": 30,
        "weight": 1,
        "stackable": True,
        "max_stack": 3,
        "consumable": True,
        "effect": {"mana": 120},
    },
    "blue_cristal": {
        "name": "Blue Cristal",
        "description": "A strange blue cristal... there are engraved strange simbols: 'W.W.'",
        "item_type": "CONSUMABLE",
        "value": 999,
        "weight": 0.1,
        "stackable": False,
        "consumable": True,
        "effect": {
            "hp": 100,
            "mana": 999,
            "bonus_damage": 20,
        },
    },
    "yellow_cristal": {
        "name": "Yellow Cristal",
        "description": "A strange yellow cristal... you feel the ancestors experience there...",
        "item_type": "CONSUMABLE",
        "value": 999,
        "weight": 0.1,
        "stackable": False,
        "consumable": True,
        "effect": {
            "xp": 999,
            "hp": 100,
            "mana": 100,
            "intelligence": 10,
        },
    },
    "red_cristal": {
        "name": "Red Cristal",
        "description": "A strange red cristal... you feel... power...",
        "item_type": "CONSUMABLE",
        "value": 999,
        "weight": 0.1,
        "stackable": False,
        "consumable": True,
        "effect": {
            "skill_points": 1,
            "xp": 100,
            "hp": 100,
            "mana": 100,
            "bonus_damage": 2,
        },
    },
    "chaos_cristal": {
        "name": "Chaos Cristal",
        "description": "A strange cristal, you can fell some chaos inside it...",
        "item_type": "CONSUMABLE",
        "value": 999,
        "weight": 0.1,
        "stackable": False,
        "consumable": True,
        "effect": {
            "skill_points": 10,
            "xp": 999,
            "hp": 999,
            "mana": 999,
            "bonus_damage": 10,
            "intelligence": 50,
        },
    },
}

STARTING_ITEMS = [
    {"id": "minor_health_potion", "quantity": 2},
    {"id": "minor_mana_potion", "quantity": 2},
]
STARTING_CRISTALS = ("green_cristal", "blue_cristal", "yellow_cristal", "red_cristal")

# Quest cheat-sheet: "visit", "defeat", or "task".
# PS: location can be id or "any"
QUESTS = {
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
    "bastion_watch": {
        "title": "The Night Watch",
        "origin": "bastion",
        "description": "Camelot is looking for signs of whatever is testing the fortress.",
        "objectives": [
            {
                "text": "Defeat creatures near the Bastion",
                "event": "defeat",
                "location": "bastion",
                "count": 5,
            },
        ],
        "reward": {"xp": 175, "items": [{"id": "minor_health_potion", "quantity": 2}]},
    },
    "the_florest_guardian": {
        "title": "The Florest Guardian",
        "origin": "bastion",
        "description": "Hold the creatures while Resee saves her child!",
        "objectives": [
            {
                "text": "Defeat creatures in the florest",
                "event": "defeat",
                "location": "gray_forest",
                "count": 5,
            },
        ],
        "reward": {"xp": 175, "items": [{"id": "minor_health_potion", "quantity": 1}]},
    },
}

LOCATIONS = {
    "eldoria_village": {
        "name": "Eldoria Village",
        "description": "A peaceful village surrounded by ancient hills. No creatures are present here, but the villagers are wary of the dark forces that lurk beyond the hills.",
        "width": 20,
        "height": 20,
        "encounters": False,
        "connections": {"north": "gray_forest", "south": "bastion"},
    },
    "bastion": {
        "name": "The Bastion",
        "description": "An new fortress built to protect the realm from dark forces. The walls are high and the guards are vigilant, but rumors of a hidden threat persist.",
        "width": 30,
        "height": 30,
        "encounters": True,
        "connections": {"north": "eldoria_village"},
    },
    "gray_forest": {
        "name": "Gray Forest",
        "description": "An ancient forest filled with mysterious creatures. The trees are tall and the canopy is thick, allowing only a few rays of sunlight to reach the forest floor.",
        "width": 50,
        "height": 50,
        "encounters": True,
        "connections": {"south": "eldoria_village"},
    },
}

SPECIALIZATIONS = {
    "pyromancer": {
        "name": "Pyromancer",
        "hp": 100,
        "mana": 120,
        "intelligence": 15,
        "bonus_damage": 5,
        "description": "A mage specialized in destructive fire magic.",
    },
    "arcanist": {
        "name": "Arcanist",
        "hp": 115,
        "mana": 160,
        "intelligence": 12,
        "bonus_damage": 1.5,
        "description": "A scholar who masters the arcane arts.",
    },
    "druid": {
        "name": "Druid",
        "hp": 90,
        "mana": 130,
        "intelligence": 20,
        "bonus_damage": 1,
        "description": "A guardian who draws power from nature.",
    },
    "necromancer": {
        "name": "Necromancer",
        "hp": 100,
        "mana": 140,
        "intelligence": 18,
        "bonus_damage": 2,
        "description": "A guardian who draws power from the undead.",
    },
}

STARTING_SKILLS = {
    "pyromancer": ["fireball", "punch"],
    "arcanist": ["frost", "focus"],
    "druid": ["nature_blessing", "meditation", "focus"],
    "necromancer": ["bone_spear", "punch", "focus"],
}


SPELLS = {
    "punch": {
        "name": "Punch",
        "cost": 0,
        "damage": 10,
        "type": "damage",
        "description": "The most primal form of attack",
    },
    "meditation": {
        "name": "Meditation",
        "cost": 1,
        "damage": 50,
        "type": "heal",
        "description": "Focus is the key",
    },
    "focus": {
        "name": "Focus",
        "cost": 0,
        "damage": 20,
        "type": "mana",
        "description": "Remenber: mana is your body energy flow",
    },
    # PYROMANCER
    "fireball": {
        "name": "Fireball",
        "cost": 15,
        "damage": 28,
        "type": "damage",
        "description": "The oldest solution to every problem",
    },
    "inferno": {
        "name": "Inferno",
        "cost": 25,
        "damage": 48,
        "type": "damage",
        "description": "Initiates a localized apocalypse",
    },
    "lavahound": {
        "name": "Lava Hound",
        "cost": 35,
        "damage": 65,
        "type": "damage",
        "description": "A flying creature made of lava from a far away royal land. Old, Slow, pricey, but works!",
    },
    "firealign": {
        "name": "Fire Alignment",
        "cost": 1,
        "damage": 900,
        "type": "mana",
        "description": "Recanalizes your mana into a fire variable",
    },
    "firetornado": {
        "name": "Fire Tornado",
        "cost": 40,
        "damage": 75,
        "type": "damage",
        "description": "The result of a Fire and Wind Wizards marriage.",
    },
    "bakuhatsu": {
        "name": "爆裂魔法 - BAKUHATSU",
        "cost": 300,
        "damage": 9999,
        "type": "damage",
        "description": "EXPLOSION! A crimson-eyed wizard would be proud >:3",
    },
    "phoenix": {
        "name": "Phoenix Rebirth",
        "cost": 50,
        "damage": 200,
        "type": "heal",
        "description": "Rise from the ashes.",
    },
    # ARCANIST
    "frost": {
        "name": "Frost Bolt",
        "cost": 10,
        "damage": 20,
        "type": "damage",
        "description": "A concentrated projectile of ice.",
    },
    "arcane_missile": {
        "name": "Arcane Missile",
        "cost": 15,
        "damage": 32,
        "type": "damage",
        "description": "Magic missiles that seek out their target.",
    },
    "void_rift": {
        "name": "Void Rift",
        "cost": 35,
        "damage": 65,
        "type": "damage",
        "description": "Opens a tiny hole in reality to another. Please don't look inside.",
    },
    "arcane_rune_engrave": {
        "name": "Arcane Rune Engravement",
        "cost": 5,
        "damage": 400,
        "type": "mana",
        "description": "Engrave mana runes into your skin temporaly, it may canalize mana from other dimension",
    },
    "time_fracture": {
        "name": "Time Fracture",
        "cost": 45,
        "damage": 80,
        "type": "damage",
        "description": "The most painful scars are in the past... and the future.",
    },
    "singularity": {
        "name": "Singularity",
        "cost": 65,
        "damage": 110,
        "type": "damage",
        "description": "Creates your own miniature black hole!",
    },
    "dimensional_heal": {
        "name": "Dimensional Restoration",
        "cost": 35,
        "damage": 200,
        "type": "heal",
        "description": "Suck vital energy from an alternate timeline. That version of you is probably furious.",
    },
    # DRUID
    "nature_blessing": {
        "name": "Nature's Blessing",
        "cost": 15,
        "damage": 200,
        "type": "heal",
        "description": "Mother Nature sends you a care package.",
    },
    "thorn_vine": {
        "name": "Thorn Whip",
        "cost": 15,
        "damage": 30,
        "type": "damage",
        "description": "Some plants are just made to hurt you!",
    },
    "entanglement": {
        "name": "Root Entanglement",
        "cost": 25,
        "damage": 45,
        "type": "damage",
        "description": "'Get over here!'",
    },
    "nature_force": {
        "name": "Nature's Force",
        "cost": 0,
        "damage": 100,
        "type": "mana",
        "description": "Plants love you so much, they even gave to you their natural mana!",
    },
    "storm_call": {
        "name": "Storm Call",
        "cost": 40,
        "damage": 75,
        "type": "damage",
        "description": "'That is the sound of the storm!'",
    },
    "ancient_guardian": {
        "name": "Ancient Guardian",
        "cost": 50,
        "damage": 85,
        "type": "damage",
        "description": "The ever-first three to grow up",
    },
    "world_tree": {
        "name": "World Tree's Embrace",
        "cost": 60,
        "damage": 999,
        "type": "heal",
        "description": "Channels the vitality of the World Tree.",
    },
    # NECROMANCER
    "soul_drain": {
        "name": "Soul Drain",
        "cost": 20,
        "damage": 50,
        "type": "damage",
        "description": "Your enemy's vital energy is now your problem-solving resource.",
    },
    "bone_spear": {
        "name": "Bone Spear",
        "cost": 15,
        "damage": 30,
        "type": "damage",
        "description": "A spear forged from the remains of something that probably deserved better.",
    },
    "spectral_army": {
        "name": "Spectral Army",
        "cost": 35,
        "damage": 65,
        "type": "damage",
        "description": "Summon the unpaid interns of the afterlife.",
    },
    "deaths_souls": {
        "name": "Death's souls",
        "cost": 10,
        "damage": 700,
        "type": "mana",
        "description": "Recently died souls loves mana, make a Honeypot and steal theirs!",
    },
    "curse_of_eternity": {
        "name": "Curse of Eternity",
        "cost": 40,
        "damage": 75,
        "type": "damage",
        "description": "A curse so ancient that even the curse doesn't remember its origin.",
    },
    "lich_regeneration": {
        "name": "Lich Regeneration",
        "cost": 35,
        "damage": 200,
        "type": "heal",
        "description": "Death is merely a minor inconvenience. Probably.",
    },
    "death_king": {
        "name": "The Death King's Decree",
        "cost": 70,
        "damage": 120,
        "type": "damage",
        "description": "Borrow the authority of the underworld.",
    },
}


SKILL_TREES = {
    # PYROMANCER
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
    # ARCANIST
    "arcanist": {
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
        "frost": {
            "name": "Frost Bolt",
            "description": "Learn to manipulate elemental arcane energy.",
            "level": 1,
            "spell_id": "frost",
            "requires": [],
        },
        "arcane_missile": {
            "name": "Arcane Missile",
            "description": "Develop precision-based magical projectiles.",
            "level": 2,
            "spell_id": "arcane_missile",
            "requires": ["frost"],
        },
        "dimensional_heal": {
            "name": "Dimensional Restoration",
            "description": "Study alternate realities to restore your vitality.",
            "level": 3,
            "spell_id": "dimensional_heal",
            "requires": ["arcane_missile"],
        },
        "arcane_rune_engrave": {
            "name": "Arcane Rune Engravement",
            "description": "Engrave mana runes into your skin temporaly, it may canalize mana from other dimension",
            "level": 3,
            "spell_id": "arcane_rune_engrave",
            "requires": ["focus", "meditation"],
        },
        "void_rift": {
            "name": "Void Rift",
            "description": "Manipulate spatial boundaries and open dimensional fractures.",
            "level": 4,
            "spell_id": "void_rift",
            "requires": ["arcane_missile"],
        },
        "time_fracture": {
            "name": "Time Fracture",
            "description": "Learn to manipulate the flow of time.",
            "level": 5,
            "spell_id": "time_fracture",
            "requires": ["dimensional_heal", "void_rift"],
        },
        "singularity": {
            "name": "Singularity",
            "description": "ULTIMATE: Condense arcane energy into a miniature cosmic disaster.",
            "level": 6,
            "spell_id": "singularity",
            "requires": ["void_rift", "time_fracture"],
        },
    },
    # DRUID
    "druid": {
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
        "nature_blessing": {
            "name": "Nature's Blessing",
            "description": "Establish a connection with the natural world.",
            "level": 1,
            "spell_id": "nature_blessing",
            "requires": [],
        },
        "thorn_vine": {
            "name": "Thorn Whip",
            "description": "Turn ordinary vegetation into a defensive weapon.",
            "level": 2,
            "spell_id": "thorn_vine",
            "requires": ["nature_blessing"],
        },
        "entanglement": {
            "name": "Root Entanglement",
            "description": "Command the roots beneath your enemies.",
            "level": 3,
            "spell_id": "entanglement",
            "requires": ["thorn_vine"],
        },
        "nature_force": {
            "name": "Nature's Force",
            "description": "Plants love you so much, they even gave to you their natural mana!",
            "level": 3,
            "spell_id": "nature_force",
            "requires": ["focus", "entanglement", "nature_blessing"],
        },
        "world_tree": {
            "name": "World Tree's Embrace",
            "description": "Access the ancient vitality of the World Tree.",
            "level": 4,
            "spell_id": "world_tree",
            "requires": ["nature_blessing"],
        },
        "storm_call": {
            "name": "Storm Call",
            "description": "Channel the destructive forces of the atmosphere.",
            "level": 5,
            "spell_id": "storm_call",
            "requires": ["entanglement"],
        },
        "ancient_guardian": {
            "name": "Ancient Guardian",
            "description": "ULTIMATE: Awaken an ancient guardian of the forest.",
            "level": 6,
            "spell_id": "ancient_guardian",
            "requires": ["storm_call", "world_tree"],
        },
    },
    # NECROMANCER
    "necromancer": {
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
        "bone_spear": {
            "name": "Bone Spear",
            "description": "Learn the fundamentals of death magic.",
            "level": 1,
            "spell_id": "bone_spear",
            "requires": [],
        },
        "soul_drain": {
            "name": "Soul Drain",
            "description": "Extract vital energy from your enemies.",
            "level": 2,
            "spell_id": "soul_drain",
            "requires": ["bone_spear"],
        },
        "lich_regeneration": {
            "name": "Lich Regeneration",
            "description": "Discover the secret of immortality through undeath.",
            "level": 3,
            "spell_id": "lich_regeneration",
            "requires": ["soul_drain"],
        },
        "deaths_souls": {
            "name": "deaths_souls",
            "description": "Recently died souls loves mana, make a Honeypot and steal theirs!",
            "level": 3,
            "spell_id": "deaths_souls",
            "requires": ["focus", "meditation", "soul_drain", "bone_spear"],
        },
        "spectral_army": {
            "name": "Spectral Army",
            "description": "Command spirits to fight alongside you.",
            "level": 4,
            "spell_id": "spectral_army",
            "requires": ["soul_drain"],
        },
        "curse_of_eternity": {
            "name": "Curse of Eternity",
            "description": "Master ancient curses that transcend mortality.",
            "level": 5,
            "spell_id": "curse_of_eternity",
            "requires": ["lich_regeneration"],
        },
        "death_king": {
            "name": "The Death King's Decree",
            "description": "ULTIMATE: Claim the authority of the underworld.",
            "level": 6,
            "spell_id": "death_king",
            "requires": ["spectral_army", "curse_of_eternity"],
        },
    },
}

MONSTERS = (
    # TIER I — FOREST & MEADOWS
    {
        "id": "forest_slime",
        "name": "Forest Slime",
        "level": 1,
        "hp": 55,
        "damage": 10,
        "xp": 35,
        "drops": [{"id": "minor_mana_potion", "chance": 0.35, "min": 1, "max": 2}],
    },
    {
        "id": "shadow_wolf",
        "name": "Shadow Wolf",
        "level": 2,
        "hp": 75,
        "damage": 14,
        "xp": 50,
        "drops": [{"id": "minor_mana_potion", "chance": 0.25, "min": 1, "max": 1}],
    },
    {
        "id": "corrupted_treant",
        "name": "Corrupted Treant",
        "level": 3,
        "hp": 110,
        "damage": 18,
        "xp": 80,
    },
    # TIER II — CURSED LANDS
    {
        "id": "gravewalker",
        "name": "Gravewalker",
        "level": 4,
        "hp": 130,
        "damage": 22,
        "xp": 100,
    },
    {"id": "rotcap", "name": "Rotcap", "level": 4, "hp": 95, "damage": 26, "xp": 110},
    {
        "id": "void_wraith",
        "name": "Void Wraith",
        "level": 5,
        "hp": 115,
        "damage": 30,
        "xp": 135,
    },
    {
        "id": "runic_golem",
        "name": "Runic Golem",
        "level": 5,
        "hp": 190,
        "damage": 25,
        "xp": 150,
    },
    # TIER III — INFERNAL TERRITORIES
    {
        "id": "hellhound",
        "name": "Hellhound",
        "level": 6,
        "hp": 180,
        "damage": 38,
        "xp": 190,
    },
    {
        "id": "ashen_knight",
        "name": "Ashen Knight",
        "level": 7,
        "hp": 260,
        "damage": 42,
        "xp": 240,
    },
    {
        "id": "magma_colossus",
        "name": "Magma Colossus",
        "level": 8,
        "hp": 340,
        "damage": 48,
        "xp": 300,
    },
    # TIER IV — FORBIDDEN REALM
    {
        "id": "lich_sovereign",
        "name": "Lich Sovereign",
        "level": 9,
        "hp": 420,
        "damage": 55,
        "xp": 450,
    },
    {
        "id": "the_unwritten",
        "name": "The Unwritten",
        "level": 10,
        "hp": 500,
        "damage": 65,
        "xp": 600,
    },
)
