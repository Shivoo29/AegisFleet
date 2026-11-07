#!/usr/bin/env python3
"""Wipe demo data. Run from backend/: python -m scripts.reset_demo (needs PYTHONPATH=..)"""
from app.demo import reset_db

reset_db()
print("demo data wiped")
