
import pathlib
import shutil
import os

print("Cleaning up __pycache__...")
count = 0
for p in pathlib.Path('.').rglob('__pycache__'):
    if p.is_dir():
        try:
            shutil.rmtree(p)
            print(f"Deleted: {p}")
            count += 1
        except Exception as e:
            print(f"Failed to delete {p}: {e}")

print(f"Cleanup complete. Removed {count} directories.")
