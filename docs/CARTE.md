## Entrées et sorties

*   **lit :** le fichier de logs Apache (brut), la configuration (JSON), et les variables d'environnement (via `.env`). *(et qui décide du chemin : les options en ligne de commande en priorité (`--log`, `--config`, `--reports`), sinon les variables d'environnement (ex: `LOGWATCH_LOG`) chargées potentiellement par le `.env`, sinon la valeur par défaut codée en dur dans `argparse`).*
*   **écrit :** un fichier de rapport au format JSON horodaté dans le dossier spécifié (ex: `reports/rapport-20231026-153000.json`).
*   **supprime :** les anciens fichiers de rapports JSON présents dans le dossier `reports` qui dépassent la durée de rétention.

## Les fonctions, dans l'ordre du fichier

| fonction                                            | rend                                                                                                                              |
|-----------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| `charger_env(chemin=".env")`                        | `None` (fonction à effet de bord : peuple `os.environ` avec le contenu du fichier `.env`).                                          |
| `charger_config(chemin)`                            | Un `dict` (dictionnaire) contenant la configuration finale (défauts écrasés par le JSON).                                         |
| `parser_ligne(ligne)`                               | Un dictionnaire à onze clés, ou `None` si la ligne n'a pas la forme attendue.                                                     |
| `lire_log(chemin, encodage="utf-8")`                | Un `tuple` (une liste des entrées parsées avec succès, un entier comptant les lignes ignorées).                                   |
| `anonymiser_ip(ip)`                                 | Une `str` (chaîne de caractères) représentant l'IP avec le dernier octet remplacé par "x".                                        |
| `d1_requetes_par_ip(entrees, top_ips)`              | Un `dict` contenant le décompte total ("somme") et le top des IP les plus actives ("par_ip").                                     |
| `d2_brute_force(entrees, url_login, seuil)`         | Une `list` de dictionnaires contenant les alertes d'IP ayant dépassé le seuil d'échecs de connexion.                              |
| `d3_scan(entrees, seuil)`                           | Une `list` de dictionnaires d'alertes (IP, nb d'URLs sondées, liste des URLs), triée par gravité.                                 |
| `d4_pic_trafic(entrees, seuil_pic, fenetre_minutes)`| Un `dict` décrivant l'alerte de pic de trafic (statut booléen, charge moyenne, max par minute, etc.).                             |
| `d5_erreurs_5xx(entrees, seuil)`                    | Un `dict` résumant le volume d'erreurs serveur (nombre de 5xx, total, ratio et statut de l'alerte).                               |
| `d6_purger_rapports(dossier, retention_jours)`      | Une `list` de chaînes de caractères (les noms des fichiers de rapport qui ont été supprimés).                                     |
| `analyser(entrees, config)`                         | Un `dict` constituant le corps du rapport (regroupe les retours des fonctions D1 à D5).                                           |
| `ecrire_rapport(rapport, dossier)`                  | Un objet `Path` correspondant au chemin complet du fichier JSON qui vient d'être sauvegardé.                                      |
| `main(argv=None)`                                   | Un `int` (code de retour du programme : `0` si succès, `1` si échec).                                                             |

## Les détections annoncées par le README (question 7)

| détection | fonction | ce que le README lui demande (seuil, unité, « dès que » / « au moins » / « au-delà ») |
|-----------|----------|------------------------------------------------------------------------------------|
| D1        | `d1_requetes_par_ip` | Liste les `top_ips` (10) IP ayant fait le plus de requêtes avec succès (statut < 400). |
| D2        | `d2_brute_force`     | Alerte **au-delà** de `seuil_brute_force` (10) tentatives POST échouées (401/403) sur `url_login`. |
| D3        | `d3_scan`            | Alerte **dès que** l'IP a testé **au moins** `seuil_scan` (5) URLs suspectes différentes (liste `MOTIFS_SCAN`). |
| D4        | `d4_pic_trafic`      | Alerte **au-delà** d'une moyenne de `seuil_pic` (100) requêtes par minute. |
| D5        | `d5_erreurs_5xx`     | Alerte **au-delà** d'un ratio de `seuil_5xx` (0.5 soit 50%) de requêtes serveur en erreur (500-599). |
| D6        | `d6_purger_rapports` | Supprime les rapports **dès que** leur ancienneté dépasse la limite fixée (censée être `retention_jours`). |

## Points opaques (question 8)

*   **Ligne 114 (dans `d4_pic_trafic`)** : Que vaut le paramètre `fenetre_minutes` quand il est passé à la fonction ? Il est censé valoir `5` selon les paramètres par défaut, mais ce paramètre **n'est jamais utilisé dans la fonction** ! Le script calcule une moyenne globale par minute sur la totalité du fichier log au lieu d'observer une fenêtre glissante.
*   **Ligne 132 (dans `d6_purger_rapports`)** : Que vaut `limite_jours` quand `retention_jours` vaut `7` (la valeur par défaut) ? Il vaut **210** ! (`limite_jours = retention_jours * 30`). Le commentaire indique "retention exprimée en mois", ce qui est en contradiction totale avec le nom de la variable `retention_jours` qui sous-entend clairement des jours. Cela risque de conserver les logs liés aux IPs pendant 210 jours (presque 7 mois) au lieu des 7 jours prévus, ce qui pose un problème de conformité RGPD.