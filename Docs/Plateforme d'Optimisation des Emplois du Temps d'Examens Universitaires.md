# Plateforme d'Optimisation des Emplois du Temps d'Examens Universitaires

## Introduction

Ce projet vise à développer une plateforme d'optimisation des emplois du temps d'examens pour une université de grande envergure. Face aux défis de la planification manuelle, qui engendre des conflits et des inefficacités, ce système propose une solution automatisée basée sur une base de données relationnelle et un algorithme d'optimisation avancé. L'objectif est de générer des plannings d'examens optimaux en moins de 45 secondes, en respectant un ensemble de contraintes complexes.

## Contexte et Problématique

Dans une faculté comptant plus de 13 000 étudiants répartis sur 7 départements et plus de 200 offres de formation, la planification manuelle des examens est une tâche ardue et sujette à des erreurs. Les problèmes courants incluent la surcharge des amphithéâtres, le respect des capacités des salles (limitées à 20 étudiants en période d'examen), les chevauchements entre les emplois du temps des étudiants et des professeurs, ainsi que les contraintes liées aux équipements. Ce projet a pour ambition de concevoir une solution technologique pour automatiser et optimiser ce processus.

## Objectifs Pédagogiques

Ce projet académique a pour but de permettre aux étudiants de maîtriser plusieurs compétences clés :

*   **Modélisation relationnelle complexe** : Concevoir une base de données capable de gérer de multiples contraintes.
*   **Requêtes analytiques avancées** : Implémenter des algorithmes de détection de conflits et d'optimisation.
*   **Optimisation des performances** : Gérer efficacement des jeux de données volumineux (environ 130 000 inscriptions).
*   **Développement d'une interface web** : Créer une interface fonctionnelle pour la démonstration et l'utilisation de la plateforme.

## Acteurs et Fonctionnalités

La plateforme s'adresse à plusieurs types d'utilisateurs, chacun ayant des fonctionnalités spécifiques :

| Acteur | Fonctionnalités Principales |
| :--- | :--- |
| **Vice-doyen et Doyen** | Vue stratégique globale (occupation des amphithéâtres et salles, taux de conflits par département), validation finale de l'EDT, KPIs académiques (heures de professeurs, taux d'utilisation des salles, etc.). |
| **Administrateur des examens** | Génération automatique de l'EDT, détection des conflits, optimisation des ressources. |
| **Chef de département** | Validation de l'EDT au niveau du département, statistiques, gestion des conflits par formation. |
| **Étudiants/Professeurs** | Consultation d'un planning personnalisé (avec filtres par département ou formation). |

## Modélisation de la Base de Données

La structure de la base de données est conçue pour représenter les entités principales du système. Voici les tables principales à implémenter :

```sql
-- Structure adaptée à l'échelle réelle
departements (id, nom);
formations (id, nom, dept_id, nb_modules);
etudiants (id, nom, prenom, formation_id, promo);
modules (id, nom, credits, formation_id, pre_req_id);
lieu_examen (id, nom, capacite, type, batiment);
professeurs (id, nom, dept_id, specialite);
inscriptions (etudiant_id, module_id, note);
examens (id, module_id, prof_id, salle_id, date_heure, duree_minutes);
```

*Note : La liste des tables est un exemple et devra être adaptée en fonction de l'existant.*

## Contraintes Critiques à Modéliser

Le système doit respecter un ensemble de contraintes pour garantir la faisabilité et l'équité des emplois du temps :

*   **Étudiants** : Maximum 1 examen par jour.
*   **Professeurs** : Maximum 3 examens par jour.
*   **Salles et amphithéâtres** : Respect de la capacité réelle.
*   **Priorités** : Les examens du département sont prioritaires (un enseignant surveille en priorité les examens de son département).
*   **Équité** : Tous les enseignants doivent avoir le même nombre de surveillances.

## Technologies

La stack technologique retenue pour ce projet est la suivante :

*   **Système de Gestion de Base de Données (SGBD)** : MySQL ou PostgreSQL.
*   **Backend** : Python.
*   **Frontend** : Streamlit + Bootstrap.
*   **Optimisation** : Procédures PL/pgSQL + index partiels.

## Livrables Obligatoires

L'évaluation du projet (20/20) se fera sur la base des livrables suivants :

*   **Scripts SQL complets** : Création de la base de données et requêtes utilisées dans le dashboard.
*   **Dataset réaliste** : La base de données doit être alimentée pour pouvoir la tester.
*   **Prototype fonctionnel** : Génération de l'EDT et interface multi-départements.
*   **Rapport technique (10-15 pages PDF)** : Incluant des benchmarks de performances (temps d'exécution des requêtes).

## Informations Importantes

*   **Date de début du projet** : 20/10/2025
*   **Date de remise des liens** : 19/01/2026 23:59
*   **Travail par trinômes**
*   **Aucun retard ne sera accepté (CC2=0)**
*   **Tout plagiat sera sanctionné (CC2=0)**

## Procédure à Suivre

1.  Veuillez vous inscrire sur la liste disponible dans classroom (obligatoire).
2.  Le chef du trinôme déposera les liens sur son compte.
