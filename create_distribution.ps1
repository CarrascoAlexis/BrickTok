# Script pour créer un package de distribution propre
Write-Host "=== Création du package de distribution ===" -ForegroundColor Cyan

# Créer un dossier de distribution propre
$distFolder = "BrickTok_Distribution"
if (Test-Path $distFolder) {
    Remove-Item $distFolder -Recurse -Force
}
New-Item -ItemType Directory -Path $distFolder | Out-Null

# Copier les fichiers
Write-Host "Copie des fichiers..." -ForegroundColor Green
Copy-Item "dist\BrickTok.exe" -Destination $distFolder
Copy-Item "dist\assets" -Destination "$distFolder\assets" -Recurse
Copy-Item "dist\levels" -Destination "$distFolder\levels" -Recurse

# Créer un README pour les utilisateurs
$readmeContent = @"
# BrickTok - Jeu Arcade

## Comment jouer

1. Double-cliquez sur BrickTok.exe
2. Le jeu démarre en plein écran

## Contrôles

### Pong
- **Joueur 1 (Gauche)** : W (haut) / S (bas)
- **Joueur 2 (Droite)** : Flèches directionnelles
- **Lancer la balle** : ESPACE

### Brick Breaker
- **Joueur 1** : A (gauche) / D (droite)
- **Joueur 2** : Flèches gauche/droite
- **Lancer la balle** : ESPACE

## Configuration système

- Windows 7 ou supérieur
- Pas d'installation requise
- Aucune dépendance externe

## Crédits

Développé par carras_a
Version 1.0
"@

$readmeContent | Out-File -FilePath "$distFolder\README.txt" -Encoding UTF8

Write-Host ""
Write-Host "✅ Package créé avec succès !" -ForegroundColor Green
Write-Host ""
Write-Host "Dossier : $distFolder\" -ForegroundColor Yellow
Write-Host ""
Write-Host "Vous pouvez maintenant :" -ForegroundColor Cyan
Write-Host "  1. Compresser le dossier en ZIP" -ForegroundColor White
Write-Host "  2. Le partager avec n'importe qui" -ForegroundColor White
Write-Host "  3. Le mettre sur GitHub Releases" -ForegroundColor White

# Créer un ZIP automatiquement
if (Get-Command Compress-Archive -ErrorAction SilentlyContinue) {
    Write-Host ""
    Write-Host "Création du fichier ZIP..." -ForegroundColor Green
    $zipPath = "BrickTok_v1.0.zip"
    if (Test-Path $zipPath) {
        Remove-Item $zipPath -Force
    }
    Compress-Archive -Path $distFolder -DestinationPath $zipPath
    Write-Host "✅ Archive créée : $zipPath" -ForegroundColor Green
    Write-Host "   Taille : $([math]::Round((Get-Item $zipPath).Length / 1MB, 2)) MB" -ForegroundColor Yellow
}
