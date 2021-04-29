import sys, os

INTERP = "/home/wwagah/AgahSolutionsRepositories/jewelry-manager/venv/bin/python"

if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

from webdev.wsgi import application