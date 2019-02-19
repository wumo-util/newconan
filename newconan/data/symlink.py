import os, sys, platform
from os.path import join, abspath
import pathlib

try:
  pardir = abspath(join(sys.argv[2], os.pardir))
  pathlib.Path(pardir).mkdir(parents=True, exist_ok=True)
  if platform.system() == 'Windows':
    import _winapi
    _winapi.CreateJunction(sys.argv[1], sys.argv[2])
  else:
    os.symlink(sys.argv[1], sys.argv[2])
  print(f"Create Symlink {sys.argv[2]} -> {sys.argv[1]}")
except FileExistsError:
  print(f"Symlink already exists: {sys.argv[2]}")
except Exception as e:
  print(f"{sys.argv}\n{e}")