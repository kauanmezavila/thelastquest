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
        "hp": 110,
        "mana": 150,
        "intelligence": 12,
        "bonus_damage": 2,
        "description": "A scholar who masters the arcane arts.",
    },
    "druid": {
        "name": "Druid",
        "hp": 130,
        "mana": 130,
        "intelligence": 10,
        "bonus_damage": 0,
        "description": "A guardian who draws power from nature.",
    },
}

SPELLS = {
    "fireball": {
        "name": "Fireball",
        "cost": 15,
        "damage": 28,
        "type": "damage",
        "description": "A powerful fire projectile.",
    },
    "firespark": {
        "name": "Fire Spark",
        "cost": 5,
        "damage": 20,
        "type": "damage",
        "description": "A simple fire spark...",
    },
    "frost": {
        "name": "Frost Bolt",
        "cost": 10,
        "damage": 20,
        "type": "damage",
        "description": "An arcane bolt of frost.",
    },
    "heal": {
        "name": "Healing Light",
        "cost": 20,
        "damage": 25,
        "type": "heal",
        "description": "Restores your health.",
    },
}


SKILL_TREES = {
    "pyromancer": {
        "fireball": {
            "name": "Fireball",
            "description": "A powerful fire projectile.",
            "level": 1,
            "spell_id": "fireball",
            "requires": [],
        },
        "frost": {
            "name": "Frost Bolt",
            "description": "An arcane bolt of frost.",
            "level": 2,
            "spell_id": "frost",
            "requires": ["fireball"],
        },
        "firespark": {
            "name": "Fire Spark",
            "description": "A simple fire spark",
            "level": 2,
            "spell_id": "firespark",
            "requires": ["fireball"],
        },
        "heal": {
            "name": "Healing Light",
            "description": "Restores your health",
            "level": 3,
            "spell_id": "heal",
            "requires": ["frost"],
        },
    },
    "arcanist": {
        "frost": {
            "name": "Frost Bolt",
            "description": "Dispara um projétil arcano gélido.",
            "level": 1,
            "spell_id": "frost",
            "requires": [],
        },
        "heal": {
            "name": "Healing Light",
            "description": "Aprende uma cura arcana básica.",
            "level": 2,
            "spell_id": "heal",
            "requires": ["frost"],
        },
        "fireball": {
            "name": "Fireball",
            "description": "Domina uma poderosa magia de fogo.",
            "level": 3,
            "spell_id": "fireball",
            "requires": ["heal"],
        },
    },
    "druid": {
        "heal": {
            "name": "Healing Light",
            "description": "Canaliza energia vital para se curar.",
            "level": 1,
            "spell_id": "heal",
            "requires": [],
        },
        "frost": {
            "name": "Frost Bolt",
            "description": "Concentra a força da natureza em um projétil.",
            "level": 2,
            "spell_id": "frost",
            "requires": ["heal"],
        },
        "fireball": {
            "name": "Fireball",
            "description": "Invoca uma explosão de energia elemental.",
            "level": 3,
            "spell_id": "fireball",
            "requires": ["frost"],
        },
    },
}

MONSTERS = (
    {"name": "Forest Slime", "hp": 55, "damage": 10, "xp": 35},
    {"name": "Shadow Wolf", "hp": 75, "damage": 14, "xp": 50},
    {"name": "Corrupted Treant", "hp": 110, "damage": 18, "xp": 80},
)
