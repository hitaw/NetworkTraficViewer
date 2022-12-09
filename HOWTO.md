# Comment installer et lancer le programme ?

1. Linux

Si tkinter est déjà installé sur votre ordinateur, lancez la commande `make run` ou directement `python fireshark.py` dans le terminal de commande, après vous être placé dans le dossier Fireshark avec la commande `cd`
Dans le cas contraire, il faut installer tkinter manuellement. Comme les commandes changent en fonction des distibutions, il est compliqué de faire un makefile complet (par exemple la commande pour manjaro sera `sudo pacman -S tk`)

2. Mac

Si tkinter est d'ores et déjà installé sur votre ordinateur, lancez la commande `make run` ou directement `python3 fireshark.py` dans le terminal de commande, après vous être placé dans le dossier Fireshark avec la commande `cd`.   
Dans le cas contraire, lancez `make all`. Attention, il faut avoir pip3 d'installé. Nous n'avons pas trouver de façon de faire installer pip3. Mais normalement pip3 est automatiquement installé avec python3, il ne devrait donc pas y avoir de problèmes.

3. Windows

Lancez la commande `python fireshark.py` dans le terminal de commande. 
/!\ Les scrollbar ne semblent pas marcher sur cet OS, nous n'avons pas réussi à régler le problème.


4. Informations

Il faut descendre et monter les scrollbar manuellement, nous n'avons pas réussi à associer la molette de la souris à la gestion de la scrollbar.