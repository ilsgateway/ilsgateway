#!/usr/bin/env python
from django.core.management import execute_manager
import sys

try:
	import settings # Assumed to be in the same directory.
except ImportError:
	sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r." % __file__)	
	sys.exit(1)


if __name__ == "__main__":
	import os
	project_root = os.path.abspath(os.path.dirname(__file__))
	for dir in ["lib", "apps"]:
		path = os.path.join(project_root, dir)
		sys.path.insert(0, path)
	sys.path.insert(0, project_root)
	execute_manager(settings)