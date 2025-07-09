from typing import cast

import discord
import wavelink
import spotipy
from discord.ext import commands
from spotipy.oauth2 import SpotifyClientCredentials

import secret


class MusicCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=secret.SPOTIFY_CLIENT_ID,
                client_secret=secret.SPOTIFY_CLIENT_SECRET,
            )
        )

    @commands.command()
    async def play(self, ctx: commands.Context, *, query: str) -> None:
        """Command to play a track or playlist."""
        if not ctx.guild or not ctx.author.voice:
            return await ctx.send('🔇 You must be in a voice channel to use this command.')

        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)

        if not player:
            player = await ctx.author.voice.channel.connect(cls=wavelink.Player)

        # Detect autoplay flag.
        autoplay = '--autoplay' in query
        if autoplay:
            player.autoplay = wavelink.AutoPlayMode.enabled

        query = query.replace('--autoplay', '').strip()

        # Set home channel if not already set.
        if not hasattr(player, 'home'):
            player.home = ctx.channel
        elif player.home != ctx.channel:
            return await ctx.send(f'⚠️ I\'m already active in {player.home.mention}.')

        # Detect Spotify links.
        if 'open.spotify.com' in query:
            await ctx.send('🔄 Spotify link detected. Searching on YouTube...')

            if 'track' in query:
                track_id = query.split('track/')[1].split('?')[0]
                track_info = self.sp.track(track_id)
                query = f"ytsearch:{track_info['name']} {track_info['artists'][0]['name']}"

            elif 'playlist' in query:
                playlist_id = query.split('playlist/')[1].split('?')[0]
                playlist = self.sp.playlist_tracks(playlist_id)

                for item in playlist['items']:
                    track = item['track']
                    search_query = f"ytsearch:{track['name']} {track['artists'][0]['name']}"
                    results = await wavelink.Playable.search(search_query)
                    if results:
                        await player.queue.put_wait(results[0])

                await ctx.send(f"📑 Playlist added with {len(playlist['items'])} tracks.")

                if not player.playing:
                    await player.play(player.queue.get(), volume=30)

                return

            elif 'album' in query:
                album_id = query.split('album/')[1].split('?')[0]
                album = self.sp.album_tracks(album_id)

                for track in album['items']:
                    search_query = f"ytsearch:{track['name']} {track['artists'][0]['name']}"
                    results = await wavelink.Playable.search(search_query)
                    if results:
                        await player.queue.put_wait(results[0])

                await ctx.send(f"💿 Album added with {len(album['items'])} tracks.")

                if not player.playing:
                    await player.play(player.queue.get(), volume=30)

                return

            else:
                return await ctx.send('❌ Unsupported Spotify link.')

        # Regular search (YouTube, etc.).
        results = await wavelink.Playable.search(query)
        if not results:
            return await ctx.send('❌ No results found.')

        if isinstance(results, wavelink.Playlist):
            await player.queue.put_wait(results)
            await ctx.send(f'📑 Playlist added: `{results.name}` ({len(results)}) tracks.')
        else:
            track = results[0]
            await player.queue.put_wait(track)
            await ctx.send(f'🎵 Track added: `{track.title}`')

        if not player.playing:
            await player.play(player.queue.get(), volume=30)

    @commands.command()
    async def playnext(self, ctx: commands.Context, *, query: str) -> None:
        """Play a track as the next song in the queue."""
        if not ctx.guild or not ctx.author.voice:
            return await ctx.send('🔇 You must be in a voice channel to use this command.')

        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)

        if not player:
            player = await ctx.author.voice.channel.connect(cls=wavelink.Player)

        # Set home channel if not already set.
        if not hasattr(player, 'home'):
            player.home = ctx.channel
        elif player.home != ctx.channel:
            return await ctx.send(f'⚠️ I\'m already active in {player.home.mention}.')

        # Detect Spotify track links.
        if 'open.spotify.com' in query and 'track' in query:
            await ctx.send('🔄 Spotify track detected. Searching on YouTube...')
            track_id = query.split('track/')[1].split('?')[0]
            track_info = self.sp.track(track_id)
            query = f"ytsearch:{track_info['name']} {track_info['artists'][0]['name']}"

        # Perform search.
        results = await wavelink.Playable.search(query)
        if not results:
            return await ctx.send('❌ No results found.')

        if isinstance(results, wavelink.Playlist):
            return await ctx.send('⚠️ You can only use `playnext` with single tracks.')

        track = results[0]
        await ctx.send(f'⏭️ Track `{track.title}` will play next!')
        await player.queue.put_at(0, track)

        if not player.playing:
            await player.play(player.queue.get(), volume=30)

    @commands.command()
    async def queue(self, ctx: commands.Context) -> None:
        """Command to view the queue."""
        player = cast(wavelink.Player, ctx.voice_client)
        if not player or player.queue.is_empty:
            return await ctx.send('📭 The queue is empty.')

        upcoming = list(player.queue)
        description = ''

        for index, track in enumerate(upcoming[:10], start=1):  # Show up to 10 tracks.
            description += f'**{index}.** `{track.title}` by `{track.author}`\n'

        embed = discord.Embed(title='📜 Queue', description=description)
        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx: commands.Context) -> None:
        """Command to skip the current track."""
        player = cast(wavelink.Player, ctx.voice_client)
        if player:
            await player.skip(force=True)
            await ctx.message.add_reaction('⏭️')

    @commands.command()
    async def nightcore(self, ctx: commands.Context) -> None:
        """Command to apply nightcore effect."""
        player = cast(wavelink.Player, ctx.voice_client)
        if player:
            filters = player.filters
            filters.timescale.set(pitch=1.2, speed=1.2, rate=1)
            await player.set_filters(filters)
            await ctx.message.add_reaction('🌙')

    @commands.command(aliases=['pause', 'resume'])
    async def toggle(self, ctx: commands.Context) -> None:
        """Command to toggle pause/resume."""
        player = cast(wavelink.Player, ctx.voice_client)
        if player:
            await player.pause(not player.paused)
            await ctx.message.add_reaction('⏯️')

    @commands.command()
    async def volume(self, ctx: commands.Context, value: int) -> None:
        """Command to set the volume (0-100)."""
        player = cast(wavelink.Player, ctx.voice_client)
        if player:
            await player.set_volume(value)
            await ctx.message.add_reaction('🔊')

    @commands.command(aliases=['dc'])
    async def disconnect(self, ctx: commands.Context) -> None:
        """Command to disconnect the bot from the voice channel."""
        player = cast(wavelink.Player, ctx.voice_client)
        if player:
            await player.disconnect()
            await ctx.message.add_reaction('👋')


async def setup(bot: commands.Bot):
    await bot.add_cog(MusicCommands(bot))
