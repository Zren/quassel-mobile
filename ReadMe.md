# Quassel Mobile

A simple webapp to read quassel's recent logs targeted for mobile use. Written in Python 3.x. Uses flask for the webserver and sqlalchemy to query sql. The clientside currently uses Ractive, jQuery and Bootstrap.

# Screenshots

[![](http://i.imgur.com/pyVVGojl.png)](http://i.imgur.com/pyVVGoj.png) [![](http://i.imgur.com/9hKORR5l.png)](http://i.imgur.com/9hKORR5.png) [![](http://i.imgur.com/9kddHU6l.png)](http://i.imgur.com/9kddHU6.png) 

## Install

`git clone git@github.com:Zren/quassel-mobile.git`

Run `install.sh` to install the requirements. A new file called `config.py` will be created (a copy of `config.defualt.py`). Edit your `session_secret` to something random, and `host` and `port` if necessary.

Then run `run.sh` and open http://localhost:3000/.

### Optionally

* Port forward so you can visit the website on your phone (since it won't be connected to your LAN).
* When visiting the site in Chrome (Android), open the menu and click "Add to Home screen" to browse like a regular app without the address bar.

## TODO

* Support QuasselCores that store `quaseluser.password` as something other than SHA1. Currently supports QuasselCore v10.
    * Sha512 seen in v11, with a salt split from the hash with a `:`.
    * A whole new column is added in v12 to specify which encoding.
* Support SSL?
* Load more when scrolled to the top.
    * During `on('scroll')` check the `scrollTop`. Add a `&before=oldestFetchedMessageId` to the message request, and set `messagesContainer.scrollTop` to `.scrollHeight` after adding the new messages.
* Geastures using Hammer.js (or it's Ractive equivalent): Swipe up (when at the bottom of the backlog) == reload/fetch more. Swipe right/left (open networks list).
* Format message types (Eg: message.type == Action senderColumn = `*` contentsColumn = `Zren slaps ____`).
