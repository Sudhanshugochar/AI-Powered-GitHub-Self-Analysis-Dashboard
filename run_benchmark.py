import time
import argparse
from src.llm_analysis import OllamaAnalyzer

def run_benchmark(models=["llama3.1", "mistral"], iterations=5):
    print(f"Benchmarking models: {models} with {iterations} iterations...")
    
    tasks = [
        "Explain the concept of recursion in programming.",
        "Write a python function to reverse a string.",
        "Summarize the benefits of using a linter."
    ]

    results = {model: {"total_time": 0, "success_count": 0} for model in models}

    analyzer = OllamaAnalyzer()

    for model in models:
        print(f"\nTesting model: {model}")
        analyzer.model = model
        
        for i in range(iterations):
            for task in tasks:
                start_time = time.time()
                try:
                    # We reuse the compare_models method or just direct chat
                    response = analyzer.client.chat(model=model, messages=[{'role': 'user', 'content': task}])
                    duration = time.time() - start_time
                    
                    if response and 'message' in response:
                        results[model]["total_time"] += duration
                        results[model]["success_count"] += 1
                        print(f"  Iteration {i+1} Task '{task[:10]}...' - Time: {duration:.2f}s")
                    else:
                        print(f"  Iteration {i+1} Task '{task[:10]}...' - Failed")
                except Exception as e:
                    print(f"  Iteration {i+1} Task '{task[:10]}...' - Error: {e}")

    print("\n--- Benchmark Results ---")
    print(f"{'Model':<15} | {'Avg Time (s)':<15} | {'Success Rate':<15}")
    print("-" * 50)
    
    for model, metrics in results.items():
        avg_time = metrics["total_time"] / (iterations * len(tasks)) if metrics["success_count"] > 0 else 0
        success_rate = (metrics["success_count"] / (iterations * len(tasks))) * 100
        print(f"{model:<15} | {avg_time:<15.2f} | {success_rate:<15.2f}%")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark LLM models.")
    parser.add_argument("--models", nargs="+", default=["llama3.1", "mistral"], help="List of models to benchmark")
    parser.add_argument("--iterations", type=int, default=3, help="Number of iterations per task")
    args = parser.parse_args()
    
    run_benchmark(models=args.models, iterations=args.iterations)
