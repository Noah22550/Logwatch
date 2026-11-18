# Spécification chiffrée — LogWatch

**Date de création :** 18/11/2026  
**Jeu de référence :** `sample-logs.log` et `config.json` du kit (copie de `config.example.json`, avec `seuil_5xx: 0.05` et `seuil_lenteur_ms: 2000`).  
**Source des chiffres attendus :** `explorer.py` (jamais la sortie de `logwatch.py` v0).

---

## D1 - Requêtes par IP

| Cas | Id | Prerequis | Etape | Resultat attendu | Obtenu | Statut |
|---|---|---|---|---|---|---|
| nominal | D1-01 | `sample-logs.log`, `config.json` du kit (`top_ips = 10`) | `python logwatch.py` | `D1_requetes_par_ip.somme = 743` (`== total_lines`, source `explorer.py` : `len(sample_logs)` et `sum(compteur2.values())`), au plus 10 entrées dans `par_ip`, IP anonymisées (`x` en dernier octet) | | |
| limite | D1-02 | fichier fabriqué avec 3 requêtes toutes en erreur (`401`, `404`, `500`) | `python logwatch.py --log ...` | `D1_requetes_par_ip.somme = 3` (`== total_lines`), les réponses `>= 400` sont comptées | | |
| erreur | D1-03 | `sample-logs.log` contenant 3 lignes mal formées (tronquée, ligne de rotation, date `11:2x:15`) | `python logwatch.py` | `lignes_ignorees = 3` (source `explorer.py` : `ignorees`), ces 3 lignes sont exclues de `somme` | | |

## D2 - Brute force

