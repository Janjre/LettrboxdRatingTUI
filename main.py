import feedparser
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Center, Container
from textual.screen import Screen
from textual.widgets import Static, Header, TextArea, Button
import textual.events as events
from textual import on, work

class TextConsole(TextArea):
    def _on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.screen.dismiss(self.text)

            event.prevent_default()

class StartScreen (Screen[str]):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Lettrboxd review recommender", id = "title")
        yield Static("This works by looking at your recent public reviews and comparing them against the film you just watched. Based off which films it was better or worse than, it will recommend you a rating that accurately describes what you think of it. ", id = "paragraph")
        yield Static("To start, enter your username", id = "ask-for-entry")
        yield TextConsole(placeholder="Username",id = "username-entry")

class Preference (Screen[str]):

    CSS_PATH = "preference.tcss"
    def __init__(self,film1: str, film2: str):
        super().__init__()
        self.Film1 = film1
        self.Film2 = film2

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Which film do you prefer:", id = "title")
        yield Horizontal(
            Container(Button(self.Film1, id = "film-a-text",classes="option-text"),classes="option",id="film-a"),
            Container(Button(self.Film2, id = "film-b-text",classes="option-text"),classes="option",id="film-b")
        )

class LettrboxdTUI (App):

    CSS_PATH = "app.tcss"
    BINDINGS = [("q", "quit", "Quit")]
    def compose(self) -> ComposeResult:
        yield Header()

    @work
    async def on_mount(self) -> None:
        username = await self.push_screen_wait(StartScreen())

        feed_url = f"https://letterboxd.com/{username}/rss/"
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            print("Title:", entry.get("title"))
            print("Link:", entry.get("link"))
            print("Published:", entry.get("published"))
            print("Summary:", entry.get("summary"))
            print("-" * 40)


        decision = await self.push_screen_wait(Preference("a", "b"))
        await self.action_quit()



app = LettrboxdTUI()
app.run()