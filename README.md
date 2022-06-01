# EXOGEN 1.0

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/built-with-swag.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/makes-people-smile.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/it-works-why.svg)](https://forthebadge.com)

## Générateur d'exercices et de corrections.

### Pré-requis

- Version de Python : Ce projet a été testé avec la version **3.10 de python**. Certains réglages mineurs
  pourraient s'avérés nécessaires pour la compatibilité avec des versions antérieures de python.

### Packages python utilisés

- Ce projet utilise les versions suivantes de certains packages et certaines librairies python (Les versions supérieures devraient fonctionner sans ajout particulier).
  - **PyYAML** dans sa version **_6.0_**
  - **Graphviz** dans sa version **_0.19.1_**
  - **Numpy** dans sa version **_1.22.2_**
  

### Installation et configuration de TexMaker

- Pour faire fonctionner le script python contenu dans un projet, il est nécessaire d'installer un éditeur capable d'interpreter du code python au sein de Latex.
    - Pour cela, [installer **TexMaker** ](https://www.xm1math.net/texmaker/download.html)
    - Puis [installer **MikTex**](https://miktex.org/download)
    - Ouvrir la `console MiKTeX` et cliquer sur `check for updates` pour faires les mises à jours nécessaires`.
    - Cliquer sur packages (dans la console MiKTeX) et s'assurrer que les trois packages suivants sont installés et à jour:
      - pythontex
      - pythontex__doc
      - pythontex__source

### Ajouter une commande utilisateur à TexMaker pour gérer les pdf
    
![Ajouter une commande dans TexMaker etape 1](/help/1.png?raw=true)

![Ajouter une commande dans TexMaker etape 2](/help/2.png?raw=true)

Ajouter la commande suivante dans la boîte de dialogue: (_Veillez à adapter les chemins d'accès aux spécificités de l'environnement de l'utilisateur._)

    `pdflatex --shell-escape -synctex=1 -interaction=nonstopmode %.tex|C:\Users\dieu-\AppData\Local\Programs\Python\Python310\python.exe "C:\Users\dieu-\AppData\Local\Programs\MiKTeX\scripts\pythontex\pythontex.py" %.tex|pdflatex --shell-escape -synctex=1 -interaction=nonstopmode %.tex|"C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat\Acrobat.exe" %.pdf`


![Ajouter une commande dans TexMaker etape 3](/help/3.png?raw=true)

## Démarrage

Exécuter le script Latex avec le bouton d'exécution juste à gauche de la commande que vous avez sélectionner à l'étape précédente.

![Exécution du script](/help/4.png?raw=true)


## Versions

**Dernière version stable :** Sur la branche **Master**

    
## Auteurs

* **PADONOU Dieu-Donné Isidore**
* **ATTOUMBRE Juvénal Kouadio**
* **FOFANA Mohamed**
* **CAMARA Jacob N'Kong**

## License

[![forthebadge](https://forthebadge.com/images/badges/open-source.svg)](https://forthebadge.com)  ![Badge che-lou](/help/5.png?raw=true)
