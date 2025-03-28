from os import getenv as get_secret

if(get_secret("PIPELINE") == "production"):
    from .production import *
else:
    from .local import *