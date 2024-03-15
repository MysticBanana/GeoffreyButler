# GeoffreyButler
Simple extendable Discord bot using the Discord.py (v2.0) library.

**The bot is still work in progress and much features/plugins will be added in near future.**

## Features
 * dynamic loading of  extensions/plugins from defined folder
 * data stored in a database via sqlalchemy
 * tracking activity of users by xp
 * custom permissions (add command permissions to server roles)
 
## Available plugins
 * Musicbot (outdated)
 * Polls (role polls, polls, short polls)
 * Activity Tracking and leveling

# How to use
All configs are made in the `conf.ini`. To customize them create a `conf.ini.local` and specify all
variables you want to overwrite (e.g. your token). If the discord server doesn't get saved in the database
automatically you can run the command `<prefix>register`.

## Plugins
To write your own plugin just copy the `sample-ext` package and rename it. Add your package name in
the `conf.ini.local`. Now your plugin should be loaded.

Note:
 * Import `from core.botbase import Bot` to access the client instance
 * Import `from data import db_utils` if you want to submit database requests
 * Use `send` and `respond` function from `core.messages` to send messages or use bot.responses to send a more complex 
message