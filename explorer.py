from logwatch import lire_log

sample_logs, ignorees = lire_log("sample-logs.log")

print(f"Nombre de lignes lues : {(len(sample_logs))}")


"""Compte le nombre de requetes par famille de code de réponse"""
compteur  = {}
for log in sample_logs:
  status = str(log["statut"])[0] + "xx"  # Regroupe les codes par famille (2xx, 3xx, 4xx, 5xx)
  compteur[status] = compteur.get(status, 0) + 1

print(compteur)
print(sum(compteur.values()))  # Devrait correspondre au nombre total de lignes lues

compteur2  = {}
for log in sample_logs:
  adresseIp = log["ip"]  # Regroupe les codes par famille (2xx, 3xx, 4xx, 5xx)
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