#!/usr/bin/env python

import subprocess
# Format used for representing invalid unicode characters
INVALID_UNICODE_CHAR_FORMAT = r"\x%02x"

IS_WIN = subprocess.mswindows

# Selectable list of plugins
LIST_PLUGINS = ["subdomain", "find_service", "whatcms", "fuzz"]