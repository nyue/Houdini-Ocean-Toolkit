#
# A simple launcher for the pavement script using paver-minilib.
#
import os,sys

# We force people to use hython on the Windows platform so we have an
# easy way of determining if we are running a 32 or 64 bit version of
# houdini.
if sys.platform == 'win32':
    if 'hython' not in sys.executable:
        print 'Sorry, this script can only be run by hython on Windows.'
        sys.exit(1)
    
if os.path.exists("paver-minilib.zip"):
    import sys
    sys.path.insert(0, "paver-minilib.zip")

import paver.tasks
paver.tasks.main()
