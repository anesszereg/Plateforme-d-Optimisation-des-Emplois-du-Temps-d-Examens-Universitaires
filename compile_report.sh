#!/bin/bash

# Script de compilation du rapport LaTeX
# Génère le PDF du rapport technique

echo "============================================================"
echo "Compilation du Rapport Technique LaTeX"
echo "============================================================"

# Vérifier que pdflatex est installé
if ! command -v pdflatex &> /dev/null
then
    echo "❌ pdflatex n'est pas installé"
    echo ""
    echo "Pour installer LaTeX sur macOS:"
    echo "  brew install --cask mactex"
    echo ""
    echo "Ou télécharger depuis: https://www.tug.org/mactex/"
    exit 1
fi

echo "✅ pdflatex trouvé"
echo ""

# Nettoyer les fichiers temporaires précédents
echo "🧹 Nettoyage des fichiers temporaires..."
rm -f rapport_technique.aux rapport_technique.log rapport_technique.out rapport_technique.toc

# Première compilation
echo "📄 Première compilation..."
pdflatex -interaction=nonstopmode rapport_technique.tex > /dev/null 2>&1

# Deuxième compilation (pour la table des matières)
echo "📄 Deuxième compilation (table des matières)..."
pdflatex -interaction=nonstopmode rapport_technique.tex > /dev/null 2>&1

# Troisième compilation (pour les références croisées)
echo "📄 Troisième compilation (références)..."
pdflatex -interaction=nonstopmode rapport_technique.tex > /dev/null 2>&1

# Vérifier si le PDF a été généré
if [ -f "rapport_technique.pdf" ]; then
    echo ""
    echo "============================================================"
    echo "✅ Rapport généré avec succès!"
    echo "============================================================"
    echo ""
    echo "📄 Fichier: rapport_technique.pdf"
    echo "📊 Taille: $(du -h rapport_technique.pdf | cut -f1)"
    echo ""
    echo "Pour ouvrir le rapport:"
    echo "  open rapport_technique.pdf"
    echo ""
    
    # Nettoyer les fichiers temporaires
    echo "🧹 Nettoyage des fichiers temporaires..."
    rm -f rapport_technique.aux rapport_technique.log rapport_technique.out rapport_technique.toc
    
    echo "✅ Terminé!"
else
    echo ""
    echo "❌ Erreur lors de la génération du PDF"
    echo ""
    echo "Vérifiez le fichier de log:"
    echo "  cat rapport_technique.log"
    exit 1
fi
