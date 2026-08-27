import pandas as pd
import json

def generate_dataset():
    # Load data
    stations = pd.read_csv("data/stations.csv")
    transactions = pd.read_csv("data/transactions.csv")
    maintenance = pd.read_csv("data/maintenance.csv")
    complaints = pd.read_csv("data/complaints.csv")

    dataset = []

    # Q1: Total transactions
    total_trans = len(transactions)
    dataset.append({
        "id": 1,
        "question": "Quel est le nombre total de transactions dans le réseau ?",
        "expected_agent": "sql",
        "ground_truth": str(total_trans),
        "eval_type": "exact_match"
    })

    # Q2: Total revenue
    ca_total = transactions['amount'].sum()
    dataset.append({
        "id": 2,
        "question": "Quel est le chiffre d'affaires total généré par toutes les stations ?",
        "expected_agent": "sql",
        "ground_truth": f"{ca_total:.2f}",
        "eval_type": "approx_match"
    })

    # Q3: Station with most breakdowns
    station_breakdowns = maintenance['station_name'].value_counts()
    max_station = station_breakdowns.idxmax()
    max_count = station_breakdowns.max()
    dataset.append({
        "id": 3,
        "question": "Quelle station a subi le plus de pannes et combien ?",
        "expected_agent": "sql",
        "ground_truth": f"{max_station} avec {max_count} pannes",
        "eval_type": "keyword_match"
    })

    # Q4: Most frequent complaint reason
    frequent_reason = complaints['reason'].mode()[0]
    dataset.append({
        "id": 4,
        "question": "Quel est le motif de réclamation le plus fréquent chez les clients ?",
        "expected_agent": "rag",
        "ground_truth": frequent_reason,
        "eval_type": "keyword_match"
    })

    # Q5: High severity complaint category
    high_severity = complaints[complaints['severity'] == 'High']
    high_cat = high_severity['category'].mode()[0] if not high_severity.empty else "Aucune"
    dataset.append({
        "id": 5,
        "question": "Quelles sont les catégories de plaintes classées comme graves ?",
        "expected_agent": "rag",
        "ground_truth": high_cat,
        "eval_type": "keyword_match"
    })

    # Save dataset
    with open("evaluation/evaluation_dataset.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

    print(f"Dataset generated with {len(dataset)} questions in evaluation/evaluation_dataset.json")

if __name__ == "__main__":
    generate_dataset()