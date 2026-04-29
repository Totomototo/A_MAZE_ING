*This project has been created as part of the 42 curriculum by vavegee, tbenavid.*

# A-Maze-ing

## Description

A-Maze-ing est un projet Python dont le but est de générer un labyrinthe aléatoire à partir d’un fichier de configuration, de le résoudre, de l’afficher dans le terminal, puis de l’écrire dans un fichier de sortie au format demandé par le sujet.

Le projet contient :

- un générateur de labyrinthe ;
- un parseur de fichier de configuration ;
- un solveur pour trouver le plus court chemin ;
- un affichage ASCII interactif ;
- un package Python réutilisable nommé `mazegen`.

Le labyrinthe est composé de cellules. Chaque cellule peut avoir des murs au nord, à l’est, au sud et à l’ouest. Ces murs sont encodés avec des bits, puis exportés sous forme de chiffres hexadécimaux.

Le projet supporte aussi la reproductibilité avec une seed. Avec la même configuration et la même seed, le même labyrinthe peut être généré à nouveau.

---

## Instructions

### Prérequis

Le projet est écrit en Python 3.10 ou supérieur.

Pour installer les dépendances de développement :

```bash
make install
```

Cette commande crée un environnement virtuel dans `.venv`, met à jour `pip`, `setuptools` et `wheel`, puis installe les dépendances listées dans `requirements.txt`.

Pour activer manuellement l’environnement virtuel :

```bash
source .venv/bin/activate
```

L’activation manuelle est optionnelle, car les commandes du `Makefile` utilisent directement l’environnement virtuel.

### Lancer le projet

Le sujet demande de lancer le programme avec :

```bash
python3 a_maze_ing.py config.txt
```

Il est aussi possible d’utiliser :

```bash
make run
```

Par défaut, `make run` utilise le fichier :

```text
config.txt
```

Pour utiliser un autre fichier de configuration :

```bash
make run CONFIG_FILE=my_config.txt
```

### Debug

```bash
make debug
```

### Nettoyage

```bash
make clean
```

Cette commande supprime les fichiers temporaires Python, les caches, les dossiers de build, les fichiers de distribution et les dossiers `egg-info`.

### Lint

```bash
make lint
```

Cette commande exécute :

```bash
flake8 .
mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
```

Une version stricte est aussi disponible :

```bash
make lint-strict
```

### Construire le package réutilisable

```bash
make build
```

Cette commande génère les fichiers du package dans le dossier `dist/`, par exemple :

```text
dist/mazegen-1.0.0-py3-none-any.whl
dist/mazegen-1.0.0.tar.gz
```

Pour installer localement le package généré :

```bash
make package-install
```

---

## Fichier de configuration

Le programme prend un fichier de configuration en argument.

Exemple :

```ini
# Configuration par défaut pour A-Maze-ing

WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze_output.txt
PERFECT=True
SEED=42
DISPLAY=True
```

### Clés obligatoires

| Clé | Description | Exemple |
|---|---|---|
| `WIDTH` | Largeur du labyrinthe, en nombre de cellules | `WIDTH=20` |
| `HEIGHT` | Hauteur du labyrinthe, en nombre de cellules | `HEIGHT=15` |
| `ENTRY` | Coordonnées de l’entrée au format `x,y` | `ENTRY=0,0` |
| `EXIT` | Coordonnées de la sortie au format `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | Nom du fichier de sortie | `OUTPUT_FILE=maze_output.txt` |
| `PERFECT` | Indique si le labyrinthe doit être parfait | `PERFECT=True` |

### Clés optionnelles

| Clé | Description | Exemple |
|---|---|---|
| `SEED` | Seed utilisée pour rendre la génération reproductible | `SEED=42` |
| `DISPLAY` | Active ou désactive l’interface ASCII | `DISPLAY=True` |

### Règles du fichier de configuration

- Une seule paire `KEY=VALUE` par ligne.
- Les lignes vides sont ignorées.
- Les lignes qui commencent par `#` sont ignorées.
- `WIDTH` et `HEIGHT` doivent être des entiers positifs.
- `ENTRY` et `EXIT` doivent être dans les limites du labyrinthe.
- `ENTRY` et `EXIT` doivent être différentes.
- `PERFECT` et `DISPLAY` doivent valoir `True` ou `False`.
- Si `SEED` est fournie, la même configuration avec la même seed produit le même labyrinthe.

---

## Format du fichier de sortie

Le labyrinthe est écrit ligne par ligne, avec un chiffre hexadécimal par cellule.

Chaque bit représente un mur fermé :

| Bit | Direction |
|---|---|
| `0` | Nord |
| `1` | Est |
| `2` | Sud |
| `3` | Ouest |

Exemples :

- `3` signifie que les murs nord et est sont fermés.
- `A` signifie que les murs est et ouest sont fermés.

