import feedparser

feed_url = "https://letterboxd.com/janjre1/rss/"
feed = feedparser.parse(feed_url)


for entry in feed.entries:
    info = str(entry.get("title")) # "Maestro, 2023 - ★½"
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

    stars = total

    print(f"Name: {name}, date: {date}, rating: {stars}")