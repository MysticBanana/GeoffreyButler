import asyncio
import discord
from discord.ext import commands
from .utils import commands as audio_commands, models
from core import botbase, messages
from core.audio import audiocontroller
import typing
from discord import ui
# from discord.ui import Button
import traceback

from core import Geoffrey


class MusicView(ui.View):
    interaction: discord.Interaction = None
    message: discord.Message = None

    def __init__(self, bot: Geoffrey, user: typing.Union[discord.User, discord.Member], guild: discord.Guild, timeout: float = 60.0) -> None:
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.guild = guild

    async def interaction_check(self, interaction: discord.Interaction[discord.Client]) -> bool:
        if interaction.user.id != self.user.id:
            await interaction.response.send_message(
                "You cannot interact with this view.", ephemeral=True
            )
            return False
            # update the interaction attribute when a valid interaction is received
        self.interaction = interaction
        return True

    async def on_timeout(self) -> None:
        for button in self.children:
            button.disabled = True  # type: ignore
        # and update the message with the update View.
        if self.message:
            await self.message.edit(view=self)

    async def on_error(
            self, interaction: discord.Interaction[discord.Client], error: Exception,
            item: discord.ui.Item[typing.Any]
    ) -> None:
        tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        message = f"An error occurred while processing the interaction for [ActivitySetupView]:\n```py\n{tb}\n```"
        botbase.Bot._logger.get_logger("Activity").warning(message)
        await interaction.response.send_message(message, ephemeral=True)

    @discord.ui.button(emoji="⏮️")
    async def previous(self, interaction: discord.Interaction, button: discord.Button):
        audio_controller = await audiocontroller.Controller.controller_from_interaction(self.bot, interaction)
        await audio_commands.prev_command(audio_controller)

    @discord.ui.button(emoji="⏯️", style=discord.ButtonStyle.secondary)
    async def play(self, interaction: discord.Interaction, button: discord.Button):
        audio_controller = await audiocontroller.Controller.controller_from_interaction(self.bot, interaction)
        await audio_commands.pause_command(audio_controller)

    @discord.ui.button(emoji="⏭️")
    async def skip(self, interaction: discord.Interaction, button: discord.Button):
        audio_controller = await audiocontroller.Controller.controller_from_interaction(self.bot, interaction)
        await audio_commands.skip_command(audio_controller)

    @discord.ui.button(emoji="⏹️")
    async def stop(self, interaction: discord.Interaction, button: discord.Button):
        audio_controller = await audiocontroller.Controller.controller_from_interaction(self.bot, interaction)
        await audio_commands.stop_command(audio_controller)


def play_embed(title: str, duration: int, uploader: str, user: discord.User, thumnail_url: str = "",
               url: str = "") -> discord.Embed:

    embed = messages.embeds.build_embed(
        title=title,
        thumbnail=thumnail_url,
        footer=url
        # footer=f"Queued by {user.display_name}"
    )

    embed.add_field(
        name="Duration",
        value=duration,
    )

    embed.add_field(
        name="Uploader",
        value=uploader
    )

    embed.add_field(
        name="Queued by",
        value=user.display_name
    )

    return embed


class MusicCog(commands.Cog):
    def __init__(self, bot: Geoffrey):
        self.bot: Geoffrey = bot

    @commands.command(name="join", help="joins your channel")
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(name="leave", help="leaves the channel again")
    async def leave(self, ctx):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)

        await audio_controller.disconnect()

    @commands.command(name="play", help="plays music/sound from a given link or name")
    async def play(self, ctx, *, url: str):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)
        await audio_commands.play_command(audio_controller, url)

        track: models.Track = audio_controller.current_track

        await self.bot.responses.send(channel=ctx.channel, view=MusicView(
            self.bot, ctx.author, ctx.guild
        ), embed=play_embed(
            title=track.info.title,
            duration=track.convert_time(track.info.duration),
            uploader=track.info.uploader,
            user=ctx.author,
            thumnail_url=track.info.thumbnail,
            url=track.info.webpage_url
        ))

    @commands.command(name="queue", help="plays music/sound from a given link or name")
    async def queue(self, ctx, *, url: str):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)
        await audio_commands.queue_command(audio_controller, url)

    @commands.command(name="playlist", help="shows the playlist")
    async def playlist(self, ctx):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)

        # todo temp
        await self.bot.responses.send(channel=ctx.channel, content="\n".join([i.url for i in audio_controller.playlist.track_list]))

    @commands.command(name="skip", help="skips current track")
    async def skip(self, ctx):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)
        await audio_commands.skip_command(audio_controller)

    @commands.command(name="prev", help="plays the previous song")
    async def prev(self, ctx):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)
        await audio_commands.prev_command(audio_controller)

    @commands.command(name='pause', help='This command pauses the song')
    async def pause(self, ctx):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)
        await audio_commands.pause_command(audio_controller)

    @commands.command(name='resume', help='Resumes the song')
    async def resume(self, ctx):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)
        await audio_commands.resume_command(audio_controller)

    @commands.command(name='save_playlist', help='saves a list of links as playlist')
    async def save_playlist(self, ctx):
        audio_controller = await audiocontroller.Controller.controller_from_ctx(self.bot, ctx)
        # todo
        pass


async def setup(bot):
    await bot.add_cog(MusicCog(bot))
