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