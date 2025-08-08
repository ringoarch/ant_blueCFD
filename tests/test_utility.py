import sys
import types
import os

# Ensure the project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Create dummy modules to satisfy imports in utility.py
Rhino = types.ModuleType('Rhino')
Rhino.RhinoDoc = types.SimpleNamespace(ActiveDoc=None)
sys.modules['Rhino'] = Rhino
sys.modules['Rhino.Geometry'] = types.ModuleType('Rhino.Geometry')

ghpythonlib = types.ModuleType('ghpythonlib')
ghpythonlib.components = types.ModuleType('components')
sys.modules['ghpythonlib'] = ghpythonlib
sys.modules['ghpythonlib.components'] = ghpythonlib.components

from utility import find_BCA_exe_file, find_exe_files


def test_find_BCA_exe_file_recursive(tmp_path, monkeypatch):
    root1 = tmp_path / 'pf'
    root2 = tmp_path / 'pf86'
    nested = root1 / 'a' / 'b'
    nested.mkdir(parents=True)
    exe = nested / 'blueCFD-AIR.exe'
    exe.write_text('')

    monkeypatch.setenv('ProgramFiles', str(root1))
    monkeypatch.setenv('ProgramFiles(x86)', str(root2))

    assert find_BCA_exe_file() == str(exe)


def test_find_exe_files_recursive(tmp_path, monkeypatch):
    root1 = tmp_path / 'pf'
    root2 = tmp_path / 'pf86'
    nested = root2 / 'ParaView' / 'deep' / 'bin'
    nested.mkdir(parents=True)
    exe = nested / 'paraview.exe'
    exe.write_text('')

    monkeypatch.setenv('ProgramFiles', str(root1))
    monkeypatch.setenv('ProgramFiles(x86)', str(root2))

    assert find_exe_files('ParaView') == str(exe)
