# BrickTok - Instructions pour créer un exécutable

## Méthode 1 : Utiliser le script automatique (RECOMMANDÉ)

1. Ouvrez PowerShell dans le dossier du projet
2. Exécutez :
   ```powershell
   .\build_exe.ps1
   ```
3. Attendez la compilation (quelques minutes)
4. Votre jeu sera dans : `dist\BrickTok.exe`

## Méthode 2 : Commandes manuelles

Si le script ne fonctionne pas, exécutez ces commandes une par une :

```powershell
# 1. Activer l'environnement virtuel
.\.venv\Scripts\Activate.ps1

# 2. Installer PyInstaller
pip install pyinstaller

# 3. Créer l'exécutable
pyinstaller --onefile --windowed --name BrickTok --add-data "assets;assets" --add-data "levels;levels" main.py
```

## Distribution du jeu

Une fois l'exécutable créé :

### Option A : Fichier unique (plus simple)
- Prenez `dist\BrickTok.exe`
- Le fichier contient tout le jeu
- ⚠️ **IMPORTANT** : Vous devez copier le dossier `assets` à côté de l'exe

### Option B : Dossier complet (recommandé)
- Copiez tout le dossier `dist`
- Partagez ce dossier
- Double-cliquez sur `BrickTok.exe` pour jouer

## Structure finale pour distribution

```
BrickTok/
├── BrickTok.exe       <- Le jeu
├── assets/            <- Nécessaire !
│   ├── fonts/
│   ├── images/
│   ├── sounds/
│   └── sprites/
└── levels/            <- Nécessaire !
```

## Options avancées

### Ajouter une icône
Si vous avez un fichier `.ico` :
```powershell
pyinstaller --onefile --windowed --icon=icon.ico --name BrickTok --add-data "assets;assets" main.py
```

### Créer un dossier au lieu d'un seul fichier (démarrage plus rapide)
```powershell
pyinstaller --windowed --name BrickTok --add-data "assets;assets" --add-data "levels;levels" main.py
```

## Résolution de problèmes

### "pyinstaller n'est pas reconnu"
```powershell
pip install pyinstaller
```

### "Assets not found"
Assurez-vous que le dossier `assets` est à côté de l'exe

### Le jeu ne se lance pas
- Testez d'abord avec : `pyinstaller --onedir` (sans --onefile)
- Vérifiez les erreurs dans `build\BrickTok\warn-BrickTok.txt`

### Antivirus bloque l'exe
- C'est normal pour les nouveaux .exe Python
- Ajoutez une exception dans votre antivirus
- Ou utilisez `--onedir` au lieu de `--onefile`

## Nettoyage

Pour supprimer les fichiers de build :
```powershell
Remove-Item -Recurse -Force build, dist, *.spec
```
