# GeoffreyButler
Simple framework build on top of the Discord.py library.

 * automatically loads extensions/plugins from defined folder
 * config manager to access and store structured server specific data

# How to use

All configurations are stored in the `conf.ini`. To use them you have to create a `conf.ini.local` and specify all
variables you want to overwrite for example your token.

A configuration file for every server gets created automatically after the bot receives a message. Every Discord-Server
uses an own `ConfigLoader` that is stored in a dictionary `SERVERS` (access with server-id). To access the saved data 
you can treat the `ConfigLoader` as a dictionary and might call `flush` at the end to write the data in the file.