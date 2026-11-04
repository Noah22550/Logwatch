# Registre des défauts LogWatch - 2 défaut(s) ouvert(s) au 30/09/2026
| n° | date | symptôme observé
| fonction suspectée | état |
|----|------------|---------------------------------------------------------
--|--------------------|--------|

## B1 - <la condition qui foire>

 Test en échec : test_d1_somme_egale_total_lines
 Attendu / reçu : 6 / 3
 Fonction visée : d1_somme_egale_total_lines, ligne NN
 Cause racine : le if dans D1 qui n'est pas bon. on attend 6 statut dans le test (200, 404, 200, 500,401,200) sur 6 route différentes, sauf que notre fonction ne renvoie que celle ou son statut est inférieur à 400 donc ça plante
 Correction prévue : retirer la condition afin de correspondre au test et comtabilisé toute les routes
 (étape 6) Correctif : commit <hash>, <auteur>, le 30/09/2026
 Vérifié par : <Noah>, sur <le cas éprouvé, différent de celui du test>

## B2 - <les motifs >

 Test en échec : test_d3_ignore_url_legitime
 Attendu / reçu : [] / [{'ip': '10.0...': 'moyenne'}]
 Fonction visée : d1_somme_egale_total_lines, ligne NN
 Cause racine : dans notre fonction on vérifie les motifs qui méritent un scan, dans les routes que l'on test nous avons deux motifs qui fait partie de de cette liste(adimn et ../) donc on peut en conclure que ça foire a cause de cette vérification qui prend en compte ces motifs. 
 Correction prévue :
 (étape 6) Correctif : commit <hash>, <auteur>, le 30/09/2026
 Vérifié par : <Noah>, sur <le cas éprouvé, différent de celui du test>

## B3 - <Pic de trafic non détecté et paramètre de fenêtre ignoré>

Test en échec : N/A (constaté manuellement dans le terminal lors de l'exploration)
Attendu / reçu : alerte=True (un pic dépassant 100 requêtes existe) / alerte=False (charge affichée trop basse)
Fonction visée : d4_pic_trafic, ligne de retour ("alerte": charge > seuil_pic)
Cause racine : Le paramètre `fenetre_minutes` de la signature n'est pas utilisé dans la fonction (le découpage est fait fixement minute par minute). De plus, pour déclencher l'alerte, la fonction compare la *moyenne* globale de toutes les minutes au seuil (`charge = statistics.mean(...)`), au lieu de comparer la valeur de la fenêtre la plus chargée.
Correction prévue : Découper les requêtes par tranches en appliquant un modulo avec `fenetre_minutes`, et corriger la condition d'alerte pour vérifier si la fenêtre maximale dépasse le `seuil_pic` (`maxi > seuil_pic`).
(étape 6) Correctif :  commit <hash>, <auteur>, le 19/10/2026
 Vérifié par : <Noah>


## B4 - Valeur incohérente du seuil d'erreurs 5xx (D5)

 Test en échec : N/A (constaté manuellement via explorer.py)
 Attendu / reçu : Le seuil réel utilisé devrait correspondre à la documentation. Voici les valeurs mises côte à côte :
 - README : `seuil_5xx` = 0.05 (5 %)[cite: 6]
 - config.example.json : `seuil_5xx` = 0.05
 - logwatch.py (constante DEFAUTS) : `"seuil_5xx": 0.5`[cite: 5]
 - Rapport JSON (sous config) : `seuil_5xx` = 0.5
 Fonction visée : `DEFAUTS` (ligne 28)[cite: 5]
 Cause racine : Le développeur a confondu 5% (0.05) et 50% (0.5) en codant la valeur par défaut en dur dans la constante `DEFAUTS` de `logwatch.py`[cite: 5].
 Correction prévue : Remplacer `0.5` par `0.05` dans le dictionnaire.
 (étape 6) Correctif : 
 Vérifié par : Noah, en comparant le pourcentage réel du terminal avec le rapport JSON

## B5 - Le seuil brute-force (D2) ne réagit pas à la valeur exacte

 Test en échec : N/A (constaté manuellement avec dix-echecs.log)
 Attendu / reçu : Le README exige qu'une IP soit signalée "dès qu'elle atteint ce nombre d'échecs de connexion"[cite: 6] (soit au bout de 10). / Lors du passage de `dix-echecs.log` (10 échecs), la ligne D2 affiche `0 IP(s)`. L'alerte ne se déclenche qu'à partir de 11 échecs.
 Fonction visée : `d2_brute_force`[cite: 5]
 Cause racine : La comparaison dans le code utilise un opérateur strictement supérieur (`if n > seuil:`)[cite: 5] au lieu d'un opérateur supérieur ou égal.
 Correction prévue : Modifier la condition dans `logwatch.py` par `if n >= seuil:`.
 (étape 6) Correctif : 
 Vérifié par : Noah, via le lancement de journaux d'essais à 10 et 11 lignes