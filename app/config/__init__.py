import os
import sys
import app.config.settings

# create settings object corresponding to specified env
APP_ENV = os.environ.get('FLASK_ENV', 'Base')
_current = getattr(sys.modules['app.config.settings'], '{0}Config'.format(APP_ENV))()

# copy attributes to the module for convenience
for atr in [f for f in dir(_current) if not '__' in f]:
    # environment can override anything
    val = os.environ.get(atr, getattr(_current, atr))
    setattr(sys.modules[__name__], atr, val)
