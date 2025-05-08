# -*- mode: python ; coding: utf-8 -*-

import os
import wordfreq  # wordfreq 경로 추적용

# 📌 wordfreq의 data 디렉토리 경로 자동 추적
wordfreq_data_dir = os.path.join(os.path.dirname(wordfreq.__file__), 'data')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[(wordfreq_data_dir, 'wordfreq/data')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,  # ✅ 아카이브 사용 (release에서는 기본값 False 유지)
    optimize=2,       # ✅ 최적화 수준 증가
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='wordbook_release',
    debug=False,                   # ✅ 디버그 비활성화
    bootloader_ignore_signals=False,
    strip=True,                    # ✅ 크기 줄이기
    upx=True,
    console=False,                 # ✅ GUI 앱이면 콘솔 숨김
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=True,
    upx=True,
    upx_exclude=[],
    name='wordbook_release',
)
