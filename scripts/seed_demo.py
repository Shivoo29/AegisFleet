#!/usr/bin/env python3
"""Wipe and seed Riya's demo story. From backend/: PYTHONPATH=. python ../scripts/seed_demo.py"""
from app.demo import reset_db, seed

reset_db()
seed()
print("demo seeded")
