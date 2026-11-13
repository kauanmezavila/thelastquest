from __future__ import annotations

import random
import json
from pathlib import Path
from typing import Any

from barebones_rpg import Game, GameConfig, Location, World
from barebones_rpg.items import Inventory

from .content import (
    LOCATIONS,
    MONSTERS,
    SKILL_TREES,
    STARTING_SKILLS,
    SPECIALIZATIONS,
    SPELLS,
    STARTING_LOCATION,
)


class GameSession:

    def __init__(self, *, rng: Any = random, save_path: Path | None = None):
        self.engine = Game(
            GameConfig(title="The Last Quest", save_directory="saves", auto_save=True)
        )
        self.save_path = save_path or (
            Path(__file__).resolve().parent.parent / "saves" / "the_last_quest.json"
        )
        self.world = self._build_world()
        self.inventory = Inventory(max_slots=20)
        self.character: dict[str, Any] | None = None
        self.enemy: dict[str, Any] | None = None
        self.rng = rng

    def _build_world(self) -> World:
        world = World(name="Eldoria")
        locations_by_id = {}
        for location_key, details in LOCATIONS.items():
            location = Location(
                name=details["name"],
                description=details["description"],
                width=details["width"],
                height=details["height"],
            )
            locations_by_id[location_key] = location
            world.add_location(location)

        self.locations_by_name = {
            location.name: location for location in locations_by_id.values()
        }
        self.location_keys_by_id = {
            location.id: location_key
            for location_key, location in locations_by_id.items()
        }
        for location_key, details in LOCATIONS.items():
            source = locations_by_id[location_key]
            for direction, destination_key in details.get("connections", {}).items():
                if destination_key not in locations_by_id:
                    raise ValueError(
                        f"Unknown destination '{destination_key}' from '{location_key}'."
                    )
                world.connect_locations(
                    source.id,
                    direction,
                    locations_by_id[destination_key].id,
                    bidirectional=False,
                )

        if STARTING_LOCATION not in locations_by_id:
            raise ValueError(f"Unknown starting location '{STARTING_LOCATION}'.")
        world.set_current_location(locations_by_id[STARTING_LOCATION].id)
        return world

    def save_game(self) -> None:
        location = self.current_location
        data = {
            "character": self.character,
            "location": location.name if location else None,
            "enemy": self.enemy,
        }
        self.save_path.parent.mkdir(parents=True, exist_ok=True)
        self.save_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def load_game(self) -> bool:
        if not self.save_path.exists():
            return False

        data = json.loads(self.save_path.read_text(encoding="utf-8"))
        character = data.get("character")
        location_name = data.get("location")
        if (
            not isinstance(character, dict)
            or character.get("class") not in SPECIALIZATIONS
        ):
            raise ValueError("The save file has invalid character data.")
        if location_name not in self.locations_by_name:
            raise ValueError("The save file has an unknown location.")

        self.character = character
        self.enemy = data.get("enemy")
        self.world.set_current_location(self.locations_by_name[location_name].id)
        return True

    @property
    def current_location(self):
        return self.world.get_current_location()

    def create_character(self, name: str, specialization: str) -> bool:
        name = name.strip()
        stats = SPECIALIZATIONS.get(specialization)
        if not name or stats is None:
            return False
        self.character = {
            "name": name,
            "class": specialization,
            "level": 1,
            "max_level": 10,
            "xp": 0,
            "xp_next": 100,
            "skill_points": 0,
            "skills": STARTING_SKILLS[specialization].copy(),
            "hp": stats["hp"],
            "max_hp": stats["hp"],
            "mana": stats["mana"],
            "max_mana": stats["mana"],
            "intelligence": stats["intelligence"],
            "bonus_damage": stats["bonus_damage"],
        }
        return True

    def learn_skill(self, skill_id: str) -> tuple[bool, str]:
        player = self.character
        if player is None:
            return False, "Create a character first"
        tree = SKILL_TREES.get(player["class"], {})
        skill = tree.get(skill_id)
        if skill is None:
            return False, "This class don't remain to your class"
        if skill_id in player["skills"]:
            return False, "You already learned that skill"
        if player["level"] < skill["level"]:
            return False, f"Avaliable on level {skill['level']}."
        if not all(required in player["skills"] for required in skill["requires"]):
            return False, "Learn the required skills first"
        if player["skill_points"] <= 0:
            return False, "You don't have hability points"
        player["skills"].append(skill_id)
        player["skill_points"] -= 1
        return True, f"Learned skill: {skill['name']}!"

    def available_spells(self) -> dict[str, dict[str, Any]]:
        if self.character is None:
            return {}
        tree = SKILL_TREES.get(self.character["class"], {})
        return {
            node["spell_id"]: SPELLS[node["spell_id"]]
            for skill_id, node in tree.items()
            if skill_id in self.character["skills"] and node.get("spell_id") in SPELLS
        }

    def travel(self, direction: str) -> bool:
        location = self.current_location
        if location is None:
            return False
        destination_id = location.connections.get(direction)
        if destination_id is None:
            return False
        self.world.set_current_location(destination_id)
        return True

    def search(self) -> tuple[dict[str, Any] | None, str | None]:
        if self.character is None:
            return None, "Create a character before exploring."
        location = self.current_location
        if location is None:
            return None, "There is nowhere to explore."
        location_key = self.location_keys_by_id.get(location.id)
        if location_key and not LOCATIONS[location_key].get("encounters", True):
            return None, "This region is peaceful. No creatures nearby."
        player_level = self.character["level"]
        # Keep encounters close to the player's level, allowing a small chance
        # of finding a stronger creature without exposing endgame monsters early.
        suitable_monsters = [
            monster
            for monster in MONSTERS
            if max(1, player_level - 1) <= monster["level"] <= player_level + 1
        ]
        self.enemy = dict(self.rng.choice(suitable_monsters))
        self.enemy["max_hp"] = self.enemy["hp"]
        return self.enemy, None

    def cast_spell_player(self, spell_id: str) -> tuple[str, bool, int | None]:
        player, enemy = self.character, self.enemy
        spell = SPELLS.get(spell_id)
        if player is None or enemy is None or spell is None:
            return "That action is not available.", False, None
        if player["mana"] < spell["cost"]:
            return "Not enough mana!", False, None
        if spell["type"] == "heal" and player["hp"] >= player["max_hp"]:
            return "Your health is already full!", False, None

        player["mana"] -= spell["cost"]
        if spell["type"] == "heal":
            restored = min(spell["damage"], player["max_hp"] - player["hp"])
            player["hp"] += restored
            message = (
                f"{player['name']} used {spell['name']} and restored {restored} HP."
            )
        elif spell["type"] == "mana":
            restored = min(spell["damage"], player["max_mana"] - player["mana"])
            player["mana"] += restored * player["intelligence"] // 10
            message = (
                f"{player['name']} used {spell['name']} and restored {restored} Mana"
            )
        else:
            damage = (
                spell["damage"]
                + player["bonus_damage"]
                + player["intelligence"] // 5 * player["level"] // 10
            )
            enemy["hp"] -= damage
            message = (
                f"{player['name']} attacked {enemy['name']} using {spell['name']} "
                f"and dealt {damage} damage."
            )
            if enemy["hp"] <= 0:
                reward = self._claim_victory()
                message = f"Victory! You earned {reward} XP!"
                return message, True, reward

        return message, False, None

    def enemy_attack(self) -> tuple[str, bool]:
        player, enemy = self.character, self.enemy
        if player is None or enemy is None:
            return "That action is not available.", True
        enemy_damage = self.rng.randint(max(1, enemy["damage"] - 3), enemy["damage"])
        player["hp"] -= enemy_damage
        message = f"{enemy['name']} retaliated and dealt {enemy_damage} damage."
        if player["hp"] <= 0:
            player["hp"] = 1
            self.enemy = None
            return (
                message + " You lost the encounter and retreated safely!",
                True,
            )
        return message, False

    def cast_spell(self, spell_id: str) -> tuple[str, bool, int | None]:
        message, finished, reward = self.cast_spell_player(spell_id)
        if finished:
            return message, True, reward
        enemy_message, finished = self.enemy_attack()
        return f"{message}\n{enemy_message}", finished, None

    def _claim_victory(self) -> int:
        assert self.enemy is not None and self.character is not None
        reward = self.enemy["xp"]
        player = self.character
        if player["level"] < player["max_level"]:
            player["xp"] += reward
        self.enemy = None
        while (
            player["xp"] >= player["xp_next"] and player["level"] < player["max_level"]
        ):
            player["xp"] -= player["xp_next"]
            player["level"] += 1
            player["skill_points"] += 1
            player["xp_next"] = player["level"] * 100
            player["max_hp"] += 15
            player["max_mana"] += 20
            player["hp"] = player["max_hp"]
            player["mana"] = player["max_mana"]
            player["intelligence"] += 2
        if player["level"] >= player["max_level"]:
            player["xp"] = player["xp_next"] = 1
        return reward

    def retreat(self) -> None:
        self.enemy = None
