#!/usr/bin/env python
import os, sys


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.settings")
    os.path.sys.path.append(os.path.join(os.path.abspath(''),'modules'))
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
