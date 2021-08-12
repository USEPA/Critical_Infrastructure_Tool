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
    'matplotlib',
    'pyproj',
     'scipy',

    'palettable',
    'rtree',
    'pytest',
    'pandas._libs.tslibs.timedeltas',
     'statsmodels.tsa.statespace._kalman_initialization',
     'statsmodels.tsa.statespace._kalman_filter',
    'statsmodels.tsa.statespace._kalman_smoother',
     'statsmodels.tsa.statespace._representation',
      'statsmodels.tsa.statespace._simulation_smoother',
    'statsmodels.tsa.statespace._statespace',
    'statsmodels.tsa.statespace._tools',
    'statsmodels.tsa.statespace._filters._conventional',
    'statsmodels.tsa.statespace._filters._inversions',
    'statsmodels.tsa.statespace._filters._univariate',
    'statsmodels.tsa.statespace._filters._univariate_diffuse',
    'statsmodels.tsa.statespace._smoothers._alternative',
   'statsmodels.tsa.statespace._smoothers._classical',
   'statsmodels.tsa.statespace._smoothers._conventional',
   'statsmodels.tsa.statespace._smoothers._univariate',
   'statsmodels.tsa.statespace._smoothers._univariate_diffuse'
]
added_files = [('default.csv', '.'),('C:\\REPOS2\\Contaminated','Contaminated\\') ,('infrastructures_inputs.txt', '.'),('C:\\REPOS2\\Sensitivity Images','Sensitivity Images\\'),('C:\\REPOS2\\Sensitivity','Sensitivity\\'),('report_inputs.txt','.'), ('DefineScenario.xlsx','.'),  ("C:\\REPOS2\\dist\\sensitivity_GUI", "."), ('final_pdf.py','.'), ('Battelle.EPA.WideAreaDecon.Launcher.exe','.'),('Battelle.Native.External.Rmath.dll','.'),('Battelle.RiskAssessment.Common.Statistics.Native.Interface.dll','.'), ("C:\\REPOS2\\executingDirectoryPath", "executingDirectoryPath\\"),("C:\\REPOS2\\azure", "azure\\"),("C:\\REPOS2\\Azure-ttk-theme-main", "Azure-ttk-theme-main\\"),("azure.tcl","."),("C:\\REPOS2\\palettable","palettable\\"),("C:\\REPOS2\\Affected","Affected\\"),("C:\\REPOS2\\Contaminated","Contaminated\\"),("C:\\REPOS2\\Overall","Overall\\"),("C:\\REPOS2\\JobRequest.json","."),("C:\\REPOS2\\SIRMResults.json",".")]

a = Analysis(['infrastructures_gui.py'],
             pathex=['C:\\REPOS2'],
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
