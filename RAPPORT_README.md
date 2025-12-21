# Rapport Technique LaTeX

Ce dossier contient le rapport technique complet du projet en format LaTeX.

## Fichiers

- `rapport_technique.tex` - Document LaTeX source
- `compile_report.sh` - Script de compilation automatique
- `rapport_technique.pdf` - PDF généré (après compilation)

## Compilation du Rapport

### Option 1: Script Automatique (Recommandé)

```bash
./compile_report.sh
```

Le script effectue automatiquement:
- Vérification de l'installation LaTeX
- Trois compilations successives (pour la table des matières et références)
- Nettoyage des fichiers temporaires
- Ouverture du PDF généré

### Option 2: Compilation Manuelle

```bash
# Compiler trois fois pour générer la table des matières
pdflatex rapport_technique.tex
pdflatex rapport_technique.tex
pdflatex rapport_technique.tex

# Ouvrir le PDF
open rapport_technique.pdf
```

## Installation de LaTeX

### macOS

```bash
# Avec Homebrew (recommandé)
brew install --cask mactex

# Ou télécharger depuis
# https://www.tug.org/mactex/
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install texlive-full
```

### Windows

Télécharger MiKTeX depuis: https://miktex.org/download

## Contenu du Rapport

Le rapport technique comprend:

1. **Introduction**
   - Contexte du projet
   - Objectifs
   - Périmètre

2. **Architecture Technique**
   - Stack technologique
   - Architecture en couches
   - Diagrammes

3. **Modèle de Données**
   - Schéma relationnel
   - Contraintes d'intégrité
   - Vues analytiques

4. **Algorithme de Planification**
   - Principe de fonctionnement
   - Contraintes respectées
   - Complexité algorithmique

5. **Implémentation**
   - Module de base de données
   - Vérificateur de contraintes
   - Interface utilisateur

6. **Tests et Validation**
   - Méthodologie de test
   - Résultats des tests (9/9 réussis)
   - Tests de performance

7. **Résultats et Métriques**
   - Données du système
   - Performance de planification
   - Analyse des conflits

8. **Fonctionnalités Implémentées**
   - Gestion des examens
   - Analyses et statistiques
   - Interfaces utilisateur

9. **Optimisations et Améliorations**
   - Optimisations réalisées
   - Améliorations futures

10. **Guide d'Utilisation**
    - Installation
    - Utilisation de l'interface

11. **Conclusion**
    - Objectifs atteints
    - Points forts
    - Limitations et perspectives

12. **Annexes**
    - Structure du projet
    - Commandes utiles
    - Références

## Caractéristiques du Rapport

- **Format**: A4, 12pt
- **Langue**: Français
- **Pages**: ~25 pages
- **Sections**: 11 sections principales + annexes
- **Tableaux**: 10+ tableaux de données
- **Code**: Exemples Python et SQL avec coloration syntaxique
- **Graphiques**: Métriques et statistiques
- **Références**: Liens hypertexte vers documentation

## Packages LaTeX Utilisés

- `babel` - Support français
- `geometry` - Marges et mise en page
- `listings` - Coloration syntaxique du code
- `hyperref` - Liens hypertexte
- `booktabs` - Tableaux professionnels
- `tcolorbox` - Encadrés colorés
- `fancyhdr` - En-têtes et pieds de page

## Personnalisation

Pour modifier le rapport:

1. Ouvrir `rapport_technique.tex` dans un éditeur LaTeX
2. Modifier le contenu souhaité
3. Recompiler avec `./compile_report.sh`

### Éditeurs LaTeX Recommandés

- **TeXShop** (macOS) - Inclus avec MacTeX
- **Overleaf** (Web) - https://www.overleaf.com
- **TeXstudio** (Multi-plateforme) - https://www.texstudio.org
- **VS Code** avec extension LaTeX Workshop

## Dépannage

### Erreur: "pdflatex: command not found"

LaTeX n'est pas installé. Voir section "Installation de LaTeX".

### Erreur: "! LaTeX Error: File 'xxx.sty' not found"

Un package LaTeX est manquant. Installer la distribution complète:
```bash
brew install --cask mactex  # macOS
```

### Le PDF n'est pas généré

1. Vérifier les erreurs dans `rapport_technique.log`
2. Compiler manuellement pour voir les messages d'erreur:
   ```bash
   pdflatex rapport_technique.tex
   ```

### La table des matières est vide

Compiler le document au moins deux fois:
```bash
pdflatex rapport_technique.tex
pdflatex rapport_technique.tex
```

## Export vers d'autres formats

### Word (DOCX)

```bash
# Installer pandoc
brew install pandoc

# Convertir
pandoc rapport_technique.tex -o rapport_technique.docx
```

### HTML

```bash
# Avec pandoc
pandoc rapport_technique.tex -o rapport_technique.html --standalone

# Ou avec htlatex
htlatex rapport_technique.tex
```

## Support

Pour toute question sur le rapport:
- Consulter la documentation LaTeX: https://www.latex-project.org/help/documentation/
- Forum TeX StackExchange: https://tex.stackexchange.com/

---

**Dernière mise à jour**: Décembre 2024
