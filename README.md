# Discord MP3 Bot

This is a Discord bot that downloads YouTube audio as MP3s with optional metadata like title, artist, album, and cover art. It also zips the file if it's too large and entertains users with random horse GIFs while processing.

---

## Example Usage

Attach image to the message for album cover, then use the command:

```bash
!mp3 https://www.youtube.com/watch?v=dQw4w9WgXcQ --title "Never Gonna Give You Up" --artist "Rick Astley" --album "Whenever You Need Somebody"
```

## Features

- `!mp3 <url> [--title "Song"] [--artist "Artist"] [--album "Album"]`
  - Downloads and tags MP3 audio from a YouTube link.
  - Automatically resizes and embeds album cover (if image attached).
  - Zips files larger than 8MB.
  - Too bad if the file is larger than 8MB, it won't work.
  - All flags are optional.
- `!hello`
  - Test command.

## .Env Variables

- `TOKEN`: Your Discord bot token.
- `GIPHY`: Your Giphy API key for fetching random horse GIFs (optional).
