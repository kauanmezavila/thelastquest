from __future__ import annotations

import random
from typing import Any

from barebones_rpg import Game, GameConfig, Location, World
from barebones_rpg.items import Inventory

from .content import MONSTERS, SPECIALIZATIONS, SPELLS, SKILL_TREES


class GameSession:

    def __init__(self, *, rng: Any = random):
        self.engine = Game(
            GameConfig(title="The Last Quest", save_directory="saves", auto_save=True)
        )
        self.world = self._build_world()
        self.inventory = Inventory(max_slots=20)
        self.character: dict[str, Any] | None = None
        self.enemy: dict[str, Any] | None = None
        self.rng = rng

    @staticmethod
    def _build_world() -> World:
        world = World(name="Eldoria")
        village = Location(
            name="Eldoria Village",
            description="A peaceful village surrounded by ancient hills.",
            width=20,
            height=20,
        )
        forest = Location(
            name="Gray Forest",
            description="An ancient forest filled with mysterious creatures.",
            width=30,
            height=30,
        )
        world.add_location(village)
        world.add_location(forest)
        world.connect_locations(village.id, "north", forest.id, bidirectional=True)
        world.set_current_location(village.id)
        return world

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
            "xp": 0,
            "xp_next": 100,
            "skill_points": 0,
            "skills": [next(iter(SKILL_TREES[specialization]))],
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
        location = self.current_location
        if location is None:
            return None, "There is nowhere to explore."
        if location.name == "Eldoria Village":
            return None, "The village is peaceful. No creatures nearby."
        self.enemy = dict(self.rng.choice(MONSTERS))
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
            message = f"{player['name']} used {spell['name']} and restored {restored} HP."
        else:
            damage = (
                spell["damage"] + player["bonus_damage"] + player["intelligence"] // 5
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
        """Resolve a complete spell turn for callers that do not animate combat."""
        message, finished, reward = self.cast_spell_player(spell_id)
        if finished:
            return message, True, reward
        enemy_message, finished = self.enemy_attack()
        return f"{message}\n{enemy_message}", finished, None

    def _claim_victory(self) -> int:
        assert self.enemy is not None and self.character is not None
        reward = self.enemy["xp"]
        player = self.character
        player["xp"] += reward
        self.enemy = None
        while player["xp"] >= player["xp_next"]:
            player["xp"] -= player["xp_next"]
            player["level"] += 1
            player["skill_points"] += 1
            player["xp_next"] = player["level"] * 100
            player["max_hp"] += 15
            player["max_mana"] += 20
            player["hp"] = player["max_hp"]
            player["mana"] = player["max_mana"]
            player["intelligence"] += 2
        return reward

    def retreat(self) -> None:
        self.enemy = None
