# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/MBI_project/server.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/MBI_project/gui.html', '.'), ('C:/MBI_project/ticket.html', '.'), ('C:/MBI_project/logo/logo.jpg', 'logo')],
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
