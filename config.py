
# ===========================
# STATIONS CONFIGURATION
# ===========================

STATIONS = {

    "Agadir Centre": {
        "city": "Agadir",
        "type": "urban",
        "location_factor": 1.15,
        "base_customers": 500,
        "tank_capacity": {
            "Gasoil": 40000,
            "Sans Plomb": 18000
        },
        "num_pumps": 8,
        "employees": 12
    },

    "Agadir Port": {
        "city": "Agadir",
        "type": "industrial",
        "location_factor": 0.90,
        "base_customers": 380,
        "tank_capacity": {
            "Gasoil": 22000,
            "Sans Plomb": 15000
        },
        "num_pumps": 6,
        "employees": 10
    },

    "Casablanca Ain Sebaa": {
        "city": "Casablanca",
        "type": "industrial",
        "location_factor": 1.45,
        "base_customers": 700,
        "tank_capacity": {
            "Gasoil": 70000,
            "Sans Plomb": 25000
        },
        "num_pumps": 12,
        "employees": 18
    },

    "Casablanca Maarif": {
        "city": "Casablanca",
        "type": "urban",
        "location_factor": 1.35,
        "base_customers": 650,
        "tank_capacity": {
            "Gasoil": 60000,
            "Sans Plomb": 22000
        },
        "num_pumps": 10,
        "employees": 16
    },

    "Rabat Centre": {
        "city": "Rabat",
        "type": "urban",
        "location_factor": 1.20,
        "base_customers": 560,
        "tank_capacity": {
            "Gasoil": 45000,
            "Sans Plomb": 20000
        },
        "num_pumps": 9,
        "employees": 14
    },

    "Marrakech Nord": {
        "city": "Marrakech",
        "type": "touristic",
        "location_factor": 1.35,
        "base_customers": 620,
        "tank_capacity": {
            "Gasoil": 58000,
            "Sans Plomb": 22000
        },
        "num_pumps": 10,
        "employees": 16
    },

    "Marrakech Sud": {
        "city": "Marrakech",
        "type": "suburban",
        "location_factor": 1.10,
        "base_customers": 480,
        "tank_capacity": {
            "Gasoil": 36000,
            "Sans Plomb": 18000
        },
        "num_pumps": 8,
        "employees": 12
    },

    "Essaouira": {
        "city": "Essaouira",
        "type": "touristic",
        "location_factor": 0.85,
        "base_customers": 320,
        "tank_capacity": {
            "Gasoil": 20000,
            "Sans Plomb": 14000
        },
        "num_pumps": 6,
        "employees": 9
    }

}


FUELS = [
    "Gasoil",
    "Sans Plomb"
]



WEEKDAY_FACTOR = {
    0: 0.95,   # Lundi
    1: 1.00,
    2: 1.00,
    3: 1.05,
    4: 1.10,
    5: 1.30,   # Samedi
    6: 1.20    # Dimanche
}

MONTH_FACTOR = {
    1: 0.75,
    2: 0.80,
    3: 0.90,
    4: 1.00,
    5: 1.10,
    6: 1.20,
    7: 1.40,
    8: 1.55,
    9: 1.20,
    10: 1.00,
    11: 0.90,
    12: 1.30
}


#Quantité achetée

MIN_LITERS = 10

MAX_LITERS = 60


#Prix

PRICE = {

"Gasoil":11.80,

"Sans Plomb":13.50

}


FAILURE_RATE = 0.01

#si le reservoir < 45% -> déclenche automatiquement une commande de livraison de carburant
DELIVERY_THRESHOLD = 0.45 

# ===========================
# FAILURE CONFIGURATION
# ===========================

# Nombre d'utilisations à partir duquel une pompe commence à vieillir
FAILURE_USAGE_THRESHOLD = 3000

# Probabilité minimale de panne
BASE_FAILURE_RATE = 0.00005

# Probabilité maximale
MAX_FAILURE_RATE = 0.02


FAILURE_CONFIG = {

    "Pump Failure": {
        "base_probability": 0.0001,
        "usage_factor": 0.000002, #le risque de panne ajouté à chaque utilisation  
        "repair_days": 3
    },

    "Card Reader Failure": {
        "base_probability": 0.0008,
        "usage_factor": 0.0,
        "repair_days": 1
    },

    "Nozzle Leakage": {
        "base_probability": 0.0003,
        "usage_factor": 0.000001,
        "repair_days": 2
    },

    "Fuel Sensor Error": {
        "base_probability": 0.00015,
        "usage_factor": 0.0000005,
        "repair_days": 4
    },

    "Power Failure": {
        "base_probability": 0.00003,
        "usage_factor": 0.0,
        "repair_days": 5
    }

}


PAYMENT_METHODS = {
    "Cash": 0.30,
    "Card": 0.70
}


PUMP_INSTALLATION_START_YEAR = 2015
PUMP_INSTALLATION_END_YEAR = 2024


TECHNICIANS = [

    {
        "id": "TECH001",
        "name": "Ahmed El Idrissi",
        "phone": "0661234567"
    },

    {
        "id": "TECH002",
        "name": "Salma Benali",
        "phone": "0672345678"
    },

    {
        "id": "TECH003",
        "name": "Youssef Alaoui",
        "phone": "0663456789"
    },

    {
        "id": "TECH004",
        "name": "Khadija Amrani",
        "phone": "0674567890"
    },

    {
        "id": "TECH005",
        "name": "Omar Bennani",
        "phone": "0665678901"
    },

    {
        "id": "TECH006",
        "name": "Fatima Zahra El Fassi",
        "phone": "0676789012"
    },

    {
        "id": "TECH007",
        "name": "Hamza Berrada",
        "phone": "0667890123"
    },

    {
        "id": "TECH008",
        "name": "Nadia Chraibi",
        "phone": "0678901234"
    }

]

ROLES = {

    "Manager": 1,

    "Cashier": 2,

    "Pump Attendant": 5,

    "Maintenance Agent": 1,

    "Security Guard": 1,

    "Cleaning Agent": 2

}

SALARY = {

    "Manager": (8000,12000),

    "Cashier": (3500,4500),

    "Pump Attendant": (3000,4200),

    "Maintenance Agent": (4500,6500),

    "Security Guard": (3000,4000),

    "Cleaning Agent": (2800,3500)

}

#Période de simulation

START_DATE = "2025-01-01"

END_DATE = "2025-01-15"
