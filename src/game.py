from __future__ import annotations

import random
import json
from pathlib import Path
from typing import Any

from barebones_rpg import Game, GameConfig, Location, World
from barebones_rpg.items import Inventory, Item, ItemType

from .content import (
    LOCATIONS,
    ITEMS,
    MONSTERS,
    QUESTS,
    SKILL_TREES,
    STARTING_SKILLS,
    SPECIALIZATIONS,
    SPELLS,
    STARTING_LOCATION,
    STARTING_CRISTALS,
    STARTING_ITEMS,
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
        self.quest_progress: dict[str, list[int]] = {}
        self.completed_quests: list[str] = []
        self.accepted_quests: list[str] = []
        self.pending_item_rewards: list[dict[str, Any]] = []
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
            "quest_progress": self.quest_progress,
            "completed_quests": self.completed_quests,
            "accepted_quests": self.accepted_quests,
            "inventory": self.inventory.to_dict(),
            "pending_item_rewards": self.pending_item_rewards,
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
        saved_inventory = data.get("inventory")
        if isinstance(saved_inventory, dict):
            self.inventory = Inventory.from_dict(saved_inventory)
        else:
            self.inventory = Inventory(max_slots=20)
        saved_pending_rewards = data.get("pending_item_rewards", [])
        self.pending_item_rewards = [
            {"id": reward["id"], "quantity": reward.get("quantity", 1)}
            for reward in saved_pending_rewards
            if isinstance(reward, dict)
            and isinstance(reward.get("id"), str)
            and isinstance(reward.get("quantity", 1), int)
            and reward.get("quantity", 1) > 0
            and reward["id"] in ITEMS
        ] if isinstance(saved_pending_rewards, list) else []
        saved_completed = data.get("completed_quests", [])
        if not isinstance(saved_completed, list):
            saved_completed = []
        self.completed_quests = [qid for qid in saved_completed if qid in QUESTS]
        saved_accepted = data.get("accepted_quests")
        if not isinstance(saved_accepted, list):
            # Migrate saves from the previous quest version, where every quest
            # started active as soon as the character was created.
            saved_accepted = (
                list(data.get("quest_progress", {}).keys())
                if isinstance(data.get("quest_progress"), dict)
                else []
            )
        self.accepted_quests = [
            qid
            for qid in saved_accepted
            if qid in QUESTS and qid not in self.completed_quests
        ]
        saved_progress = data.get("quest_progress", {})
        if not isinstance(saved_progress, dict):
            saved_progress = {}
        self.quest_progress = {}
        for quest_id, quest in QUESTS.items():
            if quest_id not in self.accepted_quests:
                continue
            values = saved_progress.get(quest_id, [])
            if not isinstance(values, list):
                values = []
            counts = [
                max(0, int(value)) for value in values[: len(quest["objectives"])]
            ]
            counts.extend([0] * (len(quest["objectives"]) - len(counts)))
            self.quest_progress[quest_id] = counts
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
        self.quest_progress = {}
        self.completed_quests = []
        self.accepted_quests = []
        self.pending_item_rewards = []
        self.inventory = Inventory(max_slots=20)
        for item_reward in STARTING_ITEMS:
            self.grant_item(item_reward["id"], item_reward.get("quantity", 1))
        crystal_pool = STARTING_CRISTALS
        if self.rng.random() < 0.01:
            crystal_pool = ("green_cristal", "chaos_cristal")
        self.grant_item(self.rng.choice(crystal_pool))
        return True

    def grant_item(self, item_id: str, quantity: int = 1) -> bool:
        definition = ITEMS.get(item_id)
        if definition is None or not isinstance(quantity, int) or quantity < 1:
            return False
        item_type = ItemType[definition["item_type"]]
        item = Item(
            name=definition["name"],
            description=definition.get("description", ""),
            item_type=item_type,
            value=definition.get("value", 0),
            weight=definition.get("weight", 1.0),
            stackable=definition.get("stackable", False),
            max_stack=definition.get("max_stack", 1),
            quantity=quantity,
            consumable=definition.get("consumable", False),
            metadata={"content_id": item_id, **definition.get("effect", {})},
        )
        return self.inventory.add_item(item)

    def _grant_reward_items(self, rewards: list[dict[str, Any]]) -> list[str]:
        failures = []
        for reward in rewards:
            item_id = reward.get("id")
            quantity = reward.get("quantity", 1)
            if not isinstance(item_id, str):
                failures.append(str(item_id))
                continue
            if not self.grant_item(item_id, quantity):
                failures.append(item_id)
                self.pending_item_rewards.append({"id": item_id, "quantity": quantity})
        return failures

    def _deliver_pending_item_rewards(self) -> list[str]:
        delivered = []
        remaining = []
        for reward in self.pending_item_rewards:
            if self.grant_item(reward["id"], reward["quantity"]):
                delivered.append(reward["id"])
            else:
                remaining.append(reward)
        self.pending_item_rewards = remaining
        return delivered

    def use_item(self, item_id: str) -> tuple[bool, str]:
        player = self.character
        item = next(
            (
                candidate
                for candidate in self.inventory.items
                if candidate.metadata.get("content_id") == item_id
            ),
            None,
        )
        definition = ITEMS.get(item_id)
        if player is None or item is None or definition is None:
            return False, "You do not have that item."
        if not definition.get("consumable", False):
            return False, "That item cannot be used."

        effects = definition.get("effect", {})
        restored_hp = 0
        restored_mana = 0
        if "hp" in effects:
            missing_hp = max(0, player["max_hp"] - player["hp"])
            restored_hp = min(max(0, effects["hp"]), missing_hp)
        if "mana" in effects:
            missing_mana = max(0, player["max_mana"] - player["mana"])
            restored_mana = min(max(0, effects["mana"]), missing_mana)
        has_permanent_effect = any(
            effects.get(key, 0) > 0
            for key in ("xp", "skill_points", "intelligence", "bonus_damage")
        )
        if restored_hp <= 0 and restored_mana <= 0 and not has_permanent_effect:
            if "hp" in effects and "mana" in effects:
                return False, "Your health and mana are already full."
            return False, "Your health or mana is already full."
        player["hp"] += restored_hp
        player["mana"] += restored_mana
        if "xp" in effects:
            self._award_xp(effects["xp"])
        if "skill_points" in effects:
            player["skill_points"] += effects["skill_points"]
        if "intelligence" in effects:
            player["intelligence"] += effects["intelligence"]
        if "bonus_damage" in effects:
            player["bonus_damage"] += effects["bonus_damage"]
        self.inventory.remove_item(item)
        delivered = self._deliver_pending_item_rewards()
        result = f"Used {item.name}; restored {restored_hp} HP and {restored_mana} mana."
        if delivered:
            result += " Pending reward added: " + ", ".join(delivered) + "."
        return True, result

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
        destination = self.current_location
        location_key = (
            self.location_keys_by_id.get(destination.id) if destination else None
        )
        self._record_quest_event("visit", location_key)
        return True

    def quest_objective_progress(self, quest_id: str, objective_index: int) -> int:
        return self.quest_progress.get(quest_id, [])[objective_index]

    def quest_status(self, quest_id: str) -> str:
        if quest_id in self.completed_quests:
            return "completed"
        if quest_id in self.accepted_quests:
            return "active"
        return "available"

    def accept_quest(self, quest_id: str) -> bool:
        if quest_id not in QUESTS or self.quest_status(quest_id) != "available":
            return False
        self.accepted_quests.append(quest_id)
        self.quest_progress[quest_id] = [0] * len(QUESTS[quest_id]["objectives"])
        return True

    def _record_quest_event(self, event: str, location_key: str | None) -> None:
        newly_completed = []
        pending_events: list[tuple[str, str | None, str | None]] = [
            (event, location_key, None)
        ]
        while pending_events:
            event_name, event_location, task_id = pending_events.pop(0)
            for quest_id, quest in QUESTS.items():
                if (
                    quest_id not in self.accepted_quests
                    or quest_id in self.completed_quests
                ):
                    continue
                progress = self.quest_progress.setdefault(
                    quest_id, [0] * len(quest["objectives"])
                )
                for index, objective in enumerate(quest["objectives"]):
                    if objective["event"] != event_name:
                        continue
                    if event_name == "task" and objective.get("task_id") != task_id:
                        continue
                    if objective.get("location", "any") not in ("any", event_location):
                        continue
                    if progress[index] >= objective["count"]:
                        continue

                    progress[index] += 1
                    if progress[index] == objective["count"] and objective.get("id"):
                        pending_events.append(("task", event_location, objective["id"]))

                if all(
                    progress[i] >= objective["count"]
                    for i, objective in enumerate(quest["objectives"])
                ):
                    self.completed_quests.append(quest_id)
                    self.accepted_quests.remove(quest_id)
                    newly_completed.append((quest_id, quest["reward"]))
                    pending_events.append(("task", event_location, quest_id))

        for _quest_id, reward in newly_completed:
            self._award_xp(reward.get("xp", 0))
            self._grant_reward_items(reward.get("items", []))

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
        enemy = self.enemy
        reward = enemy["xp"]
        player = self.character
        self.enemy = None
        self._award_xp(reward)
        self._grant_enemy_drops(enemy)
        location = self.current_location
        location_key = self.location_keys_by_id.get(location.id) if location else None
        self._record_quest_event("defeat", location_key)
        return reward

    def _grant_enemy_drops(self, enemy: dict[str, Any]) -> list[str]:
        granted = []
        for drop in enemy.get("drops", []):
            if self.rng.random() > drop.get("chance", 1.0):
                continue
            quantity = self.rng.randint(drop.get("min", 1), drop.get("max", 1))
            if self.grant_item(drop["id"], quantity):
                granted.append(drop["id"])
        return granted

    def _award_xp(self, amount: int) -> None:
        player = self.character
        if player is None or player["level"] >= player["max_level"]:
            return
        player["xp"] += amount
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

    def retreat(self) -> None:
        self.enemy = None
