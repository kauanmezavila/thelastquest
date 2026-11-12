import asyncio

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Footer, Header, Input, ProgressBar, Select, Static

from .content import SPECIALIZATIONS, SKILL_TREES
from .game import GameSession


class AshenKingdom(App):

    TITLE = "The Last Quest"
    SUB_TITLE = "A Mage's Journey Through Eldoria"

    CSS = """
    Screen {
        background: #101014;
    }

    #main-screen {
        width: 100%;
        height: 1fr;
        border: round #9b80d4;
        padding: 1 2;
    }

    #actions {
        dock: bottom;
        width: 100%;
        height: 4;
        layout: horizontal;
    }

    #actions Button {
        width: 1fr;
        min-width: 10;
        margin: 0 1;
    }

    #interaction-actions {
        dock: bottom;
        width: 100%;
        height: 4;
        layout: horizontal;
        align: center middle;
    }

    #interaction-actions Button {
        width: 1fr;
        min-width: 10;
        margin: 0 1;
    }

    .title {
        color: #c4a7ff;
        text-style: bold;
        text-align: center;
        width: 100%;
        margin-bottom: 2;
    }

    .subtitle {
        color: #aaaaaa;
        margin-bottom: 1;
    }

    .info {
        color: #d6d6e0;
        padding: 1;
    }

    #character-sheet {
        width: 100%;
        height: 1fr;
        align: center middle;
    }

    #character-details {
        width: 2fr;
        height: auto;
    }

    #character-art {
        width: 1fr;
        height: auto;
        color: #c4a7ff;
        text-align: center;
        content-align: center middle;
    }

    Button {
        background: #292437;
        color: white;
        border: round #594875;
    }

    Button:hover {
        background: #594875;
    }

    Input {
        margin-bottom: 1;
    }

    Select {
        margin-bottom: 1;
    }

    #battle-log {
        height: 3;
        min-height: 3;
        border: round #9b80d4;
        padding: 0 1;
        margin: 1 0;
        color: #f1eaff;
        text-style: bold;
    }

    .health-bar {
        width: 100%;
        margin-bottom: 1;
    }

    .health-bar Bar > .bar--bar {
        color: green;
        background: #541414;
    }

    .health-bar Bar > .bar--complete {
        color: lime;
    }

    .health-bar.health-low Bar > .bar--bar {
        color: yellow;
    }

    .health-bar.health-critical Bar > .bar--bar {
        color: red;
    }

    #player-mana-bar Bar > .bar--bar {
        color: cyan;
        background: #17334a;
    }

    .skill-level {
        color: #c4a7ff;
        text-style: bold;
        margin-top: 1;
        margin-bottom: 0;
    }

    .skill-node {
        border: round #594875;
        padding: 0 1;
        margin: 0 0 1 2;
        color: #d6d6e0;
        height: auto;
    }

    #skill-tree-content {
        height: 1fr;
        width: 100%;
        overflow-y: auto;
        padding-right: 1;
    }

    #skill-tree-content Button {
        width: 100%;
        height: auto;
        min-height: 3;
        margin: 0 0 1 2;
        text-align: left;
    }

    .skill-learned {
        border: round #6b9b73;
    }

    .skill-available {
        border: round #c4a7ff;
    }

    #skill-message {
        color: #e3c77a;
        text-style: bold;
        margin-bottom: 1;
    }
    """

    def __init__(self):
        super().__init__()

        self.session = GameSession()
        self.battle_log = []
        self.battle_animating = False

    @property
    def character(self):
        return self.session.character

    @property
    def enemy(self):
        return self.session.enemy

    def compose(self) -> ComposeResult:

        yield Header()

        with Vertical(id="main-screen"):
            yield Static(
                "THE LAST QUEST\n\n" "A new adventure awaits...", classes="title"
            )

        with Horizontal(id="actions"):
            yield Button("Explore", id="explore")
            yield Button("Map", id="map")
            yield Button("Character", id="character")
            yield Button("Inventory", id="inventory")
            yield Button("Exit", id="exit")

        yield Footer()

    async def on_mount(self):
        await self.show_character_creation()

    async def clear_screen(self):

        screen = self.query_one("#main-screen", Vertical)
        await screen.remove_children()
        await screen.mount(Horizontal(id="interaction-actions"))

        return screen

    async def mount_interaction_buttons(self, *buttons):
        actions = self.query_one("#interaction-actions", Horizontal)
        await actions.mount(*buttons)

    def show_ascii_character(self):
        character_ascii = """
⡟⠛⡻⠟⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⢛⣛⣛⡻⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⣟⠛⠛⠛⠛⠛⢛⣛⣛⣛⣛⣛⣛⣛⣛⣛⣛⣛⢻
⡇⣶⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⣖⠒⠊⠉⠉⣥⣤⣤⠒⠒⠒⠒⠒⢒⠒⠒⠒⣿⣦⣤⣤⠒⠒⠊⠉⣭⣭⣭⣭⣭⣭⣭⣭⣭⣭⢺
⡇⠀⢳⡆⠀⠀⠀⠀⣀⡰⠶⠟⣉⣀⡰⠶⠞⠉⠉⠀⠀⠀⣀⣀⣀⣀⣁⣀⠶⠶⠞⠛⢃⣀⣀⠶⠞⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠶⣾
⡇⠀⢸⠃⠀⢀⣴⡖⠉⡥⠔⠒⠁⠀⠀⠀⠀⣠⣤⡔⠒⠒⠺⣭⣭⠛⠋⠉⠀⢠⣤⣶⣾⣯⡉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹
⡇⠀⡏⢀⡶⠉⡰⠾⠈⠀⠀⣀⠰⠶⠶⠉⣁⣁⠶⠶⠎⠉⠉⠀⠀⣀⡰⠶⠿⠉⠁⠀⠀⠈⠉⠹⠶⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⡇⠀⡟⠋⣤⠛⠀⢠⣤⡜⠛⠀⠠⣤⡜⠛⠉⠉⠀⠀⠀⢀⣤⡜⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸
⡇⣿⣱⠎⠉⣀⠎⠉⣀⡰⠶⠋⠁⠀⠀⠀⠀⢀⣠⣶⡎⠉⢀⡀⠀⠀⠀⠀⠀⠀⠀⠐⣂⡀⠀⠀⢄⠀⠠⠬⠱⣄⠀⠀⠀⠀⠀⠀⠀⢸
⡇⣿⠘⣤⡟⢀⣼⡟⠁⠀⠀⠀⠀⠀⢀⣤⡜⠛⣿⠘⢣⡀⢸⣟⣢⡀⠀⠀⠀⠀⠀⠀⠸⣧⣤⠀⠀⠈⣤⠀⠀⠀⠳⣤⡀⠀⠀⢠⣤⢸
⡇⣿⢦⡱⠿⠉⠀⠀⠀⠀⠀⣀⣰⢶⡿⠉⢇⡀⣿⡶⢖⣉⣶⡈⠳⣩⣂⠀⠀⠀⠀⣀⠀⠸⣄⢹⣆⡀⠙⣦⣀⠀⠀⠈⣉⣉⣉⡵⠉⢸
⣧⡿⠃⠀⠀⠀⠀⢀⣀⣤⠜⠛⢃⡼⠇⣀⠜⠟⠦⠟⠃⠀⠘⠛⠛⠤⠤⠤⣤⣀⣀⣀⠻⠧⠿⣼⡇⠛⠤⡗⠛⠿⡣⠤⡤⠯⠀⠀⠀⢸
⡏⠀⠀⠀⣀⣠⡶⠾⠉⠁⢀⠀⢸⡇⠰⠙⠁⠀⠶⠶⠆⠀⠀⠀⠀⠀⠈⠁⠉⠉⢹⣿⠶⠶⣶⣿⡇⠀⠀⠁⠈⠉⢹⡆⠀⠀⠀⠀⠀⢸
⡇⣀⣤⡾⣿⠀⠀⠀⠀⠀⠘⣴⢸⣇⣤⣿⠿⠿⣿⡿⠿⣿⠤⠀⠀⠀⠀⠀⠀⣠⣤⣤⣤⣤⣀⢸⡇⠀⠀⠀⠀⠀⠘⢣⠀⠀⠀⠀⠀⢸
⣷⣿⠏⢱⡏⠀⡆⠀⠀⠀⠀⠙⣾⡏⢹⠉⠀⠀⣿⢸⡎⣭⠸⠀⠀⠀⠀⠀⠀⠉⢹⣭⠝⠛⣿⢸⡇⢦⣀⠀⠀⠀⠀⠈⠓⣤⡄⢠⠀⢸
⣿⠁⣼⠇⠁⠀⡀⠀⠀⠀⠀⠀⠈⠣⣀⠋⠄⠀⠛⢄⣀⡿⠀⠀⠀⠀⠀⠀⠀⠀⢸⠛⢺⡇⠿⠸⠇⠀⠀⠀⠠⠤⡤⠤⠤⠤⠼⠟⠀⢸
⣿⣶⣇⠁⠀⠀⡇⡦⠀⠀⠀⠀⠀⠀⠈⠒⢤⡄⠀⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⠊⠁⠀⡖⠁⠀⠀⠀⠀⠀⠙⢢⡀⠀⠀⠀⣀⣼
⡿⠛⠀⣀⣶⠛⡳⢟⠾⠶⠶⢶⣞⠻⠛⠿⠟⠅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠃⠀⠀⠀⠀⢻⡶⢆⣀⡀⠀⠀⠀⠀⠙⠶⡞⠛⠀⢸
⣧⣤⠚⣻⡏⣶⠀⠘⣤⠀⠀⠈⢻⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣧⣬⣥⣤⣤⡀⠀⠀⠀⠀⢱⣦⠀⢸
⡿⠁⠀⠙⣗⣀⡸⠿⠍⡆⠀⠀⠠⠈⠳⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⠶⠦⠀⠀⠀⠀⠀⣾⠃⣇⠀⠀⠀⠉⠽⢿⣷⢶⣀⡈⣶⢸
⡇⠀⠀⠀⠉⣿⡇⢦⣤⣽⣦⡀⠀⠀⠀⠉⢣⡄⠀⠀⠀⠀⠀⠀⠀⠉⠉⠁⠀⠀⠀⠀⠀⢠⣾⠋⠀⠀⠒⠄⠀⠀⠀⠈⠛⣏⠙⢿⠉⣾
⡇⣠⠀⠐⠀⠀⠱⢆⠀⠀⠈⠻⣆⡀⠀⠀⠀⠈⠶⢆⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣾⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⡇⠀⠀⢹
⡇⣿⠀⠀⠀⠀⠀⠀⠛⣤⡄⠀⠘⢻⣦⣤⠀⠀⠀⠀⠀⠛⣧⡄⠀⠀⠀⠀⠀⢠⣼⣿⣥⣤⣤⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀⢐⣧⡄⠀⢸
⡧⣿⢷⡀⠀⠀⠀⠀⠀⠈⠉⠶⢶⣸⡇⠉⠉⠳⠶⣂⡀⠀⠀⠈⠳⣶⣀⣀⣶⣿⡷⠶⣂⣀⠀⠩⡉⠉⠉⠶⠾⣶⡀⠀⠀⢸⡏⡉⠹⢾
⣿⣋⣾⣿⣄⠀⢀⠀⠀⠀⠀⣠⠤⢼⡃⠀⠀⠀⠀⠀⠙⠛⠤⣄⣀⠘⠻⢟⠀⠀⢸⣦⡀⠙⠛⠛⠤⠤⠤⠀⠀⠀⠘⠛⠀⠸⡇⡇⠀⢸
⡇⠿⣮⡱⠿⠶⠈⠱⣀⠀⢀⠿⠀⠸⢆⣀⠀⠀⠀⠀⠀⣀⣰⡾⠿⢶⡀⠈⣶⠀⠈⣿⢶⠶⢶⠶⠦⢀⣀⣀⡀⢀⠀⠀⠀⠈⢁⡇⠀⢸
⡇⠀⠀⠘⠛⠛⠣⣄⣀⣿⡟⠀⠀⠀⠀⠤⠿⠿⠿⠟⢛⠃⠀⠀⠀⠀⠘⠧⣀⢇⣠⠁⠜⠀⠚⠀⣸⠁⠸⣸⡟⠛⠻⢟⠛⠛⠛⠃⠀⢸
⣧⣤⣤⣤⣤⣤⣴⣾⣩⣽⣇⣀⣠⣶⣄⣀⣠⣀⣄⣤⣹⣶⣀⣀⣀⣀⣀⣄⣿⣼⣧⣄⣤⣤⣄⣴⣥⣤⣀⣼⣇⣀⣀⣈⣶⣤⣤⣤⣤⣼
"""
        return character_ascii

    async def show_character_creation(self):

        screen = await self.clear_screen()

        await screen.mount(
            Static("CHARACTER CREATION", classes="title"),
            Static("Choose your name:"),
            Input(placeholder="Enter your name, wizard...", id="char-name"),
            Static("Choose your specialization:"),
            Select(
                [
                    (f"{details['name']} — {details['description']}", spec_id)
                    for spec_id, details in SPECIALIZATIONS.items()
                ],
                value=next(iter(SPECIALIZATIONS), Select.BLANK),
                id="char-class",
            ),
            Static("Your journey begins with a choice.", id="creation-info"),
        )
        await self.mount_interaction_buttons(
            Button(
                "Create Character", id="create-character", disabled=not SPECIALIZATIONS
            )
        )

    async def create_character(self):

        name = self.query_one("#char-name", Input).value.strip()

        specialization = self.query_one("#char-class", Select).value

        if not name:
            self.query_one("#creation-info", Static).update("Please enter a name.")

            return

        if not isinstance(specialization, str):
            return

        if not self.session.create_character(name, specialization):
            self.query_one("#creation-info", Static).update(
                "Choose a valid name and specialization."
            )
            return

        await self.show_location()

    async def show_location(self, message=None):

        if not self.character:
            await self.show_character_creation()
            return

        location = self.session.current_location

        if location is None:
            return

        screen = await self.clear_screen()

        await screen.mount(
            Static(f"LOCATION: {location.name.upper()}", classes="title"),
            Static(location.description, classes="subtitle"),
            Static(
                f"Wizard: {self.character['name']}\n"
                f"HP: {self.character['hp']}/{self.character['max_hp']}\n"
                f"Mana: {self.character['mana']}/{self.character['max_mana']}\n"
                f"Level: {self.character['level']}",
                classes="info",
            ),
            Static(message or "What would you like to do?", id="location-message"),
        )

        await self.mount_interaction_buttons(
            Button("Search for creatures", id="search")
        )

        for direction, destination_id in location.connections.items():

            destination = self.session.world.get_location(destination_id)

            if destination is None:
                continue

            await self.mount_interaction_buttons(
                Button(
                    f"Travel {direction.title()} - {destination.name}",
                    id=f"travel-{direction}",
                )
            )

    async def travel(self, direction):
        if self.session.travel(direction):
            await self.show_location("You traveled to a new location.")

    async def search_location(self):

        location = self.session.current_location

        if location is None:
            return

        enemy, message = self.session.search()
        if enemy is None:
            await self.show_location(message)
            return

        self.battle_log = [f"A {enemy['name']} appeared!", "Prepare yourself!"]

        await self.show_battle()

    async def show_battle(self):

        if not self.enemy or not self.character:
            return

        screen = await self.clear_screen()

        await screen.mount(
            Static("BATTLE", classes="title"),
            Static(
                f"{self.enemy['name']} · HP {max(0, self.enemy['hp'])}/{self.enemy['max_hp']}"
            ),
            ProgressBar(
                total=self.enemy["max_hp"],
                show_percentage=False,
                show_eta=False,
                id="enemy-hp-bar",
                classes="health-bar",
            ),
            Static(
                f"{self.character['name']} · HP {self.character['hp']}/{self.character['max_hp']}"
            ),
            ProgressBar(
                total=self.character["max_hp"],
                show_percentage=False,
                show_eta=False,
                id="player-hp-bar",
                classes="health-bar",
            ),
            Static(
                f"Mana: {self.character['mana']}/{self.character['max_mana']}",
                classes="info",
            ),
            ProgressBar(
                total=self.character["max_mana"],
                show_percentage=False,
                show_eta=False,
                id="player-mana-bar",
                classes="health-bar",
            ),
            Static("\n".join(self.battle_log[-7:]), id="battle-log"),
            Static("Choose your spell:"),
        )
        enemy_bar = screen.query_one("#enemy-hp-bar", ProgressBar)
        player_bar = screen.query_one("#player-hp-bar", ProgressBar)
        mana_bar = screen.query_one("#player-mana-bar", ProgressBar)

        self.set_health_bar_state(enemy_bar, self.enemy["hp"], self.enemy["max_hp"])
        self.set_health_bar_state(
            player_bar, self.character["hp"], self.character["max_hp"]
        )

        enemy_bar.update(
            progress=max(0, self.enemy["hp"])
        )
        player_bar.update(
            progress=max(0, self.character["hp"])
        )

        mana_bar.update(
            progress=max(0, self.character["mana"])
        )
        await self.mount_interaction_buttons(
            *[
                Button(
                    f"{spell['name']} ({spell['cost']} Mana)",
                    id=f"spell-{spell_id}",
                    disabled=(
                        self.battle_animating
                        or self.character["mana"] < spell["cost"]
                        or (
                            spell["type"] == "heal"
                            and self.character["hp"] >= self.character["max_hp"]
                        )
                    ),
                )
                for spell_id, spell in self.session.available_spells().items()
            ],
            Button("Retreat", id="retreat", disabled=self.battle_animating),
        )

    @staticmethod
    def set_health_bar_state(bar: ProgressBar, hp: int, max_hp: int) -> None:
        bar.remove_class("health-low", "health-critical")
        ratio = hp / max_hp if max_hp else 0
        if ratio <= 0.25:
            bar.add_class("health-critical")
        elif ratio <= 0.5:
            bar.add_class("health-low")

    async def show_battle_event(self, message):
        self.battle_log = [message]
        if self.enemy and self.character:
            await self.show_battle()
        else:
            await self.show_location(message)
            await asyncio.sleep(2)
        await asyncio.sleep(2)

    async def cast_spell(self, spell_id):
        if not self.character or not self.enemy or self.battle_animating:
            return
        self.battle_animating = True
        try:
            message, finished, _reward = self.session.cast_spell_player(spell_id)
            await self.show_battle_event(message)
            if finished:
                self.battle_log = []
                return

            message, finished = self.session.enemy_attack()
            await self.show_battle_event(message)
            if finished:
                self.battle_log = []
                return
        finally:
            self.battle_animating = False
        await self.show_battle()

    async def show_character(self):

        if not self.character:
            await self.show_character_creation()
            return

        p = self.character

        screen = await self.clear_screen()

        ascii_character = self.show_ascii_character()

        await screen.mount(
            Static("CHARACTER SHEET", classes="title"),
            Horizontal(
                Static(
                    f"Name: {p['name']}\n"
                    f"Specialization: {SPECIALIZATIONS[p['class']]['name']}\n"
                    f"Level: {p['level']}\n\n"
                    f"HP: {p['hp']}/{p['max_hp']}\n"
                    f"Mana: {p['mana']}/{p['max_mana']}\n\n"
                    f"Intelligence: {p['intelligence']}\n"
                    f"Magic Bonus: +{p['bonus_damage']}\n\n"
                    f"XP: {p['xp']}/{p['xp_next']}\n\n"
                    f"Skill points: {p['skill_points']}\n"
                    f"Learned skills: {len(p['skills'])}\n\n"
                    f"{SPECIALIZATIONS[p['class']]['description']}",
                    classes="info",
                    id="character-details",
                ),
                Static(ascii_character, id="character-art"),
                id="character-sheet",
            ),
        )
        await self.mount_interaction_buttons(
            Button("Skill tree", id="skill-tree"),
            Button("Back", id="back"),
        )

    async def show_skill_tree(self, message=None):
        if not self.character:
            await self.show_character_creation()
            return
        player = self.character
        tree = SKILL_TREES.get(player["class"], {})
        screen = await self.clear_screen()
        await screen.mount(
            Static("SKILL TREE", classes="title"),
            Static(
                f"{SPECIALIZATIONS[player['class']]['name']} · Level {player['level']} · "
                f"Skill points: {player['skill_points']}",
                classes="subtitle",
            ),
            VerticalScroll(id="skill-tree-content"),
        )
        content = screen.query_one("#skill-tree-content", VerticalScroll)
        if message:
            await content.mount(Static(message, id="skill-message"))

        skills_by_level = {}
        for skill_id, node in tree.items():
            skills_by_level.setdefault(node["level"], []).append(skill_id)

        def node_label(skill_id):
            node = tree[skill_id]
            learned = skill_id in player["skills"]
            prerequisites_met = all(req in player["skills"] for req in node["requires"])
            can_learn = (
                not learned
                and player["level"] >= node["level"]
                and prerequisites_met
                and player["skill_points"] > 0
            )
            if learned:
                status = "✓ Learned"
            elif player["level"] < node["level"]:
                status = f"Locked · reach level {node['level']}"
            elif not prerequisites_met:
                status = "Locked · learn prerequisite first"
            else:
                status = (
                    "Available · 1 point"
                    if player["skill_points"]
                    else "Available · no points"
                )
            required = (
                " + ".join(tree[req]["name"] for req in node["requires"] if req in tree)
                or "Starting skill"
            )
            return (
                f"{'✓' if learned else '○'} {node['name']}  ·  {status}\n"
                f"{node['description']}\nRequires: {required}",
                can_learn,
                "skill-learned" if learned else ("skill-available" if can_learn else ""),
            )

        for level in sorted(skills_by_level):
            await content.mount(Static(f"LEVEL {level}", classes="skill-level"))
            for skill_id in skills_by_level[level]:
                label, can_learn, status_class = node_label(skill_id)
                classes = "skill-node" + (f" {status_class}" if status_class else "")
                if can_learn:
                    await content.mount(
                        Button(label, id=f"skill-{skill_id}", classes=classes)
                    )
                else:
                    await content.mount(Static(label, classes=classes))
        await self.mount_interaction_buttons(Button("Back", id="back"))

    async def show_inventory(self):

        screen = await self.clear_screen()

        await screen.mount(
            Static("INVENTORY", classes="title"),
            Static(
                f"Items: {self.session.inventory.count_items()}\n"
                f"Available slots: {self.session.inventory.get_available_slots()}\n"
                f"Total slots: {self.session.inventory.max_slots}",
                classes="info",
            ),
        )
        await self.mount_interaction_buttons(Button("Back", id="back"))

    async def show_map(self):

        screen = await self.clear_screen()

        current = self.session.current_location

        if current is None:
            await screen.mount(
                Static("ELDORIA WORLD MAP", classes="title"),
                Static("No current location is set.", classes="info"),
            )
            await self.mount_interaction_buttons(Button("Back", id="back"))
            return

        await screen.mount(
            Static("ELDORIA WORLD MAP", classes="title"),
            Static(
                f"Current location: {current.name}\n\n" f"Connected locations:",
                classes="info",
            ),
        )

        for direction, destination_id in current.connections.items():

            destination = self.session.world.get_location(destination_id)
            if destination is None:
                continue

            await self.mount_interaction_buttons(
                Button(f"{destination.name} ({direction})", id=f"travel-{direction}")
            )

        await self.mount_interaction_buttons(Button("Back", id="back"))

    async def on_button_pressed(self, event: Button.Pressed):

        button_id = event.button.id

        if button_id is None:
            return

        if self.battle_animating:
            return

        if button_id == "create-character":

            await self.create_character()

        elif button_id == "explore":

            await self.show_location()

        elif button_id == "search":

            await self.search_location()

        elif button_id == "map":

            await self.show_map()

        elif button_id == "character":

            await self.show_character()

        elif button_id == "skill-tree":
            await self.show_skill_tree()

        elif button_id.startswith("skill-"):
            skill_id = button_id.split("-", 1)[1]
            _learned, message = self.session.learn_skill(skill_id)
            await self.show_skill_tree(message)

        elif button_id == "inventory":

            await self.show_inventory()

        elif button_id == "back":

            await self.show_location()

        elif button_id == "retreat":

            self.session.retreat()
            await self.show_location("You retreated from the encounter.")

        elif button_id.startswith("travel-"):

            direction = button_id.split("-", 1)[1]

            await self.travel(direction)

        elif button_id.startswith("spell-"):

            spell_id = button_id.split("-", 1)[1]

            await self.cast_spell(spell_id)

        elif button_id == "exit":

            self.exit()
