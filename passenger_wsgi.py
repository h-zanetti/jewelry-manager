import sys, os

INTERP = "/root/.local/share/virtualenvs/jewelry-manager-l3Kjw74_/bin/python"

if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

from webdev.wsgi import application