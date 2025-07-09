# 🎶 KuzoBot

**KuzoBot** is a powerful Discord bot focused on music playback, built with [discord.py](https://github.com/Rapptz/discord.py), [Wavelink](https://github.com/PythonistaGuild/Wavelink), and [Spotipy](https://github.com/plamere/spotipy). It supports music from YouTube and intelligently handles Spotify links (tracks, playlists, and albums) by searching for their counterparts on YouTube.

---

## 🚀 Features

- ✅ Plays music from YouTube
- 🔁 Queue management
- 🎧 Spotify support (track, playlist, album)
- 🌙 Nightcore audio effect
- 🔊 Volume and playback controls
- 📜 Now Playing + Rich embeds
- ⚙️ Lavalink integration
- ⏭️ Play next command
- 🤖 Auto-disconnect on inactivity or alone in voice

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

Create a file called `secret.py` in the root directory and add your credentials:

```python
DISCORD_TOKEN = 'your_discord_token'
SPOTIFY_CLIENT_ID = 'your_spotify_client_id'
SPOTIFY_CLIENT_SECRET = 'your_spotify_client_secret'
```

### 4. Run a Lavalink server

You must have a Lavalink server running. Example (local setup):

```bash
java -jar Lavalink.jar
```

Ensure your `Node` is configured for `http://localhost:2333` with the correct password.

### 5. Start the bot

```bash
python main.py
```

---

## 💻 Commands

| Command               | Aliases         | Description                                                               |
|----------------------|------------------|---------------------------------------------------------------------------|
| `!play <query>`      | —                | Play a song, playlist, or album. Supports Spotify links and search terms. |
| `!playnext <query>`  | —                | Queue a track to be played next. Supports Spotify track links.            |
| `!queue`             | —                | Display the current music queue.                                          |
| `!skip`              | —                | Skip the current track.                                                   |
| `!nightcore`         | —                | Apply a nightcore (pitch + speed) filter.                                 |
| `!toggle`            | `pause`, `resume`| Toggle pause/resume playback.                                             |
| `!volume <0-100>`    | —                | Set the playback volume.                                                  |
| `!disconnect`        | `dc`             | Disconnect the bot from the voice channel.                                |

---

## 🎵 Spotify Integration

KuzoBot can interpret and play:

- **Tracks**
- **Playlists**
- **Albums**

Spotify data is used to perform YouTube searches based on the track name and artist.

---

## 🧠 How It Works

- Uses Wavelink to stream via Lavalink.
- Detects Spotify URLs and fetches metadata with Spotipy.
- Converts Spotify items into `ytsearch:` YouTube queries.
- Sends rich embeds when tracks start and for queue info.
- Disconnects if left alone or inactive for set durations.

---

## 📁 File Structure (simplified)

```
kuzobot/
├── commands/
│   └── music.py           # Music command definitions
├── secret.py              # Credentials (not included in repo)
├── bot.py                 # Bot setup
├── main.py                # Bot initialization
└── README.md              # Project documentation
```

---

## ⚠️ Disclaimer

This bot does **not** stream directly from Spotify. Instead, it uses metadata to search for content on YouTube in compliance with usage guidelines.

---

## 🙏 Credits

- [discord.py](https://github.com/Rapptz/discord.py)
- [Wavelink](https://github.com/PythonistaGuild/Wavelink)
- [Spotipy](https://github.com/plamere/spotipy)
- [Colorlog](https://github.com/borntyping/python-colorlog)

---

## 📃 License

Licensed under the MIT License.

---

### ✨ Enjoy your music with KuzoBot!
