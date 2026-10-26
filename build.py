"""Roda a pipeline completa de dados na ordem correta.

Uso: python build.py
"""
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
STEPS = [
    "build_classificacao.py",
    "fix_classificacao.py",
    "mei_update.py",
    "build_dados.py",
]

for step in STEPS:
    print("\n== " + step)
    subprocess.run([sys.executable, os.path.join(BASE, step)], check=True, env=ENV)
