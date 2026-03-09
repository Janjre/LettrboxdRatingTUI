import math
from statistics import variance

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
            event.stop()
            self.screen.dismiss(self.text)



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

        yield Vertical(
            Horizontal(
                Container(Button(self.Film1, id = "film-a-text",classes="option-text",variant = "success"),classes="option"),
                Container(Button(self.Film2, id = "film-b-text",classes="option-text",variant = "error"),classes="option",id="film-b")
            ,id = "top"),
            Container(Button("They are both equally good", id = "neutral-text",classes="option-text"),classes="option",id="bottom")
        )
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.log("A button was pressed with id " + event.button.id)
        if event.button.id == "film-a-text":
            self.screen.dismiss(self.Film1)
        if event.button.id == "film-b-text":
            self.screen.dismiss(self.Film2)
        if event.button.id == "neutral-text":
            self.screen.dismiss("neutral")

class ResultScreen (Screen):
    CSS_PATH = "result.tcss"
    def __init__(self, rating: float):
        self.Rating = round(rating * 2) / 2 # round to .5
        super().__init__()

    def compose(self) -> ComposeResult:
        whole_stars = math.floor(self.Rating)
        half_star = self.Rating % 1 == 0.5
        text = "★" * whole_stars
        if half_star:
            text += "½"

        yield Static(f"You should rate this film: {text}")



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

        data: list[dict] = []

        for entry in feed.entries:
            info = str(entry.get("title"))  # "Maestro, 2023 - ★½"
            first = info.split(",")
            name = first[0]
            second = first[1].split("-")
            date = int(second[0].strip())
            stars_as_text = second[1].strip()
            total = 0
            for char in stars_as_text:
                if char == "★":
                    total += 1
                elif char == "½":
                    total += 0.5

            data.append({
                "name" : name,
                "date": date,
                "rating": total
            })


        max_rating = 5
        min_rating = 0

        active_films = data.copy()
        keep_going = True

        score = -1

        while keep_going:
            decision = await self.push_screen_wait(Preference("What you just watched", active_films[0]["name"]))

            if decision == "neutral":
                score = active_films[0]["rating"]
                self.app.log(score)
                await self.push_screen_wait(ResultScreen(score))

                await self.action_quit()
                break
            if decision == "What you just watched":
                min_rating = active_films[0]["rating"]
            else:
                max_rating =active_films[0]["rating"]

            self.app.log(f"min_rating: {min_rating}, max_rating: {max_rating}")


            active_films.pop(0)

            self.app.log(f"active films is {len(active_films)} long before filter")

            active_films = list(filter(lambda x: min_rating < x["rating"] < max_rating, active_films))

            self.app.log(f"active films is now {len(active_films)} long after filter")

            if len(active_films) == 0 or max_rating - min_rating < 1:
                score =  (max_rating + min_rating) / 2
                break

        await self.push_screen_wait(ResultScreen(score))

        await self.action_quit()



app = LettrboxdTUI()
app.run()