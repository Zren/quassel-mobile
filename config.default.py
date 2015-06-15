import os

r"""
quassel_db_uri
    Sqlite: (Windows) CurrentUser: sqlite:///C:\Users\Admin\AppData\Roaming\quassel-irc.org\quassel-storage.sqlite
    Sqlite: (Windows) NetworkService: sqlite:///C:\Windows\ServiceProfiles\NetworkService\AppData\Roaming\quassel-irc.org\quassel-storage.sqlite
    Postgres:
        Requires pg8000 `pip install pg8000`
"""
quassel_db_uri = 'sqlite:///' + os.environ.get('APPDATA') + r'\quassel-irc.org\quassel-storage.sqlite'
# quassel_db_uri = 'sqlite:///' + r'C:\Windows\ServiceProfiles\NetworkService\AppData\Roaming\quassel-irc.org\quassel-storage.sqlite'
# quassel_db_uri = 'postgresql+pg8000://quassel:password@localhost/quassel'

"""
Flask
"""
session_secret = 'ksme4$dfgj(@Mdsafdks$$#KDasdfgdff'
host = '0.0.0.0'
port = 3000
debug = False
