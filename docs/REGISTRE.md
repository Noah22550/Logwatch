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