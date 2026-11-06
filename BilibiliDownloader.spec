# -*- mode: python ; coding: utf-8 -*-

import re
import sys
from pathlib import Path

from bilibili_downloader import __version__

if sys.platform == 'darwin':
    app_icon = 'bilibili_downloader/gui/assets/app_icon.icns'
elif sys.platform == 'win32':
    app_icon = 'bilibili_downloader/gui/assets/app_icon.ico'
else:
    app_icon = 'bilibili_downloader/gui/assets/app_icon.png'

a = Analysis(
    ['bilibili_downloader/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[('bilibili_downloader/gui/assets', 'bilibili_downloader/gui/assets')],
    hiddenimports=[],
    hookspath=['packaging_hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['numpy'],
    noarchive=False,
    optimize=0,
)
if sys.platform == 'win32':
    import PySide6

    # Qt uses Windows' system ICU. A different icuuc.dll on the build host's
    # PATH (for example Poppler's) has incompatible exports and breaks QtCore.
    a.binaries = [
        entry for entry in a.binaries
        if not re.fullmatch(r'icuuc\.dll|icudt\d+\.dll', Path(entry[0]).name.lower())
    ]
    # Match the runtime used by Qt in this payload, rather than an older copy
    # from the build machine's Python installation.
    runtime_names = ('VCRUNTIME140.dll', 'VCRUNTIME140_1.dll')
    a.binaries = [entry for entry in a.binaries if entry[0].upper() not in {
        name.upper() for name in runtime_names
    }]
    qt_root = Path(PySide6.__file__).parent
    a.binaries += [(name, str(qt_root / name), 'BINARY') for name in runtime_names]
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BilibiliDownloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=app_icon,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BilibiliDownloader',
)

if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='BilibiliDownloader.app',
        icon=app_icon,
        bundle_identifier='com.itsvicoc.bilibili-downloader',
        info_plist={
            'CFBundleDisplayName': 'BiliFlow',
            'CFBundleName': 'BiliFlow',
            'CFBundleShortVersionString': __version__,
            'CFBundleVersion': __version__,
            'NSHighResolutionCapable': True,
        },
    )
