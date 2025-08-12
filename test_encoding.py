#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import locale

print("Python version:", sys.version)
print("Default encoding:", sys.getdefaultencoding())
print("Stdout encoding:", sys.stdout.encoding)
print("Locale:", locale.getpreferredencoding())

try:
    print("Testing Cyrillic: Тест")
    print("Testing emoji: 📋")
    print("All encoding tests passed!")
except UnicodeEncodeError as e:
    print(f"Encoding error: {e}")
