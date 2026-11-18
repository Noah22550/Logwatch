from logwatch import lire_log

sample_logs, ignorees = lire_log("sample-logs.log")

print(f"Nombre de lignes lues : {len(sample_logs)}")
print(f"et nombre de lignes ignorees : {ignorees}")


"""Compte le nombre de requetes par famille de code de réponse"""
compteur  = {}
for log in sample_logs:
  status = str(log["statut"])[0] + "xx"  # Regroupe les codes par famille (2xx, 3xx, 4xx, 5xx)
  compteur[status] = compteur.get(status, 0) + 1

print(compteur)
print(sum(compteur.values()))  # Devrait correspondre au nombre total de lignes lues

compteur2  = {}
for log in sample_logs:
  adresseIp = log["ip"]  
  compteur2[adresseIp] = compteur2.get(adresseIp, 0) + 1
print(compteur2)
print(sum(compteur2.values()))  # Devrait correspondre au nombre total de lignes lues

compteur3  = {}
for log in sample_logs:
  if log["methode"] == "POST" and log["url"] == "/login" and log["statut"] in (401, 403):  
    adresseIp = log["ip"]  # Regroupe les codes par famille (2xx, 3xx, 4xx, 5xx)
    compteur3[adresseIp] = compteur3.get(adresseIp, 0) + 1
print(compteur3)
print(sum(compteur3.values()))
print(sample_logs[0].keys())



par_minute = {}
for log in sample_logs:
    minute = log["date"][:17]
    par_minute[minute] = par_minute.get(minute, 0) + 1
minute_max = None
for minute, n in par_minute.items():
    if minute_max is None or n > par_minute[minute_max]:
        minute_max = minute
print(f"Minute la plus chargée : {minute_max} avec {par_minute[minute_max]} requêtes")
somme_totale = sum(par_minute.values())
print(f"Vérification : somme des minutes ({somme_totale}) = total des requêtes lues ({len(sample_logs)})")

fenetre_minutes = 5
par_fenetre = {}

for log in sample_logs:
    date_minute = log["date"][:17]
    m = int(date_minute[-2:])
    debut = m - (m % fenetre_minutes)
    cle_fenetre = f"{date_minute[:15]}{debut:02d}"
    par_fenetre[cle_fenetre] = par_fenetre.get(cle_fenetre, 0) + 1
    fenetre_max = None
for fenetre, n in par_fenetre.items():
    if fenetre_max is None or n > par_fenetre[fenetre_max]:
        fenetre_max = fenetre

print(f"Fenêtre la plus chargée : {fenetre_max} avec {par_fenetre[fenetre_max]} requêtes")

somme_requetes = sum(par_minute.values())
nombre_de_minutes = len(par_minute)

charge_calculee = somme_requetes / nombre_de_minutes

print(f"Charge calculée : {round(charge_calculee, 1)}")


total_requetes = sum(compteur.values())
part_5xx = compteur.get("5xx", 0) / total_requetes if total_requetes > 0 else 0

print(f"[D5] Part des 5xx : {part_5xx:.1%} ({compteur.get('5xx', 0)}/{total_requetes}) | Seuil README : 5.0%")

motifs_scan = ["wp-admin", "wp-login", "phpmyadmin", ".env", ".git", "../", "xmlrpc", "/admin/"]
suspects = {}
for log in sample_logs:
    url_min = log["url"].lower()
    if any(m in url_min for m in motifs_scan):
        suspects.setdefault(log["ip"], set()).add(log["url"])
alertes_scan = {ip: len(urls) for ip, urls in suspects.items() if len(urls) >= 5}
print(f"[D3] IPs scanner (>= 5 URLs distinctes) : {alertes_scan}")

# D7 - Requetes lentes (duree en microsecondes dans le log, seuil en millisecondes)
avec_duree = [log for log in sample_logs if log["duree"] is not None]
lentes_seuil_0 = [log for log in avec_duree if log["duree"] / 1000 > 0]

seuil_lenteur_ms = 2000
lentes = [log for log in avec_duree if log["duree"] / 1000 > seuil_lenteur_ms]
plus_lente = max(lentes, key=lambda log: log["duree"]) if lentes else None

print(f"[D7] Verification seuil 0 ms : {len(lentes_seuil_0)} / {len(avec_duree)} entrees avec duree")
print(f"[D7] Requetes lentes (> {seuil_lenteur_ms} ms) : {len(lentes)}")
if plus_lente:
    print(
        f"[D7] Plus lente : {plus_lente['duree'] / 1000:.1f} ms "
        f"({plus_lente['ip']} {plus_lente['methode']} {plus_lente['url']})"
    )
