# GeoffreyButler
Simple extendable Discord bot using the Discord.py (v2.0) library.

**The bot is still work in progress and much features/plugins will be added in near future.**

# Features
 * dynamic loading of  extensions/plugins from defined folder
 * config manager to access and store structured server specific data
 * dynamic config management for each extension/plugin
 * global audio controller to access from multiple plugins at the same time
 
# Plugins
 * Musicbot (works but some features are missing)
 * basic role poll (editing and other features coming soon)

# How to use
All configs are made in the `conf.ini`. To customize them create a `conf.ini.local` and specify all
variables you want to overwrite (e.g. your token).

The config file for each server gets created dynamically. Ever server gets it own `ConfigHandler` (access by server-id).
To work with the data you can treat the `ConfigLoader` as a `dictionary`. If automatic saving is disabled you should
 call `flush` after modifying.
 