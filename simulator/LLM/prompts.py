# ===========================
# PROMPT - RECLAMATIONS CLIENTS
# ===========================

COMPLAINT_PROMPT = """
Tu es un client d'une station-service.

Ta mission est de rédiger une réclamation réaliste destinée au service clientèle.

Informations :

- Identifiant : {complaint_id}
- Date : {date}
- Station : {station}
- Ville : {city}
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
- Longueur : entre 120 et 180 mots.

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
- Station : {station}
- Ville : {city}
- Pompe : {pump}
- Type de panne : {failure}
- Durée estimée de réparation : {repair_time} jour(s)

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