Après la grille du labyrinthe, le fichier contient une ligne vide, puis :

```text
entry_x,entry_y
exit_x,exit_y
shortest_path
```

Exemple :

```text
BDA9...
F81C...

0,0
19,14
EESSWWNNE...
```

Le plus court chemin est écrit avec les lettres :

```text
N E S W
```

---

## Algorithme de génération du labyrinthe

Le labyrinthe est généré avec l’algorithme du **recursive backtracker**, implémenté avec une pile explicite.

L’algorithme commence à partir de la cellule d’entrée, la marque comme visitée, puis répète les étapes suivantes :

1. récupérer les voisins non visités ;
2. choisir aléatoirement un voisin ;
3. supprimer le mur entre la cellule actuelle et ce voisin ;
4. avancer vers ce voisin ;
5. revenir en arrière quand il n’y a plus de voisin disponible.

Cet algorithme permet de générer un labyrinthe entièrement connecté.

Lorsque `PERFECT=True`, le labyrinthe contient un seul chemin possible entre deux cellules normales, à l’exception des cellules fermées utilisées pour dessiner le motif `42`.

Lorsque `PERFECT=False`, des murs supplémentaires sont ouverts après la génération principale afin de créer des boucles. Le générateur vérifie que ces ouvertures ne créent pas de grande zone ouverte interdite de type `3x3`.

---

## Pourquoi cet algorithme a été choisi

Le recursive backtracker a été choisi parce qu’il est :

- simple à comprendre ;
- simple à expliquer en évaluation ;
- adapté à la génération de labyrinthes parfaits ;
- facile à implémenter avec une pile ;
- compatible avec une génération reproductible grâce à une seed ;
- adapté à la représentation par cellules et murs demandée par le sujet.

Cet algorithme permet aussi de travailler des notions importantes comme les graphes, la récursivité logique, le backtracking, les piles et l’aléatoire contrôlé.

---

## Solveur

Le labyrinthe est résolu avec un **Breadth-First Search**, aussi appelé BFS.

Le BFS a été choisi parce que le sujet demande d’écrire le plus court chemin valide entre l’entrée et la sortie dans le fichier de sortie.

Le BFS explore le labyrinthe niveau par niveau :

1. il commence à l’entrée ;
2. il explore toutes les cellules accessibles à distance 1 ;
3. puis toutes les cellules accessibles à distance 2 ;
4. et ainsi de suite jusqu’à atteindre la sortie.

La première fois que le BFS atteint la sortie, le chemin trouvé est forcément le plus court.

Le chemin final est stocké sous forme de chaîne de caractères avec les directions :

```text
N E S W
```

Exemple :

```text
EESSWN
```

Ce chemin est utilisé dans le fichier de sortie et dans l’affichage ASCII.

---

## Affichage visuel

Le projet propose un affichage ASCII interactif dans le terminal.

L’affichage montre :

- les murs du labyrinthe ;
- l’entrée ;
- la sortie ;
- le motif `42` ;
- le plus court chemin ;
- les couleurs des murs.

L’interface permet :

```text
1 - Afficher / cacher le plus court chemin
2 - Regénérer un labyrinthe
3 - Changer la couleur des murs
4 - Afficher le plus court chemin
5 - Quitter
```

Le chemin peut être affiché avec des flèches :

```text
↑ → ↓ ←
```

Ce choix rend le chemin plus lisible que de simples points.

Le projet n’utilise pas MiniLibX. Le sujet autorise soit un affichage ASCII dans le terminal, soit un affichage graphique avec MLX. L’affichage ASCII a été choisi pour sa simplicité, sa portabilité et sa facilité de test.

---

## Reproductibilité avec la seed

Le labyrinthe est généré aléatoirement, mais la reproductibilité est assurée grâce à la clé `SEED`.

Exemple :

```ini
SEED=42
```

Avec la même configuration et la même seed, le générateur produit le même labyrinthe.

Si la seed est absente ou définie à `None`, le labyrinthe peut être différent à chaque exécution.

---

## Package réutilisable

La partie réutilisable du projet est le module de génération du labyrinthe.

Elle est disponible sous forme de package Python nommé :

```text
mazegen
```

Le package contient :

- `Cell`
- `Maze`
- `MazeGenerator`

Le package peut être construit avec :

```bash
make build
```

Cela génère :

```text
dist/mazegen-1.0.0-py3-none-any.whl
dist/mazegen-1.0.0.tar.gz
```

### Exemple d’utilisation

```python
from mazegen import MazeGenerator

generator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    seed=42,
    perfect=True,
)

maze = generator.generate()

for row in maze.grid:
    print("".join(cell.to_hex() for cell in row))
```

### Accès à la structure du labyrinthe

La structure générée est accessible avec :

```python
maze.grid
```

Chaque élément de la grille est une `Cell`.

