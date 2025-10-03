# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

base_dir = os.path.abspath('.')

a = Analysis(
    ['server.py'],
    pathex=[base_dir],
    binaries=[],
    datas=[
        (os.path.join(base_dir, 'gui.html'), '.'),
        (os.path.join(base_dir, 'ticket.html'), '.'),
        (os.path.join(base_dir, 'logo', 'logo.jpg'), 'logo'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TicketApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TicketApp'
)
# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['c:\\MBI_project\\server.py'],
    pathex=[],
    binaries=[],
    datas=[('c:\\MBI_project\\gui.html', '.'), ('c:\\MBI_project\\ticket.html', '.'), ('c:\\MBI_project\\logo\\logo.jpg', 'logo')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TicketApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
