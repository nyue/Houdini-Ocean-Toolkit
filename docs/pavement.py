#
# Automate hot build and distribution.
#
from __future__ import with_statement
import os,sys,platform
from paver.easy import *
from paver.setuputils import setup

try:
    from paver.ssh import scp
    @task
    def update_docs():
        """makes the html docs and pushes them to the web site"""
        sh('make html')
        sh('scp -r _build/html/* sf:public_html/houdini/ocean/docs')
except ImportError:
    pass


