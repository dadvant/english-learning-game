#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

# שינוי לתיקיית המשחק
game_dir = r"c:\Users\ofirn\OneDrive\Documents\Private\Kids Lessons\Idan"
os.chdir(game_dir)

print(f"Working directory: {os.getcwd()}")
print("Starting English Game Server...")

# הפעלת השרת
with open('EnglishGame.py', 'r', encoding='utf-8') as f:
    exec(f.read())