Une cellule contient notamment :

```python
cell.x
cell.y
cell.walls
cell.is_42
```

La représentation hexadécimale d’une cellule peut être obtenue avec :

```python
cell.to_hex()
```

---

## Structure du projet

Exemple de structure :

```text
.
├── a_maze_ing.py
├── config_parser.py
├── config.txt
├── maze_display.py
├── maze_generator.py
├── maze_solver.py
├── Makefile
├── pyproject.toml
├── README.md
├── requirements.txt
├── mazegen/
│   ├── __init__.py
│   └── maze_generator.py
└── dist/
    ├── mazegen-1.0.0-py3-none-any.whl
    └── mazegen-1.0.0.tar.gz
```

### Rôle des fichiers principaux

| Fichier | Rôle |
|---|---|
| `a_maze_ing.py` | Point d’entrée principal du programme |
| `config_parser.py` | Lit et valide le fichier de configuration |
| `maze_generator.py` | Génère le labyrinthe |
| `maze_solver.py` | Résout le labyrinthe avec BFS |
| `maze_display.py` | Gère l’affichage ASCII et les interactions |
| `pyproject.toml` | Définit le package réutilisable |
| `Makefile` | Automatise l’installation, l’exécution, le lint, le nettoyage et le build |

---

## Organisation de l’équipe

### Membres

- `vavegee`
- `tbenavid`

### Rôles

Le travail a été réparti autour des grandes parties du projet :

- génération du labyrinthe et encodage des murs ;
- résolution du labyrinthe et gestion du plus court chemin ;
- parsing du fichier de configuration ;
- gestion des erreurs ;
- affichage ASCII interactif ;
- packaging réutilisable ;
- documentation.

Les deux membres ont participé aux tests et à la relecture afin de vérifier que le comportement final corresponde aux exigences du sujet.

### Planning initial

Le projet a été prévu en plusieurs étapes :

1. créer la structure du labyrinthe ;
2. générer un labyrinthe valide ;
3. exporter le labyrinthe au format hexadécimal ;
4. ajouter un solveur ;
5. ajouter un affichage visuel ;
6. lire un fichier de configuration ;
7. créer un package réutilisable ;
8. finaliser le Makefile et le README.

### Évolution du planning

Au début, le solveur a été pensé avec un DFS. Ensuite, le BFS a été choisi, car le sujet demande le plus court chemin.

L’affichage était d’abord un simple rendu ASCII, puis il a été amélioré avec une interface interactive, l’affichage/cachage du chemin, les couleurs et les flèches directionnelles.

Le package réutilisable a été ajouté à la fin, une fois que la génération du labyrinthe était stable.

### Ce qui a bien fonctionné

- L’encodage des murs avec des bits est simple et efficace.
- Le recursive backtracker génère correctement des labyrinthes parfaits.
- Le BFS permet d’obtenir clairement le plus court chemin.
- L’affichage ASCII est portable et facile à tester.
- La seed facilite les tests en rendant la génération reproductible.

### Ce qui pourrait être amélioré

- Ajouter plus de tests automatisés.
- Ajouter plusieurs algorithmes de génération.
- Ajouter plus d’options d’affichage.
- Éviter la duplication entre le générateur principal et le package.
- Rendre le nombre de boucles configurable quand `PERFECT=False`.

### Outils utilisés

- Python 3.10
- Makefile
- flake8
- mypy
- module Python `build`
- Git
- affichage ASCII dans le terminal

---

## Ressources

Ressources classiques liées au projet :

- Documentation Python : <https://docs.python.org/3/>
- Module `random` : <https://docs.python.org/3/library/random.html>
- Module `collections.deque` : <https://docs.python.org/3/library/collections.html#collections.deque>
- Guide du packaging Python : <https://packaging.python.org/>
- PEP 257, conventions de docstrings : <https://peps.python.org/pep-0257/>
- Documentation flake8 : <https://flake8.pycqa.org/>
- Documentation mypy : <https://mypy.readthedocs.io/>
- Algorithmes de génération de labyrinthe : <https://en.wikipedia.org/wiki/Maze_generation_algorithm>
- Breadth-first search : <https://en.wikipedia.org/wiki/Breadth-first_search>
- Depth-first search : <https://en.wikipedia.org/wiki/Depth-first_search>

### Utilisation de l’IA

L’IA a été utilisée comme outil d’aide à la compréhension et à l’organisation du projet.

Elle a servi à mieux comprendre certaines notions, notamment :

- le fonctionnement de DFS et BFS ;
- la différence entre un chemin valide et le plus court chemin ;
- l’encodage des murs avec des bits ;
- la structure d’un fichier de configuration ;
- la création d’un parseur propre ;
- l’organisation d’un projet Python ;
- la création d’un package Python réutilisable ;
- l’amélioration des explications et de la documentation.

