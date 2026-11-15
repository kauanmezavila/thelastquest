from PyInstaller.utils.hooks import collect_all

pygame_datas, pygame_binaries, pygame_hidden = collect_all("pygame")

a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=pygame_binaries,
    datas=pygame_datas + [
        ("assets", "assets"),
    ],
    hiddenimports=pygame_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="TheLastQuest",
    debug=False,
    strip=False,
    upx=True,
    console=True,
)
