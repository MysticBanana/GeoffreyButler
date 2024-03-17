import discord

from . import models
from core.audio import audiocontroller


async def play_command(controller: audiocontroller.Controller, url):
    audio_controller = controller

    audio_controller.queue(track=models.Track(url=url))
    await audio_controller.play_wrapper()


async def queue_command(controller: audiocontroller.Controller, url):
    audio_controller = controller
    audio_controller.queue(track=models.Track(url=url))


async def skip_command(controller: audiocontroller.Controller):
    audio_controller = controller
    audio_controller.guild.voice_client.stop()

    # todo on next is automatically called when a track gets stopped so might call twice
    # audio_controller.on_next()
    # todo test if works correct now
    await audio_controller.play_wrapper()


async def prev_command(controller: audiocontroller.Controller):
    audio_controller = controller
    audio_controller.guild.voice_client.stop()

    # need to call prev twice because on_next gets called after playing something
    audio_controller.playlist.prev()
    # todo might need to stop the coro to avoid doing some funny stuff after finishing and skipping random
    await audio_controller.play_wrapper(audio_controller.playlist.prev())


async def pause_command(controller: audiocontroller.Controller):
    voice_client = controller.guild.voice_client

    if voice_client.is_playing():
        await voice_client.pause()
    elif voice_client.is_paused():
        await voice_client.resume()
    else:
        await controller.text_channel.send("There is no song in the playlist right now.")


async def resume_command(controller: audiocontroller.Controller):
    await pause_command(controller)


async def stop_command(controller: audiocontroller.Controller):
    audio_controller = controller
    voice_client = controller.guild.voice_client

    await audio_controller.stop_player()
    print("TODO")
