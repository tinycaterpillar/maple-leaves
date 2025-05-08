# -*- mode: python ; coding: utf-8 -*-

import os
import wordfreq  # wordfreq 경로 추적용

# 📌 wordfreq의 data 디렉토리 경로 자동 추적
wordfreq_data_dir = os.path.join(os.path.dirname(wordfreq.__file__), 'data')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[(wordfreq_data_dir, 'wordfreq/data')],  # ✅ 데이터 포함
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=True,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='wordbook_debug',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # ✅ 콘솔창 띄우기 (디버깅용)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='wordbook_debug',
)
