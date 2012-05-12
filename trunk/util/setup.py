# py2exe setup program
from distutils.core import setup
import pygame
import py2exe
import sys
import os
import glob, shutil
sys.argv.append("py2exe")
 
 

origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
        if os.path.basename(pathname).lower() in ("msvcp71.dll", "dwmapi.dll"):
                return 0
        return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL
 
VERSION = '1.0'
AUTHOR_NAME = 'NP4G'
AUTHOR_EMAIL = 'someone@somewhere.com'
AUTHOR_URL = "http://www.nerdparadise.com/"
PRODUCT_NAME = "PyWeek14 Entry"
SCRIPT_MAIN = 'run.py'
VERSIONSTRING = PRODUCT_NAME + " ALPHA " + VERSION
ICONFILE = 'icon.ico'
 
# Remove the build tree on exit automatically
REMOVE_BUILD_ON_EXIT = True
PYGAMEDIR = os.path.split(pygame.base.__file__)[0]
 
SDL_DLLS = glob.glob(os.path.join(PYGAMEDIR,'*.dll'))
 
if os.path.exists('dist/'): shutil.rmtree('dist/')
 
extra_files = [ ("",[ICONFILE,'icon.png','readme.txt'])]

""",
                   ("Game",glob.glob(os.path.join('Game','*.*'))),
                   ("Resources",glob.glob(os.path.join('Resources','*.*'))),
                   ("GamePlay",glob.glob(os.path.join('GamePlay','*.*'))),
                   ("Menus",glob.glob(os.path.join('Menus','*.*')))]
 """
# List of all modules to automatically exclude from distribution build
# This gets rid of extra modules that aren't necessary for proper functioning of app
# You should only put things in this list if you know exactly what you DON'T need
# This has the benefit of drastically reducing the size of your dist
 
MODULE_EXCLUDES =[
'email',
'AppKit',
'Foundation',
'bdb',
'difflib',
'tcl',
'Tkinter',
'Tkconstants',
'curses',
'distutils',
'setuptools',
'urllib',
'urllib2',
'urlparse',
'BaseHTTPServer',
'_LWPCookieJar',
'_MozillaCookieJar',
'ftplib',
'gopherlib',
'_ssl',
'htmllib',
'httplib',
'mimetools',
'mimetypes',
'rfc822',
'tty',
'webbrowser',
'socket',
'hashlib',
'base64',
'compiler',
'pydoc']
 
INCLUDE_STUFF = ['encodings',"encodings.latin_1",]
 
setup(windows=[
             {'script': SCRIPT_MAIN,
               'other_resources': [(u"VERSIONTAG",1,VERSIONSTRING)],
               'icon_resources': [(1,ICONFILE)]}],
         options = {"py2exe": {
                             "optimize": 2,
                             "includes": INCLUDE_STUFF,
                             "compressed": 1,
                             "ascii": 1,
                             "bundle_files": 2,
                             "ignores": ['tcl','AppKit','Foundation'],
                             "excludes": MODULE_EXCLUDES} },
          name = PRODUCT_NAME,
          version = VERSION,
          data_files = extra_files,
          zipfile = None,
          author = AUTHOR_NAME,
          author_email = AUTHOR_EMAIL,
          url = AUTHOR_URL,
          packages = []#'Game', 'Menus', 'GamePlay', 'Resources', 'MapGen']
          #package_dir = {'': os.path.join('Game', 'Menus', 'GamePlay', 'Resources')}
          )
 
# Create the /save folder for inclusion with the installer
shutil.copytree('images','dist/images')
shutil.copytree('data','dist/data')
shutil.copytree('sound','dist/sound')
shutil.copyfile('freesansbold.ttf', 'dist/freesansbold.ttf')

 
if os.path.exists('dist/tcl'): shutil.rmtree('dist/tcl') 
 
# Remove the build tree
if REMOVE_BUILD_ON_EXIT:
     shutil.rmtree('build/')
 
if os.path.exists('dist/tcl84.dll'): os.unlink('dist/tcl84.dll')
if os.path.exists('dist/tk84.dll'): os.unlink('dist/tk84.dll')
 
for f in SDL_DLLS:
    fname = os.path.basename(f)
    try:
        shutil.copyfile(f,os.path.join('dist',fname))
    except: pass