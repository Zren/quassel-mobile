# Quassel Mobile

A simplified quasselsuche meant for mobile use. Written in Python 3.x.

## Install

Run `install.sh` to install the requirements. A new file called `config.py` will be created (a copy of `config.defualt.py`). Edit your `session_secret` to something random, and `host` and `port` if necessary.

Then run `run.sh` and open http://localhost:3000/.

## TODO

* Support QuasselCores that store `quaseluser.password` as something other than SHA1. Currently supports QuasselCore v10.
* Support SSL?
