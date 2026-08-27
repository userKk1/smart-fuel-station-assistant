import json
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from agent.assistant import SmartFuelAssistant
except ImportError as e:
    print(f"Error: Cannot import SmartFuelAssistant. Details: {e}")
    sys.exit(1)

def run_evaluation():
    dataset_path = os.path.join(os.path.dirname(__file__), "evaluation_dataset.json")
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    print("Initializing assistant...")
    assistant = SmartFuelAssistant()

    scores = []
    total_latency = 0

    print("\nStarting evaluation...\n")

    for item in dataset:
        question = item["question"]
        # On nettoie la vraie réponse (enlever espaces et changer virgules en points)
        ground_truth = item["ground_truth"].lower().replace(" ", "").replace(",", ".")
        eval_type = item["eval_type"]

        print(f"Question {item['id']}: {question}")

        start_time = time.time()
        try:
            ai_response = assistant.ask(question)
        except Exception as e:
            ai_response = ""
            print(f"   Assistant error: {e}")

        end_time = time.time()
        latency = end_time - start_time
        total_latency += latency

        # On nettoie aussi la réponse de l'IA de la même façon
        ai_response_lower = ai_response.lower().replace(" ", "").replace(",", ".")
        score = 0

        if eval_type == "exact_match" or eval_type == "approx_match":
            # Pour les chiffres, on vérifie simplement si le nombre est dans la réponse
            if ground_truth in ai_response_lower:
                score = 100
                
        elif eval_type == "keyword_match":
            keywords = ground_truth.split()
            found = sum(1 for word in keywords if word in ai_response_lower)
            score = (found / len(keywords)) * 100 if keywords else 0

        scores.append(score)
        display_response = ai_response[:80] + "..." if len(ai_response) > 80 else ai_response
        print(f"   AI Response: {display_response} | Score: {score:.0f}% | Latency: {latency:.2f}s\n")

    avg_score = sum(scores) / len(scores) if scores else 0
    avg_latency = total_latency / len(dataset) if dataset else 0

    print("=" * 50)
    print("EVALUATION RESULTS")
    print("=" * 50)
    print(f"Average accuracy score : {avg_score:.2f}%")
    print(f"Average latency        : {avg_latency:.2f} seconds")
    print(f"Total questions tested : {len(dataset)}")

if __name__ == "__main__":
    run_evaluation()