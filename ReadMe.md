# Quassel Mobile

A simplified quasselsuche meant for mobile use. Written in Python 3.x.

# Screenshots

![](http://i.imgur.com/pyVVGoj.png) ![](http://i.imgur.com/9hKORR5.png)

## Install

Run `install.sh` to install the requirements. A new file called `config.py` will be created (a copy of `config.defualt.py`). Edit your `session_secret` to something random, and `host` and `port` if necessary.

Then run `run.sh` and open http://localhost:3000/.

### Optionally

* Port forward so you can visit the website on your phone (since it won't be connected to your LAN).
* When visiting the site in Chrome (Android), open the menu and click "Add to Home screen" to browse like a regular app without the address bar.

## TODO

* Support QuasselCores that store `quaseluser.password` as something other than SHA1. Currently supports QuasselCore v10.
* Support SSL?
