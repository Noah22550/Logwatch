# Registre des défauts LogWatch - N défaut(s) ouvert(s) au AAAA-MM-JJ
| n° | date | symptôme observé
| fonction suspectée | état |
|----|------------|---------------------------------------------------------
--|--------------------|--------|
| B1    | 2026-09-29 | test_d1_somme_egale_total_lines rouge : attendu 6, reçu3 | la boucle ne compte une requête que si son statut est inférieur à 400.
Le README demande que D1 compte toutes les requêtes.Correction prévue : compter toutes les entrées sans filtrer sur le statut HTTP. | ouvert |
| B2    | AAAA-MM-JJ | test_d3_ignore_url_legitime rouge : attendu [], reçu | Cause racine : le test de détection considère un motif suspect dès qu'il apparaît comme sous-chaîne dans l'URL, ce qui fait classer des URLs légitimes contenant « admin » ou « administration » comme suspectes.
Correction prévue : distinguer les motifs réellement suspects des occurrences légitimes dans les URLs.   | ouvert     |
## B1 - <le symptôme, en cinq mots>
 Test en échec : test_d1_somme_egale_total_lines
 Attendu / reçu : 6 / 3
 Fonction visée : ..., ligne NN
 Cause racine : ...
 Correction prévue : ...
 (étape 6) Correctif : commit <hash>, <auteur>, le AAAA-MM-JJ
 Vérifié par : <nom>, sur <le cas éprouvé, différent de celui du
test>
## B2 - ...