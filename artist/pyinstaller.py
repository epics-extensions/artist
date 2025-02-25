import os
from pathlib import Path

import PyInstaller.__main__

HERE = Path(__file__).parent.absolute()
path_to_main = str(HERE / "artist.py")
def get_wireviz_path():
    # Obtenir le chemin de l'environnement virtuel
    env_path = os.getenv('VIRTUAL_ENV')
    # Construire le chemin complet du binaire wireviz
    return os.path.join(env_path, 'bin', 'wireviz')

def install():
    wireviz_path=get_wireviz_path()
    print(wireviz_path)
    PyInstaller.__main__.run([
        path_to_main,
        '--onefile',
        '--windowed',
        '--hidden-import',
        'epics.clibs',
        f'--add-binary={wireviz_path}:wireviz',
 
    ])