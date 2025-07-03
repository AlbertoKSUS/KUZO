import logging

import colorlog
import discord
from discord.ext import commands
import wavelink


class KuzoBot(commands.Bot):
    def __init__(self) -> None:
        # Logger configuration.
        handler = colorlog.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(
                '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S',
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red',
                },
                style='%'
            )
        )
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)
        self.log.addHandler(handler)

        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True

        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self) -> None:
        # Lavalink node setup.
        node = wavelink.Node(uri='http://localhost:2333', password='youshallnotpass')
        await wavelink.Pool.connect(client=self, nodes=[node], cache_capacity=100)

        await self.load_extension('commands.music')

    async def on_ready(self) -> None:
        self.log.info(f'✅ Logged in as {self.user} ({self.user.id})')


    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload) -> None:
        self.log.info(f'🎧 Lavalink node connected: {payload.node!r} | Resumed: {payload.resumed}')

    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload) -> None:
        player: wavelink.Player | None = payload.player
        track: wavelink.Playable = payload.track

        if not player:
            return

        embed = discord.Embed(title='🎶 Now Playing', description=f'**{track.title}** by `{track.author}`')

        if track.artwork:
            embed.set_thumbnail(url=track.artwork)

        if track.album.name:
            embed.add_field(name='Album', value=track.album.name)

        await player.home.send(embed=embed)
