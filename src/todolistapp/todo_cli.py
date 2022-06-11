"""
This version uses argparse instead of typer
"""

import argparse

parser = argparse.ArgumentParser(description="Accomplist: A to do list app!")

parser.add_argument("add_task", type=str, help="Adds a task to the database.")

# print("This does something.")

args = parser.parse_args()