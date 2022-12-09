# Comment installer et lancer le programme ?

1. Linux

Lancer la commande `make run` ou directement `python fireshark.py` dans le terminal de commande, après vous être placé dans le dossier Fireshark avec la commande `cd`

2. Mac

Si tkinter est d'ores et déjà installé sur votre ordinateur, lancer la commande `make run` ou directement `python3 fireshark.py` dans le terminal de commande, après vous être placé dans le dossier Fireshark avec la commande `cd`
Dans le cas contraire, lancer la commande `make all`, qui installe pip3 et tkinter. Si jamais cela ne marche pas (le makefile a été testé sur une vieille version de MAC OS, la seule à notre disposition), il faudra installer manuellement pip3 et/ou tkinter.

3. Windows

Lancer la commande `python fireshark.py` dans le terminal de commande. /!\ Les scrollbar ne semblent pas marcher sur cet OS, nous n'avons pas réussi à régler le problème.


4. Informations

Il faut descendre et monter les scrollbar manuellement, nous n'avons pas réussi à associer la molette de la souris à la gestion de la scrollbar.