| Cas | Id | Prerequis | Etape | Resultat attendu | Obtenu | Statut |
|---|---|---|---|---|---|---|
| nominal | D2-01 | `sample-logs.log`, `config.json` du kit (`seuil_brute_force = 10`, `url_login = "/login"`) | `python logwatch.py` | `1` IP signalée (`198.51.100.x`), `tentatives = 45`, `gravite = "haute"` (source `explorer.py` : `compteur3`) | | |
| limite | D2-02 | fichier fabriqué avec exactement `10` requêtes `POST /login` en `401` depuis une même IP (`seuil_brute_force = 10`) | `python logwatch.py --log ...` | `1` IP signalée avec `tentatives = 10` (le README indique « dès qu'elle atteint » : `>=`) | | |
| erreur | D2-03 | fichier fabriqué avec `15` requêtes `POST /login` en `302` (succès) ou `GET /login` en `401` | `python logwatch.py --log ...` | `0` IP signalée (`D2_brute_force = []`) | | |

## D3 - Scan de vulnérabilités

| Cas | Id | Prerequis | Etape | Resultat attendu | Obtenu | Statut |
|---|---|---|---|---|---|---|
| nominal | D3-01 | `sample-logs.log`, `config.json` du kit (`seuil_scan = 5`) | `python logwatch.py` | `1` IP signalée (`203.0.113.x`), `nb_urls = 14` (`>= 5`, source `explorer.py` : `alertes_scan`, à mesurer si la liste des motifs évolue) ; `192.0.2.x` absente | | |
| limite | D3-02 | fichier fabriqué avec `4` URL suspectes distinctes (`< 5`) ou `10` fois la même URL `/wp-admin/` | `python logwatch.py --log ...` | `0` IP signalée (`D3_scan = []`), seules les URL distinctes comptent | | |
| erreur | D3-03 | fichier fabriqué avec 6 pages légitimes (`/administration-des-reservations.html`, `/administration/planning`, `/administration/tarifs`, `/administration/clients`, `/administration/export.csv`, `/admin-guide.pdf`) | `python logwatch.py --log ...` | `0` IP signalée (`D3_scan = []`), aucun faux positif sur les pages légitimes | | |

## D4 - Pic de trafic

| Cas | Id | Prerequis | Etape | Resultat attendu | Obtenu | Statut |
|---|---|---|---|---|---|---|
| nominal | D4-01 | `sample-logs.log`, `config.json` du kit (`fenetre_minutes = 5`, `seuil_pic = 100`) | `python logwatch.py` | `alerte = true`, fenêtre la plus chargée = `03/Sep/2026:11:15` (tranche `11:15-11:20`) avec `190` requêtes (`> 100`, source `explorer.py` : `par_fenetre` / `fenetre_max`) | | |
| limite | D4-02 | fichier fabriqué avec exactement `100` requêtes dans la fenêtre `10:00-10:05` (`seuil_pic = 100`) | `python logwatch.py --log ...` | `alerte = false` (le README indique « dépasse `seuil_pic` » : comparaison stricte `>`) | | |
| erreur | D4-03 | liste d'entrées vide (fichier vide ou uniquement des lignes mal formées) | appel `d4_pic_trafic([], 100, 5)` | `alerte = false`, compteur à `0`, fenêtre `None`, aucune exception | | |

## D5 - Erreurs serveur (5xx)

| Cas | Id | Prerequis | Etape | Resultat attendu | Obtenu | Statut |
|---|---|---|---|---|---|---|
| nominal | D5-01 | `sample-logs.log`, `config.json` du kit (`seuil_5xx = 0.05`) | `python logwatch.py` | `nb_5xx = 48`, `total = 743`, `ratio = 0.0646` (`6.5 % > 5.0 %`), `alerte = true` (source `explorer.py` : `compteur["5xx"]` et `part_5xx`) | | |
| limite | D5-02 | fichier fabriqué avec `5` réponses `500` sur `100` requêtes (`ratio = 0.05`, `seuil_5xx = 0.05`) | `python logwatch.py --log ...` | `nb_5xx = 5`, `ratio = 0.05`, `alerte = false` (le README indique « au-delà de `seuil_5xx` » : `>`) | | |
| erreur | D5-03 | `config.json` absent (repli sur `DEFAUTS`) ou fichier sans requête exploitable (`entrees = []`) | `python logwatch.py` / `d5_erreurs_5xx([], 0.05)` | défaut `seuil_5xx = 0.05` appliqué (et non `0.5`) ; sur 0 requête : `ratio = 0.0`, `alerte = false`, pas de `ZeroDivisionError` | | |

## D6 - Purge des rapports (RGPD)

| Cas | Id | Prerequis | Etape | Resultat attendu | Obtenu | Statut |
|---|---|---|---|---|---|---|
| nominal | D6-01 | dossier temporaire contenant 1 `rapport-*.json` vieilli de `8` jours, `config.json` du kit (`retention_jours = 7`) | `python logwatch.py --reports essais` | `len(D6_rapports_purges) = 1`, le rapport de `8` jours est supprimé du disque (non calculé par `explorer.py` : dépend du système de fichiers) | | |
| limite | D6-02 | dossier temporaire contenant 1 rapport âgé de `6` jours et 1 rapport âgé de `7` jours et 1 seconde (`retention_jours = 7`) | `python logwatch.py --reports essais` | `len(D6_rapports_purges) = 1` : le rapport de `6` jours est conservé, celui de `> 7` jours est supprimé | | |
| erreur | D6-03 | dossier `--reports` inexistant, ou contenant un fichier tiers (`notes.txt`) vieux de `30` jours | `python logwatch.py --reports essais` | `D6_rapports_purges = []`, aucune erreur, dossier créé, `notes.txt` conservé intact | | |

## D7 - Requêtes lentes (à implémenter)

| Cas | Id | Prerequis | Etape | Resultat attendu | Obtenu | Statut |
|---|---|---|---|---|---|---|
| nominal | D7-01 | `sample-logs.log`, `config.json` du kit (`seuil_lenteur_ms = 2000`) | `python logwatch.py` | `D7_requetes_lentes.nb = 9`, 1re entrée de `requetes` à `duree_ms = 4901.6` (`192.0.2.x`, `GET /reservations`), liste triée par `duree_ms` décroissante, max 20 éléments (source `explorer.py` : section D7, vérifiée à seuil `0 ms` = `743 / 743` entrées avec durée) | | |
| limite | D7-02 | fichier fabriqué avec 1 requête de `2000000` µs (exactement `2000` ms) et 1 requête de `2000` µs (`2` ms), `seuil_lenteur_ms = 2000` | `python logwatch.py --log ...` | `nb = 0`, `requetes = []` (le README indique « dont la durée **dépasse** `seuil_lenteur_ms` » : comparaison stricte `> 2000` ms après conversion `duree / 1000`) | | |
| erreur | D7-03 | fichier fabriqué (cas absent de `sample-logs.log`) contenant 1 ligne Apache combined classique **sans champ durée** (`duree = None`) | `python logwatch.py --log ...` | ligne acceptée (`lignes_ignorees = 0`), pas de `TypeError`, jamais comptée comme lente (`nb = 0`, `requetes = []`) | | |