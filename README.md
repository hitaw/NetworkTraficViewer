# LU3IN033 - Project
## Fireshark

Fireshark est un visualisateur de traffic de réseaux hors-ligne.  
Il est codé en python.  
L'interface graphique a été créée grâce à Tkinter.

Le code est composé des fichiers suivants :
- fireshark.py
- interface.py
- analyze.py
- tri.py

### fireshark.py

Crée et lance l'application à partir d'un objet Interface() dont la classe a été créée dans interface.py

### interface.py

Comme son nom l'indique, contient le code de l'interface.   
C'est un objet hérité de Tk().   
Nous y avons mis toute la création des différents menus et des fonctions associées.   
L'affichage est donc également géré dans ce fichier.   
L'analyse se fait en appelant la fonction analyse_trames du fichier analyze.py

### analyze.py

Contient tout le code concernant l'analyse.
Les fonctions analyse_trames et verify_trame permettent de construire les trames à partir du contenu du fichier, stocker dans la variable globale "content". Les ascii dump sont gérés dans cet fichier-ci, si et seulement si ils sont séparés d'au moins trois espaces des données à analyser (nous nous sommes basés sur les exportations avec ascii dump de wireshark). De même, les lignes vides sont gérés par le programme. S'il y a un problème d'offset ou d'une ligne non analysable en plein milieu d'une trame, alors cette dernière est catégorisée comme "non analysable"   
Nous y avons donc créé l'objet Trame(), contenant toutes les informations possibles sur les différentes trames données. Comme le sujet nous l'indique, on ne peut interpréter que Ethernet II, IPv4, TCP et HTTP, mais si l'on connait le type ou le protocole, on va tout de même le stocker, sans pour autant analyser les informations encapsulées.

### tri.py

Ce fichier contient deux fonctions. Tri_trames permet de séparer les trames analysables (Ethernet) des autres. Recup_adress permet de récupérer les adresses ip des trames ipv4 et les adresses macs des trames ethernet non ipv4 et de les associer à une coordonnée x, dans le but de les afficher.