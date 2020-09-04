# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
from PyInstaller.utils.hooks import collect_data_files

hidden_imports = [
	'numpy',
    'ctypes',
    'ctypes.util',
    'fiona',
    'gdal',
    'geos',
    'shapely',
    'shapely.geometry',
    'pyproj',
    'rtree',
    'geopandas.datasets',
    'pytest',
    'pandas._libs.tslibs.timedeltas',
]
added_files = [('default.csv', '.'), ('infrastructures_inputs.txt', '.'), ('report_inputs.txt','.')]
added_files += collect_data_files('geopandas', subdir='datasets')

a = Analysis(['infrastructures_gui.py'],
             pathex=['C:\\Repos\\SIRM\\InfrastructureRemediation'],
             binaries=[],
             datas=added_files, 
             hiddenimports=hidden_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='infrastructures_gui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
		  


coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='infrastructures_gui')
