# ===========================
# PROMPT - RECLAMATIONS CLIENTS
# ===========================

COMPLAINT_PROMPT = """
Tu es un client d'une station-service.

Ta mission est de rédiger une réclamation réaliste destinée au service clientèle.

Informations :

- Date : {date}
- id de Station : {station_id}
- Station : {station_name}
- Catégorie : {category}
- Problème rencontré : {reason}
- Niveau de gravité : {severity}
- Nombre de clients concernés : {affected}

Consignes :

- Rédige UNE SEULE réclamation représentant l'ensemble des clients concernés.
- Le texte doit être naturel et crédible.
- Décris les conséquences sur les clients.
- Exprime une insatisfaction professionnelle sans être agressif.
- Ne fais pas de liste.
- Ne mentionne pas que tu es une IA.
- Longueur : court comme si un vrai client l'avait rédigé.

Réclamation :
"""


# ===========================
# PROMPT - RAPPORT DE MAINTENANCE
# ===========================

MAINTENANCE_PROMPT = """
Tu es un technicien de maintenance d'un réseau de stations-service.

Tu dois rédiger un rapport technique professionnel.

Informations :

- Date : {date}
- id de Station : {station_id}
- Station : {station_name}
- Pompe : {pump_id}
- Type de panne : {failure_type}
- Durée estimée de réparation : {start_date} à {expected_end_date} jour(s)
- Date fin de réparation : {end_date}
- Technicien : {technician}
- Status : {status}
Le rapport doit contenir :

- le contexte de l'intervention
- les symptômes observés
- le diagnostic effectué
- les actions réalisées
- les tests de validation
- les recommandations éventuelles

Le style doit être professionnel.

Longueur : entre 150 et 250 mots.

Rapport :
"""