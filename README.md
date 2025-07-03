# 🎶 KuzoBot

**KuzoBot** is a powerful Discord bot, which currently only has the functionality of a music bot, built with [discord.py](https://github.com/Rapptz/discord.py), [Wavelink](https://github.com/PythonistaGuild/Wavelink), and [Spotipy](https://github.com/plamere/spotipy). It supports music playback from YouTube and can intelligently handle Spotify links (tracks, playlists, and albums) by searching their counterparts on YouTube.

---

## 🚀 Features

- ✅ Plays music from YouTube
- 🔁 Queue management
- 🎧 Spotify support (track, playlist, album)
- 🌙 Nightcore audio effect
- 🔊 Volume and playback controls
- 📜 Now Playing + Rich embeds
- ⚙️ Lavalink integration

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/kuzobot.git
cd kuzobot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your environment

Create a file called `secret.py` in the root directory and add your Spotify credentials:

```python
DISCORD_TOKEN = 'your_discord_token'
SPOTIFY_CLIENT_ID = 'your_spotify_client_id'
SPOTIFY_CLIENT_SECRET = 'your_spotify_client_secret'
```

Make sure you also configure your Discord bot token in your `main.py` or environment variables (not included here for security).

### 4. Run a Lavalink server

You must have a Lavalink server running locally or remotely. Example (local setup):

```bash
java -jar Lavalink.jar
```

Ensure your `Node` is pointed to `http://localhost:2333` with the correct password.

### 5. Start the bot

```bash
python main.py
```

---

## 💻 Commands

| Command             | Aliases         | Description                                                               |
|---------------------|------------------|---------------------------------------------------------------------------|
| `!play <query>`     | —                | Play a song, playlist, or album. Supports Spotify links and search terms. |
| `!queue`            | —                | Display the current music queue.                                          |
| `!skip`             | —                | Skip the current track.                                                   |
| `!nightcore`        | —                | Apply a nightcore (pitch + speed) filter.                                 |
| `!toggle`           | `pause`, `resume`| Toggle pause/resume playback.                                             |
| `!volume <0-100>`   | —                | Set the playback volume.                                                  |
| `!disconnect`       | `dc`             | Disconnect the bot from the voice channel.                                |

---

## 🎵 Spotify Integration

KuzoBot can interpret and play content from the following Spotify links:

- **Tracks**
- **Playlists**
- **Albums**

It fetches the metadata via Spotify's API and performs a YouTube search using the track title and artist name.

---

## 🧠 How It Works

- Uses Wavelink to communicate with Lavalink for audio streaming.
- Detects Spotify URLs and resolves them using the Spotify Web API.
- Converts Spotify tracks into YouTube searches via `ytsearch:` queries.
- Sends rich embed messages for now-playing and queue info.

---

## 📁 File Structure (simplified)

```
kuzobot/
├── commands/
│   └── music.py           # All music commands (play, skip, queue, etc.)
├── secret.py              # Spotify credentials (not included in repo)
├── bot.py                 # Bot setup
├── main.py                # Bot initialization
└── README.md              # You are here
```

---

## ⚠️ Disclaimer

This bot does **not** stream directly from Spotify. It uses Spotify data to search for equivalent content on YouTube. This is done in compliance with YouTube and Spotify's usage guidelines.

---

## 🙏 Credits

- [discord.py](https://github.com/Rapptz/discord.py)
- [Wavelink](https://github.com/PythonistaGuild/Wavelink)
- [Spotipy](https://github.com/plamere/spotipy)
- [Colorlog](https://github.com/borntyping/python-colorlog)

---

## 📃 License

This project is licensed under the MIT License.

---

### ✨ Enjoy your bot powered by KuzoBot!
