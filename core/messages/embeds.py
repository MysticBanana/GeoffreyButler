import discord
from . import message_config


def build_embed(**kwargs) -> discord.Embed:
    config = kwargs.get("config", message_config.MessageConfig)

    title = kwargs.get("title", None)
    description = kwargs.get("description", None)
    color = kwargs.get("color", message_config.get_color(config.DEFAULT_COLOR.value))
    url = kwargs.get("url", None)
    author: discord.Member = kwargs.get("author", "")
    display_author_name = kwargs.get("author_name", "")  # replace the name of the other with a given custom name
    author_img = kwargs.get("author_img")

    if author_img is None:
        if author != "":
            author_img = author.avater_url
        else:
            author_img = None

    footer = kwargs.get("footer", None)
    footer_img = kwargs.get("footer_img", None)
    timestamp = kwargs.get("timestamp", None)
    fields = kwargs.get("fields", [])  # list of dicts {name=name, value=value, inline=bool}
    thumbnail = kwargs.get("thumbnail", "")

    e = discord.Embed()
    e.title = title
    e.description = description
    e.colour = color
    e.url = url

    e.set_author(name=(display_author_name if display_author_name else author), icon_url=author_img)
    e.set_footer(text=footer, icon_url=footer_img)
    e.set_thumbnail(url=thumbnail)
    e.timestamp = timestamp

    if fields:
        for field in fields:
            e.add_field(**field)

    return e
