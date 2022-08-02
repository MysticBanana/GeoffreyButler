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

    audio_controller.on_next()


async def prev_command(controller: audiocontroller.Controller):
    audio_controller = controller
    audio_controller.guild.voice_client.stop()

    # need to call prev twice because on_next gets called after playing something
    audio_controller.playlist.prev()
    await audio_controller.play_wrapper(audio_controller.playlist.prev())


async def pause_command(controller: audiocontroller.Controller):
    audio_controller = controller
    voice_client = controller.guild.voice_client

    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await controller.text_channel.send("The bot is not playing anything at the moment.")


async def resume_command(controller: audiocontroller.Controller):
    audio_controller = controller
    voice_client = controller.guild.voice_client

    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await controller.text_channel.send("The bot was not playing anything before this. Use play_song command")

