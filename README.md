<table style="width: 600px; border: none;" cellpadding="10" align="center">
  <tr>
    <td align="center">
      <img src="images/iPOP-up_logo.png" alt="iPOP-up" style="height: 60px; width: auto;">
    </td>
    <td align="center">
      <img src="images/U-Paris-Cite-logo.png" alt="Université Paris-Cité" style="height: 60px; width: auto;">
    </td>
    <td align="center">
      <img src="images/IFB-logo.png" alt="IFB" style="height: 65px; width: auto;">
    </td>
    <td align="center">
      <img src="images/ELIXIR-France_logo.png" alt="ELIXIR-FR" style="height: 60px; width: auto;">
    </td>
    <td align="center">
      <img src="images/MERIT-logo.png" alt="MERIT" style="height: 50px; width: auto;">
    </td>
  </tr>
</table>

# Utilisation des IA génératives comme appui à la programmation et au scripting pour la biologie

## Information pratique et programme

- <https://moodle.france-bioinformatique.fr/course/view.php?id=41>
- [https://ifb-elixirfr.github.io/AI-for-scripting-bioanalysis/](https://ifb-elixirfr.github.io/AI-for-scripting-bioanalysis/)

- [https://iabioscripting.univ-lyon1.fr/](https://iabioscripting.univ-lyon1.fr/)

- [https://forms.gle/EWbjEu2gwa8JHR7r7](https://forms.gle/EWbjEu2gwa8JHR7r7)


## Organisation

Le colloque est organisé par les trois organisations suivantes :

- [Institut Français de Bioinformatique (IFB)](https://www.france-bioinformatique.fr/)
- Université Paris Cité ([plateforme iPOP-UP](https://ipop.u-paris.fr/) et [DU omiques](https://ipop.u-paris.fr/duomiques/))
- [Réseau métier en bioinformatique (MERIT)](https://merit.cnrs.fr/)

### Encadrants

- [Imane Messak](https://orcid.org/0000-0002-1654-6652) (Institut Français de Bioinformatique)
- [Thomas Denecker](https://orcid.org/0000-0003-1421-7641) (Institut Français de Bioinformatique)
- [Baptiste Rousseau](https://orcid.org/0009-0002-1723-2732) (Institut Français de Bioinformatique)

## Atelier : Développement logiciel

Dans cet atelier, nous explorerons comment l’intelligence artificielle peut devenir un véritable assistant au service du développement logiciel. À l’aide d’outils comme [Claude](https://claude.ai/), [ChatGPT](https://chat.openai.com/), [Perplexity](https://www.perplexity.ai/) ou d’autres assistants basés sur l’IA, les participant·es apprendront à :

- transformer un code généré par IA en un projet plus clair, plus robuste et plus lisible ;
- mettre en place un environnement de travail reproductible ;
- améliorer la qualité du code, sa documentation et sa maintenabilité ;
- ajouter des tests et des vérifications permettant de fiabiliser le projet ;
- appliquer des contrôles liés à la sécurité et aux dépendances ;
- structurer le projet selon les standards attendus en Python ou en R ;
- faire évoluer le dépôt GitHub vers un projet open source documenté, partageable, citable et durable.

Cet atelier a pour but de montrer comment l’IA peut accompagner les bioinformaticien·nes dans leurs projets de scripting et d’analyse, en réduisant le temps passé à déboguer et en augmentant la qualité du code produit.

## Objectif du projet

Ce dépôt est organisé autour de **deux travaux pratiques complémentaires**, un TP **Python** et un TP **R**.

L’objectif est de partir d’un **[article scientifique](10.1371/journal.pgen.1006453)** et des **données associées**, puis d’utiliser une IA générative pour produire un script capable de **recréer la figure 2A de l’article**.

Pour ce projet, les fichiers fournis dans le dossier `/data` sont :

- Article scientifique : [`article_TP_2026_bioscripting2.pdf`](./data/article_TP_2026_bioscripting2.pdf)
- Données associées : [`pgen.1006453.s002.xlsx`](./data/pgen.1006453.s002.xlsx)

Une fois le premier script obtenu avec l’aide d’une IA, l’objectif est ensuite de le retravailler pour le rendre plus propre, plus robuste, plus lisible et plus reproductible, en suivant les consignes détaillées dans chaque TP.

- Le **TP Python** consiste à mettre aux normes un script Python généré par IA en appliquant les bonnes pratiques de développement logiciel : environnement reproductible avec **Pixi**, qualité du code, typage, sécurité, tests et documentation.
- Le **TP R** consiste à restructurer un script généré par IA sous la forme d’un **package R**, avec gestion d’environnement via **renv**, documentation **roxygen2**, tests, couverture et audit qualité.

En complément, le fichier [`instruction_bonne_pratique.md`](./instruction_bonne_pratique.md) situé à la racine du projet explique comment transformer ce dépôt GitHub en un projet **open source** respectant les standards de la communauté scientifique et logicielle.

## Structure du dépôt

Le dépôt contient deux parties principales :

- **TP Python** : travail autour d’un script Python généré par IA, à rendre reproductible, maintenable, testé et documenté.
- **TP R** : travail autour d’un script généré par IA à transformer en package R propre, documenté et auditable.

## Instructions par TP

Consulter les consignes associées à chaque partie du projet :

- [Instructions du TP Python](./tp_python/instruction.md)
- [Instructions du TP R](./tp_r/instruction.md)
- [Instructions de bonnes pratiques pour le dépôt GitHub](./instruction_bonne_pratique.md)

### Instruction pour l'atelier

1. Fork le projet
2. Clone le projet
3. Ouvre le projet et commence à travailler avec ton outil IA préféré
4. Utilise l’article scientifique et le fichier de données fournis pour reproduire une figure
5. Améliore ensuite le projet en suivant les consignes du TP Python ou du TP R
6. Applique enfin les recommandations de `instruction_bonne_pratique.md` pour rendre le dépôt plus propre, réutilisable et ouvert

À la fin de la session, dans le `README` :

- Ajouter l’outil utilisé (Pleiade, ChatGPT, Perplexity, Copilot, etc.)
- Ajouter le modèle utilisé
- Ajouter le nombre de requêtes réalisées

## Contributor Code of Conduct

Veuillez noter que ce projet est publié avec le [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). En participant, vous acceptez d’en respecter les termes. Voir le fichier [CODE_OF_CONDUCT](code_of_conduct.md).

## Licence

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg

----
