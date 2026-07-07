from pathlib import Path
from datetime import datetime, timedelta
import random

import pandas as pd

from config import (DELIVERY_THRESHOLD, MONTH_FACTOR, START_DATE, END_DATE, WEEKDAY_FACTOR, FUELS,
    MIN_LITERS, MAX_LITERS, PRICE, PAYMENT_METHODS, FAILURE_CONFIG, TECHNICIANS
)

class SimulationEngine:

    def __init__(self):

        self.stations = pd.read_csv("data/stations.csv")

        self.inventory = pd.read_csv("data/inventory.csv")

        self.pumps = pd.read_csv("data/pumps.csv")


        self.current_date = pd.to_datetime(START_DATE)

        self.end_date = pd.to_datetime(END_DATE)

        # Historique de toute la simulation

        self.transactions = []

        self.maintenance = []

        self.deliveries = []

        self.complaints = []

        self.daily_activity = []

        self.inventory_history = []


    def calculate_failure_probability(self, usage, failure_type):

        config = FAILURE_CONFIG[failure_type]

        probability = (
            config["base_probability"]
            + usage * config["usage_factor"]
        )

        return probability
    

    def create_failure(self, index, pump, failure_type):

        repair_days = FAILURE_CONFIG[failure_type]["repair_days"]

        self.pumps.loc[index, "status"] = "Out of Service"

        self.pumps.loc[index, "repair_end_date"] = (
            self.current_date
            + timedelta(days=repair_days)
        )

        technician = random.choice(TECHNICIANS)

        self.maintenance.append({

            "maintenance_id": f"MT{len(self.maintenance)+1:06d}",

            "pump_id": pump["pump_id"],

            "station_id": pump["station_id"],

            "failure_type": failure_type,

            "start_date": self.current_date,

            "expected_end_date": self.current_date + timedelta(days=repair_days),

            "end_date": None,

            "technician": technician["name"],

            "telephone": technician["phone"],

            "status": "In Progress"

        })


    def check_failures(self):

        for idx, pump in self.pumps.iterrows():

            if pump["status"] != "Operational":
                continue

            usage = pump["usage_count"]

            for failure_type in FAILURE_CONFIG:

                probability = self.calculate_failure_probability(
                    usage,
                    failure_type
                )

                if random.random() < probability:

                    self.create_failure(
                        idx,
                        pump,
                        failure_type
                    )

                    break


    def process_maintenance(self):

        for idx, maintenance in enumerate(self.maintenance):

            if maintenance["status"] != "In Progress":
                continue

            if maintenance["expected_end_date"].date() != self.current_date.date():
                continue

            maintenance["status"] = "Completed"
            maintenance["end_date"] = self.current_date

            mask = (
                self.pumps["pump_id"]
                == maintenance["pump_id"]
            )

            self.pumps.loc[mask, "status"] = "Operational"

            self.pumps.loc[mask, "repair_end_date"] = None


    def save_results(self):

        pd.DataFrame(self.transactions).to_csv(
            "data/transactions.csv",
            index=False
        )
        print(f"\n{len(self.transactions)} transactions sauvegardées.")

        pd.DataFrame(self.deliveries).to_csv(
            "data/deliveries.csv",
            index=False
        )
        print(f"\n{len(self.deliveries)} livraisons sauvegardées.")

        self.inventory.to_csv(
            "data/inventory.csv",
            index=False
        )
        print(f"\n{len(self.inventory)} articles d'inventaire sauvegardés.")

        self.pumps.to_csv(
            "data/pumps.csv",
            index=False
        )
        print(f"\n{len(self.pumps)} pompes sauvegardées.")

        pd.DataFrame(self.inventory_history).to_csv(
            "data/inventory_history.csv",
            index=False
        )
        pd.DataFrame(self.maintenance).to_csv(
            "data/maintenance.csv",
            index=False
        )
        print(f"\n{len(self.maintenance)} maintenances sauvegardées.")

        pd.DataFrame(self.complaints).to_csv(
            "data/complaints.csv",
            index=False

        )

        print(f"{len(self.complaints)} réclamations sauvegardées.")
        

    def create_complaint(
            self,
            station_id,
            station_name,
            category,
            severity,
            reason
        ):

        # Vérifier si une plainte identique existe déjà
        for complaint in self.complaints:

            if (
                complaint["date"] == self.current_date.date()
                and complaint["station_id"] == station_id
                and complaint["category"] == category
                and complaint["reason"] == reason
            ):

                complaint["affected_customers"] += 1
                return

        # Sinon créer une nouvelle plainte

        complaint = {

            "complaint_id": f"CP{len(self.complaints)+1:06d}",

            "date": self.current_date.date(),

            "station_id": station_id,

            "station_name": station_name,

            "category": category,

            "severity": severity,

            "reason": reason,

            "affected_customers": 1,

            "complaint_text": "",

            "resolved": False

        }

        self.complaints.append(complaint)


    def run(self):

        while self.current_date <= self.end_date:

            print(f"\n===== {self.current_date.date()} =====")

            self.process_maintenance()

            # Les camions arrivent avant les ventes du jour
            self.process_deliveries()

            self.simulate_day()

            self.check_failures()

            self.current_date += pd.Timedelta(days=1)

        self.save_results()


    def calculate_customers(self):

        month = self.current_date.month
        weekday = self.current_date.weekday()

        daily_customers = []

        for _, station in self.stations.iterrows():

            customers = (
            station["base_customers"]
            * station["location_factor"]
            * MONTH_FACTOR[month]
            * WEEKDAY_FACTOR[weekday]
            * random.uniform(0.90, 1.10)
            )

            customers = int(customers)

            daily_customers.append({
            "date": self.current_date.date(),
            "station_id": station["station_id"],
            "station_name": station["station_name"],
            "customers": int(customers)
            })

        return pd.DataFrame(daily_customers)
    

    def save_inventory_snapshot(self):
        """
        Sauvegarde l'état du stock de toutes les stations
        à la fin de la journée.
        """

        for _, row in self.inventory.iterrows():

            self.inventory_history.append({

                "date": self.current_date.date(),

                "station_id": row["station_id"],

                "fuel": row["fuel_type"],

                "current_stock": round(row["current_stock"], 2),

                "tank_capacity": row["tank_capacity"],

                "stock_percentage": round(
                    row["current_stock"] / row["tank_capacity"] * 100,
                    2
                )

            })

    
    def create_delivery_request(self, station_id, fuel):

        # Vérifier qu'une livraison n'est pas déjà programmée
        for delivery in self.deliveries:
            if (
                delivery["station_id"] == station_id
                and delivery["fuel"] == fuel
                and delivery["status"] == "Scheduled"
            ):
                return

        mask = (
            (self.inventory["station_id"] == station_id)
            & (self.inventory["fuel_type"] == fuel)
        )

        capacity = self.inventory.loc[mask, "tank_capacity"].iloc[0]
        current = self.inventory.loc[mask, "current_stock"].iloc[0]

        quantity = round(capacity - current, 2)

        delay = random.choices(
                population=[1, 2],
                weights=[90, 10],
                k=1
                )[0]

        delivery = {

            "delivery_id": f"DL{len(self.deliveries)+1:06d}",

            "station_id": station_id,

            "fuel": fuel,

            "order_date": self.current_date,

            "scheduled_date": self.current_date + timedelta(days=delay),

            "completed_date": None,

            "quantity": quantity,

            "status": "Scheduled"

        }

        self.deliveries.append(delivery)


    def update_inventory(self, transaction):

        station = transaction["station_id"]
        fuel = transaction["fuel"]
        liters = transaction["liters"]

        mask = (
            (self.inventory["station_id"] == station)
            & (self.inventory["fuel_type"] == fuel)
        )

        current_stock = self.inventory.loc[mask, "current_stock"].iloc[0]
        tank_capacity = self.inventory.loc[mask, "tank_capacity"].iloc[0]

        if current_stock < liters:
            station_name = transaction["station_name"]

            self.create_complaint(

            station,

            station_name,

            category="Stock",

            severity="High",

            reason=f"{fuel} unavailable"

            )   
            return False
        
        self.inventory.loc[mask, "current_stock"] -= liters
        
        current_stock = self.inventory.loc[mask, "current_stock"].iloc[0]
        
        ratio = current_stock / tank_capacity

        if ratio <= DELIVERY_THRESHOLD:
            self.create_delivery_request(station, fuel)

        return True
    

    def process_deliveries(self):

        for delivery in self.deliveries:

            if delivery["status"] != "Scheduled":
                continue

            if delivery["scheduled_date"].date() != self.current_date.date():
                continue

            mask = (
                (self.inventory["station_id"] == delivery["station_id"])
                & (self.inventory["fuel_type"] == delivery["fuel"])
            )

            capacity = self.inventory.loc[mask, "tank_capacity"].iloc[0]

            self.inventory.loc[mask, "current_stock"] = capacity

            delivery["completed_date"] = self.current_date

            delivery["status"] = "Completed"


    def select_pump(self, station_id, fuel):
        """
        Sélectionne une pompe disponible pour une station et un carburant.
        """

        available_pumps = self.pumps[
            (self.pumps["station_id"] == station_id)
            & (self.pumps["fuel_type"] == fuel)
            & (self.pumps["status"] == "Operational")
        ]

        if available_pumps.empty:
            return None

        pump = available_pumps.sample(1).iloc[0]

        return pump
    
    
    def update_pump_usage(self, pump_id):
        """
        Incrémente le nombre d'utilisations d'une pompe.
        """

        mask = self.pumps["pump_id"] == pump_id

        self.pumps.loc[mask, "usage_count"] += 1


    
    def generate_transactions(self, daily_customers):

        for _, station in daily_customers.iterrows():

            station_id = station["station_id"]
            station_name = station["station_name"]

            for _ in range(station["customers"]):

                fuel = random.choices(
                    FUELS,
                    weights=[0.75, 0.25],
                    k=1
                )[0]

                liters = round(
                    random.uniform(MIN_LITERS, MAX_LITERS),
                    2
                )

                amount = round(
                    liters * PRICE[fuel],
                    2
                )

                payment = random.choices(
                    list(PAYMENT_METHODS.keys()),
                    weights=list(PAYMENT_METHODS.values()),
                    k=1
                )[0]

                if payment == "Card" and random.random() < 0.001:

                    self.create_complaint(

                        station_id,

                        station_name,

                        category="Payment",

                        severity="Low",

                        reason="Card payment failed"

                    )

                pump = self.select_pump(station_id, fuel)

                if pump is None:
                    self.create_complaint(

                        station_id,

                        station_name,

                        category="Pump",

                        severity="Medium",

                        reason="No operational pump available"

                    )
                    continue

                pump_id = pump["pump_id"]

                hour = random.randint(6, 22)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)

                transaction_time = self.current_date.replace(
                    hour=hour,
                    minute=minute,
                    second=second
                )

                transaction = {

                    "transaction_id": f"TR{len(self.transactions)+1:08d}",

                    "datetime": transaction_time,

                    "station_id": station_id,

                    "station_name": station_name,

                    "pump_id": pump_id,

                    "fuel": fuel,

                    "liters": liters,

                    "amount": amount,

                    "payment_method": payment

                }

                success = self.update_inventory(transaction)

                if success:
                    self.transactions.append(transaction)
                    self.update_pump_usage(pump_id)
        
                

    def simulate_day(self):

        customers = self.calculate_customers()
        self.generate_transactions(customers)

        self.save_inventory_snapshot()

        print(f"Transactions générées : {len(self.transactions)}")