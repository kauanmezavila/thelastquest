import asyncio

from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Footer, Header, Input, ProgressBar, Select, Static

from .content import (
    DIALOGUES,
    DIALOGUE_UI,
    QUESTS,
    QUEST_UI,
    SPECIALIZATIONS,
    SKILL_TREES,
    STARTING_LOCATION,
)
from .game import GameSession


class _DialogueFormatContext(dict):
    def __missing__(self, key):
        return "{" + key + "}"


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
        min-width: 8;
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

    #interaction-actions.battle-actions {
        height: auto;
        layout: grid;
        grid-size: 4;
        grid-columns: 1fr 1fr 1fr 1fr;
        grid-gutter: 0 1;
    }

    #interaction-actions.battle-actions Button {
        width: 1fr;
        min-width: 0;
        margin: 0;
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

    #character-sheet-content {
        height: 1fr;
        width: 100%;
        padding: 0 1;
    }

    .character-hero {
        border: round #9b80d4;
        background: #211b2f;
        color: #e6d8ff;
        text-style: bold;
        padding: 1;
        margin-bottom: 1;
        height: auto;
    }

    .character-section {
        color: #c4a7ff;
        text-style: bold;
        margin-top: 1;
        margin-bottom: 1;
    }

    .character-stat-label {
        color: #ded8ed;
        margin-top: 1;
    }

    .character-stat-card {
        width: 1fr;
        height: auto;
        min-height: 6;
        border: round #594875;
        background: #19171f;
        color: #d6d6e0;
        padding: 1;
        margin: 0 1 1 0;
        text-align: center;
        content-align: center middle;
    }

    .location-hero {
        border: round #6b9b73;
        background: #15231b;
        color: #d9f2dc;
        text-style: bold;
        padding: 1 2;
        margin-bottom: 1;
        height: auto;
    }

    #location-content {
        height: 1fr;
        width: 100%;
        padding-right: 1;
    }

    #map-content {
        height: 1fr;
        width: 100%;
        padding: 0 1;
    }

    #map-network {
        width: 100%;
        height: auto;
        align: center middle;
    }

    .map-row {
        width: 100%;
        height: auto;
        align: center middle;
    }

    .map-slot {
        width: 1fr;
        height: 1;
    }

    .map-region-card {
        width: 1fr;
        min-height: 8;
        height: auto;
        margin: 1;
        padding: 1;
        border: round #594875;
        background: #19171f;
        color: #d6d6e0;
        text-align: center;
        content-align: center middle;
    }

    .map-region-current {
        border: round #6b9b73;
        background: #15231b;
        color: #d9f2dc;
        text-style: bold;
    }

    .map-routes {
        width: 1fr;
        height: auto;
        margin: 0 1 1 1;
        color: #c4a7ff;
        text-align: center;
    }

    #location-dashboard {
        width: 100%;
        height: auto;
        margin-bottom: 1;
    }

    .location-card {
        width: 1fr;
        height: 5;
        border: round #594875;
        background: #19171f;
        color: #e6d8ff;
        padding: 0 1;
        margin-right: 1;
        content-align: left middle;
    }

    .location-section {
        color: #c4a7ff;
        text-style: bold;
        margin-top: 1;
        margin-bottom: 0;
    }

    .location-routes {
        border: round #3f5946;
        background: #121a15;
        color: #cbe4ce;
        padding: 0 1;
        margin: 0 0 1 0;
        height: auto;
    }

    .location-message {
        border: round #594875;
        background: #19171f;
        color: #e6d8ff;
        padding: 0 1;
        margin: 1 0;
        height: auto;
    }

    .quest-local-tasks {
        width: 100%;
        height: auto;
        min-height: 3;
        border: round #3f5946;
        background: #121a15;
        color: #cbe4ce;
        padding: 1;
        margin-bottom: 1;
    }

    #quest-content {
        height: 1fr;
        width: 100%;
        padding: 0 1;
    }

    .quest-section-title {
        color: #d6ad44;
        text-style: bold;
        margin: 1 0;
    }

    .quest-card {
        width: 100%;
        height: auto;
        border: round #594875;
        background: #19171f;
        color: #e6d8ff;
        padding: 1 2;
        margin-bottom: 1;
    }

    .quest-completed {
        width: 100%;
        height: auto;
        border: round #3f5946;
        background: #121a15;
        color: #cbe4ce;
        padding: 1;
    }

    #dialogue-panel {
        width: 100%;
        height: 1fr;
        border: round #d6ad44;
        background: #19171f;
        padding: 1 2;
        margin: 1 0;
    }

    #dialogue-heading { color: #d6ad44; text-style: bold; text-align: center; width: 100%; margin-bottom: 1; }
    #dialogue-portrait { color: #d6ad44; text-style: bold; text-align: center; width: 100%; height: 3; content-align: center middle; }
    #dialogue-speaker { color: #e6d8ff; text-style: bold; text-align: center; width: 100%; margin-bottom: 1; }
    #dialogue-text { color: #eee9f5; padding: 1 2; border: round #594875; height: auto; min-height: 5; }
    #interaction-actions.dialogue-actions { height: auto; max-height: 12; overflow-y: auto; layout: vertical; }
    #interaction-actions.dialogue-actions Button { width: 100%; height: auto; min-height: 3; margin: 0 0 1 0; }

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

    .progress-bar Bar > .bar--bar {
        color: #ffd700;
        background: #604d11;
    }

    .progress-bar Bar > .bar--complete {
        color: #ffe680;
    }

    #player-mana-bar Bar > .bar--bar,
    #character-mana-bar Bar > .bar--bar {
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

    #map-content {
        height: 1fr;
        width: 100%;
        padding-right: 1;
    }

    .map-legend {
        color: #c4a7ff;
        border: round #594875;
        background: #19171f;
        padding: 0 1;
        margin-bottom: 1;
        height: auto;
        text-style: bold;
    }

    .map-row {
        width: 100%;
        height: auto;
        align: center middle;
    }

    .map-region-card {
        width: 1fr;
        height: auto;
        min-height: 7;
        border: round #594875;
        background: #19171f;
        color: #ded8ed;
        padding: 1;
        margin: 0 1 1 0;
        text-align: left;
    }

    .map-region-card:disabled {
        color: #8c8794;
        background: #17161b;
        border: round #393540;
    }

    .map-region-card.map-region-current {
        border: round #d6ad44;
        background: #2b2412;
        color: #fff0b3;
    }

    .map-region-current {
        border: round #d6ad44;
        background: #2b2412;
        color: #fff0b3;
    }

    .map-route {
        width: 20;
        height: auto;
        color: #9bd5a4;
        text-style: bold;
        text-align: center;
        content-align: center middle;
        padding: 0 1;
    }

    .map-route-blocked {
        color: #bf8585;
    }

    .map-region-list-title {
        color: #c4a7ff;
        text-style: bold;
        margin: 1 0;
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
        self.dialogue_location = None
        self.dialogue_line_index = 0
        self.dialogue_choices = []

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
            yield Button(QUEST_UI["button"], id="quests")
            yield Button("Map", id="map")
            yield Button("Character", id="character")
            yield Button("Inventory", id="inventory")
            yield Button("Save", id="save")
            yield Button("Exit", id="exit")

        yield Footer()

    async def on_mount(self):
        try:
            loaded = self.session.load_game()
        except (OSError, ValueError, TypeError) as error:
            self.notify(f"Save could not be loaded: {error}", title="Save error")
            await self.show_character_creation()
            return

        if not loaded:
            await self.show_character_creation()
        elif self.enemy:
            self.battle_log = [f"Battle resumed: {self.enemy['name']} is still here."]
            await self.show_battle()
        else:
            await self.show_location("Save loaded.")

    async def save_game(self):
        if not self.character:
            self.notify("Create a character before saving.", title="Save")
            return
        try:
            self.session.save_game()
        except OSError as error:
            self.notify(f"Could not save the game: {error}", title="Save error")
            return
        self.notify("Game saved.", title="The Last Quest", timeout=2)

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
        location_message = message or "What would you like to do?"
        if message and "Victory!" in message:
            location_message = Text(message)
            victory_start = message.index("Victory!")
            location_message.stylize("bold yellow", victory_start, len(message))

        await screen.mount(VerticalScroll(id="location-content"))
        content = screen.query_one("#location-content", VerticalScroll)
        await content.mount(
            Static("THE LAST QUEST", classes="title"),
            Static(
                f"*  {location.name.upper()}  *\n{location.description}",
                classes="location-hero",
            ),
            Horizontal(
                Static(
                    f"ADVENTURER\n{self.character['name']}\n"
                    f"{SPECIALIZATIONS[self.character['class']]['name']} - "
                    f"Level {self.character['level']}",
                    classes="location-card",
                ),
                Static(
                    f"VITALS\nHP {self.character['hp']}/{self.character['max_hp']}  -  "
                    f"Mana {self.character['mana']}/{self.character['max_mana']}",
                    classes="location-card",
                ),
                id="location-dashboard",
            ),
            Static("PROGRESSION", classes="location-section"),
            Static(
                f"Level: {self.character['level']}/{self.character['max_level']}",
                classes="character-stat-label",
            ),
            ProgressBar(
                total=self.character["max_level"],
                show_percentage=False,
                show_eta=False,
                id="player-level-bar",
                classes="progress-bar",
            ),
            Static(
                (
                    "XP: MAX"
                    if self.character["level"] >= self.character["max_level"]
                    else f"XP: {self.character['xp']}/{self.character['xp_next']}"
                ),
                classes="character-stat-label",
            ),
            ProgressBar(
                total=max(1, self.character["xp_next"]),
                show_percentage=False,
                show_eta=False,
                id="player-xp-bar",
                classes="progress-bar",
            ),
            Static(
                f"HP: {self.character['hp']}/{self.character['max_hp']}",
                classes="character-stat-label",
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
                classes="character-stat-label",
            ),
            ProgressBar(
                total=self.character["max_mana"],
                show_percentage=False,
                show_eta=False,
                id="player-mana-bar",
                classes="health-bar",
            ),
            Static(QUEST_UI["local_title"], classes="location-section"),
            Static(
                self.local_quest_tasks(
                    self.session.location_keys_by_id.get(location.id)
                ),
                id="local-quest-tasks",
                classes="quest-local-tasks",
            ),
            Static("AVAILABLE ROUTES", classes="location-section"),
            Static(
                "\n".join(
                    f"→ {direction.title()} - " f"{destination.name}"
                    for direction, destination_id in location.connections.items()
                    if (destination := self.session.world.get_location(destination_id))
                    is not None
                )
                or "No routes from this location.",
                classes="location-routes",
            ),
            Static(location_message, id="location-message", classes="location-message"),
        )

        player_bar = content.query_one("#player-hp-bar", ProgressBar)
        mana_bar = content.query_one("#player-mana-bar", ProgressBar)
        level_bar = content.query_one("#player-level-bar", ProgressBar)
        xp_bar = content.query_one("#player-xp-bar", ProgressBar)

        self.set_health_bar_state(
            player_bar, self.character["hp"], self.character["max_hp"]
        )

        player_bar.update(progress=max(0, self.character["hp"]))

        mana_bar.update(progress=max(0, self.character["mana"]))
        level_bar.update(progress=self.character["level"])
        xp_bar.update(progress=self.character["xp"])

        await self.mount_interaction_buttons(
            Button("Search for creatures", id="search")
        )

        location_key = self.session.location_keys_by_id.get(location.id)
        if location_key in DIALOGUES:
            await self.mount_interaction_buttons(
                Button(DIALOGUE_UI["interact_label"], id="dialogue-start")
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

    def local_quest_tasks(self, location_key: str | None) -> str:
        tasks = []
        for quest_id, quest in QUESTS.items():
            if quest_id not in self.session.accepted_quests:
                continue
            progress = self.session.quest_progress.get(quest_id, [])
            for index, objective in enumerate(quest["objectives"]):
                if (
                    objective["location"] not in ("any", location_key)
                    and quest.get("origin") != location_key
                ):
                    continue
                current = progress[index] if index < len(progress) else 0
                count = objective["count"]
                tasks.append(
                    f"{'✓' if current >= count else '◇'} {objective['text']} "
                    f"[{current}/{count}]  ·  +{quest['reward'].get('xp', 0)} XP"
                )
        return "\n".join(tasks) if tasks else "No active tasks in this region."

    async def show_quests(self):
        screen = await self.clear_screen()
        await screen.mount(VerticalScroll(id="quest-content"))
        content = screen.query_one("#quest-content", VerticalScroll)
        await content.mount(
            Static("THE LAST QUEST  ·  JOURNAL", classes="title"),
            Static(QUEST_UI["title"], classes="quest-section-title"),
        )

        active_count = 0
        for quest_id, quest in QUESTS.items():
            if quest_id not in self.session.accepted_quests:
                continue
            active_count += 1
            progress = self.session.quest_progress.get(quest_id, [])
            details = [
                f"{objective['text']}   {'✓' if (progress[i] if i < len(progress) else 0) >= objective['count'] else '◇'} "
                f"{progress[i] if i < len(progress) else 0}/{objective['count']}"
                for i, objective in enumerate(quest["objectives"])
            ]
            reward_text = QUEST_UI["reward_format"].format(
                xp=quest["reward"].get("xp", 0)
            )
            await content.mount(
                Static(
                    f"{quest['title']}\n{quest['description']}\n\n"
                    f"OBJECTIVES\n" + "\n".join(details) + f"\n\n{reward_text}",
                    classes="quest-card",
                )
            )

        if not active_count:
            await content.mount(Static(QUEST_UI["empty"], classes="quest-card"))

        completed = [QUESTS[qid]["title"] for qid in self.session.completed_quests]
        if completed:
            await content.mount(
                Static(QUEST_UI["completed_title"], classes="quest-section-title"),
                Static(
                    "\n".join(f"✓ {title}" for title in completed),
                    classes="quest-completed",
                ),
            )
        await self.mount_interaction_buttons(Button("Back to the world", id="back"))

    async def travel(self, direction):
        if self.session.travel(direction):
            await self.show_location("You traveled to a new location.")

    async def show_dialogue(self, *, response=None, ended=False):
        location = self.session.current_location
        if location is None:
            return
        location_key = self.session.location_keys_by_id.get(location.id)
        if location_key is None:
            await self.show_location()
            return

        dialogue = DIALOGUES.get(location_key)
        if dialogue is None:
            await self.show_location()
            return

        quest_id = dialogue.get("quest_id")
        quest_status = (
            self.session.quest_status(quest_id) if quest_id in QUESTS else None
        )
        scene = dialogue.get("quest_states", {}).get(quest_status, dialogue)
        lines = scene.get("lines", dialogue.get("lines", []))
        context = self.dialogue_context(quest_id, quest_status, location)
        self.dialogue_choices = [
            {
                **choice,
                "text": self.format_dialogue_text(choice.get("text", ""), context),
                "reply": self.format_dialogue_text(choice.get("reply", ""), context),
            }
            for choice in scene.get("choices", dialogue.get("choices", []))
        ]
        lines = [self.format_dialogue_text(line, context) for line in lines]
        speaker = self.format_dialogue_text(dialogue["speaker"], context)
        title = self.format_dialogue_text(dialogue.get("title", ""), context)
        if not lines:
            await self.show_location()
            return

        screen = await self.clear_screen()
        actions = self.query_one("#interaction-actions", Horizontal)
        actions.add_class("dialogue-actions")
        await screen.mount(VerticalScroll(id="dialogue-panel"))
        panel = screen.query_one("#dialogue-panel", VerticalScroll)
        await panel.mount(
            Static(
                Text(DIALOGUE_UI["panel_title"], style=DIALOGUE_UI["accent"]),
                id="dialogue-heading",
            ),
            Static(
                Text(dialogue.get("portrait", "✦"), style=DIALOGUE_UI["accent"]),
                id="dialogue-portrait",
            ),
            Static(
                f"{speaker}  ·  {title}",
                id="dialogue-speaker",
            ),
            Static(
                response or lines[min(self.dialogue_line_index, len(lines) - 1)],
                id="dialogue-text",
            ),
        )

        if response is not None or ended:
            await self.mount_interaction_buttons(
                Button(DIALOGUE_UI["return_label"], id="dialogue-close")
            )
        elif self.dialogue_line_index < len(lines) - 1:
            await self.mount_interaction_buttons(
                Button(DIALOGUE_UI["continue_label"], id="dialogue-continue")
            )
        else:
            for index, choice in enumerate(self.dialogue_choices):
                await self.mount_interaction_buttons(
                    Button(choice["text"], id=f"dialogue-choice-{index}")
                )

    def dialogue_context(self, quest_id, quest_status, location) -> dict:
        player = self.character or {}
        context = dict(player)
        player_class = player.get("class")
        class_id = player_class if isinstance(player_class, str) else ""
        specialization = SPECIALIZATIONS.get(class_id, {})
        context.update(
            player_name=player.get("name", "Wanderer"),
            class_name=specialization.get("name", class_id or "Mage"),
            class_id=class_id,
            location_name=location.name,
            location_key=self.session.location_keys_by_id.get(location.id, ""),
            quest_status=quest_status or "",
            quest_title=QUESTS.get(quest_id, {}).get("title", ""),
            quest_reward_xp=QUESTS.get(quest_id, {}).get("reward", {}).get("xp", 0),
        )
        if quest_id in QUESTS and quest_id in self.session.quest_progress:
            progress = self.session.quest_progress[quest_id]
            context["quest_progress"] = ", ".join(
                f"{progress[index]}/{objective['count']}"
                for index, objective in enumerate(QUESTS[quest_id]["objectives"])
            )
        else:
            context["quest_progress"] = "0/0"
        return context

    @staticmethod
    def format_dialogue_text(value: str, context: dict) -> str:
        return value.format_map(_DialogueFormatContext(context))

    async def search_location(self):

        location = self.session.current_location

        if location is None:
            return

        enemy, message = self.session.search()
        if enemy is None:
            await self.show_location(message)
            return

        self.battle_log = [
            f"A level {enemy['level']} {enemy['name']} appeared!",
            "Prepare yourself!",
        ]

        await self.show_battle()

    async def show_battle(self):

        if not self.enemy or not self.character:
            return

        screen = await self.clear_screen()
        screen.query_one("#interaction-actions", Horizontal).add_class("battle-actions")

        await screen.mount(
            Static("BATTLE", classes="title"),
            Static(
                f"Level {self.enemy['level']} {self.enemy['name']} - "
                f"HP {max(0, self.enemy['hp'])}/{self.enemy['max_hp']}"
            ),
            ProgressBar(
                total=self.enemy["max_hp"],
                show_percentage=False,
                show_eta=False,
                id="enemy-hp-bar",
                classes="health-bar",
            ),
            Static(
                f"{self.character['name']} - HP {self.character['hp']}/{self.character['max_hp']}"
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

        enemy_bar.update(progress=max(0, self.enemy["hp"]))
        player_bar.update(progress=max(0, self.character["hp"]))

        mana_bar.update(progress=max(0, self.character["mana"]))
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

        await screen.mount(
            Static("CHARACTER SHEET", classes="title"),
            VerticalScroll(id="character-sheet-content"),
        )
        content = screen.query_one("#character-sheet-content", VerticalScroll)
        await content.mount(
            Static(
                f"{p['name']}  -  {SPECIALIZATIONS[p['class']]['name']}\n"
                f"{SPECIALIZATIONS[p['class']]['description']}",
                classes="character-hero",
            ),
            Static("VITALS", classes="character-section"),
            Static(
                f"Health  -  {p['hp']}/{p['max_hp']}", classes="character-stat-label"
            ),
            ProgressBar(
                total=p["max_hp"],
                show_percentage=False,
                show_eta=False,
                id="character-hp-bar",
                classes="health-bar",
            ),
            Static(
                f"Mana  -  {p['mana']}/{p['max_mana']}", classes="character-stat-label"
            ),
            ProgressBar(
                total=p["max_mana"],
                show_percentage=False,
                show_eta=False,
                id="character-mana-bar",
                classes="health-bar",
            ),
            Static("PROGRESSION", classes="character-section"),
            Static(
                f"Level  -  {p['level']}/{p['max_level']}",
                classes="character-stat-label",
            ),
            ProgressBar(
                total=p["max_level"],
                show_percentage=False,
                show_eta=False,
                id="character-level-bar",
                classes="progress-bar",
            ),
            Static(
                (
                    "XP  -  MAX"
                    if p["level"] >= p["max_level"]
                    else f"XP  -  {p['xp']}/{p['xp_next']}"
                ),
                classes="character-stat-label",
            ),
            ProgressBar(
                total=max(1, p["xp_next"]),
                show_percentage=False,
                show_eta=False,
                id="character-xp-bar",
                classes="progress-bar",
            ),
            Static("ATTRIBUTES", classes="character-section"),
            Horizontal(
                Static(
                    f"INTELLIGENCE\n{p['intelligence']}", classes="character-stat-card"
                ),
                Static(
                    f"MAGIC BONUS\n+{p['bonus_damage']}", classes="character-stat-card"
                ),
                Static(
                    f"SKILL POINTS\n{p['skill_points']}", classes="character-stat-card"
                ),
                Static(
                    f"SKILLS LEARNED\n{len(p['skills'])}", classes="character-stat-card"
                ),
                id="character-stat-cards",
            ),
        )
        hp_bar = content.query_one("#character-hp-bar", ProgressBar)
        mana_bar = content.query_one("#character-mana-bar", ProgressBar)
        self.set_health_bar_state(hp_bar, p["hp"], p["max_hp"])
        hp_bar.update(progress=max(0, p["hp"]))
        mana_bar.update(progress=max(0, p["mana"]))
        content.query_one("#character-level-bar", ProgressBar).update(
            progress=p["level"]
        )
        content.query_one("#character-xp-bar", ProgressBar).update(progress=p["xp"])
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
                f"{SPECIALIZATIONS[player['class']]['name']} - Level {player['level']} - "
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
                status = "Learned"
            elif player["level"] < node["level"]:
                status = f"Locked - reach level {node['level']}"
            elif not prerequisites_met:
                status = "Locked - learn prerequisite first"
            else:
                status = (
                    "Available - 1 point"
                    if player["skill_points"]
                    else "Available = no points"
                )
            required = (
                " + ".join(tree[req]["name"] for req in node["requires"] if req in tree)
                or "Starting skill"
            )
            return (
                f"{'[x]' if learned else '[ ]'} {node['name']}  -  {status}\n"
                f"{node['description']}\nRequires: {required}",
                can_learn,
                (
                    "skill-learned"
                    if learned
                    else ("skill-available" if can_learn else "")
                ),
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
            await self.mount_interaction_buttons(
                Button("Return to Eldoria", id="map-return-eldoria"),
                Button("Back", id="back"),
            )
            return

        await screen.mount(
            Static("ELDORIA WORLD MAP", classes="title"),
            VerticalScroll(id="map-content"),
        )

        map_content = screen.query_one("#map-content", VerticalScroll)
        await map_content.mount(
            Static(
                "The Ancient Fields",
                classes="map-legend",
            )
        )
        regions = list(self.session.locations_by_name.values())
        regions_by_key = {
            self.session.location_keys_by_id[region.id]: region for region in regions
        }

        # Lay out a breadth-first tree from Eldoria. Treat routes as links for
        # layout, even when travel itself is one-way, so every region appears.
        root_key = (
            STARTING_LOCATION
            if STARTING_LOCATION in regions_by_key
            else next(iter(regions_by_key))
        )
        adjacency = {key: [] for key in regions_by_key}
        for key, region in regions_by_key.items():
            for destination_id in region.connections.values():
                destination = self.session.world.get_location(destination_id)
                if destination is None:
                    continue
                destination_key = self.session.location_keys_by_id[destination.id]
                if (
                    destination_key in adjacency
                    and destination_key not in adjacency[key]
                ):
                    adjacency[key].append(destination_key)
                if (
                    destination_key in adjacency
                    and key not in adjacency[destination_key]
                ):
                    adjacency[destination_key].append(key)

        levels = [[root_key]]
        visited = {root_key}
        while len(visited) < len(regions_by_key):
            next_level = []
            for key in levels[-1]:
                for neighbor in adjacency[key]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        next_level.append(neighbor)
            if not next_level:
                next_level = [key for key in regions_by_key if key not in visited]
                visited.update(next_level)
            levels.append(next_level)

        positions = {root_key: (0, 0)}
        for depth, level in enumerate(levels[1:], start=1):
            # Alternate branches above and below Eldoria to keep the hub near
            # the middle as the world grows.
            row = (depth + 1) // 2 * (-1 if depth % 2 else 1)
            for index, key in enumerate(level):
                col = index * 2 - (len(level) - 1)
                positions[key] = (row, col)

        min_row = min(row for row, _ in positions.values())
        max_row = max(row for row, _ in positions.values())
        min_col = min(col for _, col in positions.values())
        max_col = max(col for _, col in positions.values())
        by_position = {
            (row - min_row, col - min_col): regions_by_key[key]
            for key, (row, col) in positions.items()
        }
        network = Vertical(id="map-network")
        await map_content.mount(network)
        for row_index in range(max_row - min_row + 1):
            row = Horizontal(classes="map-row")
            await network.mount(row)
            for col_index in range(max_col - min_col + 1):
                region = by_position.get((row_index, col_index))
                if region is None:
                    await row.mount(Static("", classes="map-slot"))
                    continue
                key = self.session.location_keys_by_id[region.id]
                is_current = region.id == current.id
                card = Button(
                    f"{'[x] YOU ARE HERE -' if is_current else '[ ] '}{region.name}\n"
                    f"Dimensions {region.width} × {region.height}m\n{region.description}",
                    id=f"map-go-{key}",
                    classes=(
                        "map-region-card map-region-current"
                        if is_current
                        else "map-region-card"
                    ),
                    disabled=is_current,
                )
                route_parts = []
                for direction, destination_id in region.connections.items():
                    destination = self.session.world.get_location(destination_id)
                    if destination is None:
                        continue
                    route_parts.append(f"{direction.upper()} > {destination.name}")
                route_text = "  ·  ".join(route_parts) or "No routes"
                await row.mount(
                    Vertical(card, Static(route_text, classes="map-routes"))
                )

        await self.mount_interaction_buttons(
            Button("Return to Eldoria", id="map-return-eldoria"),
            Button("Back", id="back"),
        )

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

        elif button_id == "dialogue-start":
            location = self.session.current_location
            self.dialogue_location = (
                self.session.location_keys_by_id.get(location.id) if location else None
            )
            self.session._record_quest_event("talk", self.dialogue_location)
            self.dialogue_line_index = 0
            await self.show_dialogue()

        elif button_id == "dialogue-continue":
            self.dialogue_line_index += 1
            await self.show_dialogue()

        elif button_id.startswith("dialogue-choice-"):
            choice_index = int(button_id.rsplit("-", 1)[1])
            if 0 <= choice_index < len(self.dialogue_choices):
                choice = self.dialogue_choices[choice_index]
                if choice.get("action") == "accept_quest":
                    dialogue = (
                        DIALOGUES.get(self.dialogue_location, {})
                        if self.dialogue_location is not None
                        else {}
                    )
                    quest_id = choice.get("quest_id", dialogue.get("quest_id"))
                    if not isinstance(quest_id, str) or not self.session.accept_quest(quest_id):
                        self.notify("This quest is no longer available.", title="Quest")
                await self.show_dialogue(response=choice["reply"], ended=True)

        elif button_id == "dialogue-close":
            self.dialogue_location = None
            await self.show_location()

        elif button_id == "map":

            await self.show_map()

        elif button_id == "quests":

            await self.show_quests()

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

        elif button_id == "save":

            await self.save_game()

        elif button_id == "back":

            await self.show_location()

        elif button_id == "map-return-eldoria":
            target = next(
                (
                    location
                    for location in self.session.locations_by_name.values()
                    if self.session.location_keys_by_id[location.id]
                    == STARTING_LOCATION
                ),
                None,
            )
            if target is not None:
                self.session.world.set_current_location(target.id)
                await self.show_location("You returned to Eldoria.")

        elif button_id == "retreat":

            self.session.retreat()
            await self.show_location("You retreated from the encounter.")

        elif button_id.startswith("travel-"):

            direction = button_id.split("-", 1)[1]

            await self.travel(direction)

        elif button_id.startswith("map-go-"):
            location_key = button_id.removeprefix("map-go-")
            target = next(
                (
                    location
                    for location in self.session.locations_by_name.values()
                    if self.session.location_keys_by_id[location.id] == location_key
                ),
                None,
            )
            if target:
                self.session.world.set_current_location(target.id)
                await self.show_location("You traveled to a new location.")

        elif button_id.startswith("spell-"):

            spell_id = button_id.split("-", 1)[1]

            await self.cast_spell(spell_id)

        elif button_id == "exit":

            self.exit()
