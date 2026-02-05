#!/usr/bin/env python3
"""Test the Monte Carlo visualization API endpoint."""

import requests
import json

BASE_URL = "http://127.0.0.1:8001"

def test_health():
    """Test health endpoint."""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}\n")

def test_strategies_list():
    """Test strategies list endpoint."""
    print("Testing /visualization/strategies endpoint...")
    response = requests.get(f"{BASE_URL}/visualization/strategies")
    print(f"  Status: {response.status_code}")
    print(f"  Response: {json.dumps(response.json(), indent=2)}\n")

def test_visualization():
    """Test Monte Carlo visualization endpoint."""
    print("Testing /visualization/monte-carlo-paths endpoint...")
    
    payload = {
        "strategy_a": "blocking",
        "strategy_b": "random",
        "num_games": 100,
        "num_paths": 20,
        "seed": 12345
    }
    
    print(f"  Request payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/visualization/monte-carlo-paths",
        json=payload
    )
    
    print(f"  Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n  Response summary:")
        print(f"    Strategy A: {data['strategy_a']}")
        print(f"    Strategy B: {data['strategy_b']}")
        print(f"    Total games: {data['total_games']}")
        print(f"    Num paths: {data['num_paths']}")
        print(f"    Final win rate A: {data['final_win_rate_a']:.3f}")
        print(f"    Final win rate B: {data['final_win_rate_b']:.3f}")
        print(f"    95% CI: [{data['ci_lower']:.3f}, {data['ci_upper']:.3f}]")
        print(f"    Convergence std: {data['convergence_std']:.3f}")
        print(f"    Game numbers length: {len(data['game_numbers'])}")
        print(f"    Paths length: {len(data['paths'])}")
        print(f"    First path length: {len(data['paths'][0])}")
        
        # Sample first path values
        print(f"\n  First path sample (first 10 games):")
        for i in range(min(10, len(data['paths'][0]))):
            print(f"    Game {i+1}: {data['paths'][0][i]:.3f}")
    else:
        print(f"  Error: {response.text}")

def main():
    """Run all tests."""
    print("="*70)
    print("Monte Carlo Visualization API Tests")
    print("="*70 + "\n")
    
    try:
        test_health()
        test_strategies_list()
        test_visualization()
        
        print("\n" + "="*70)
        print("✅ All tests completed successfully!")
        print("="*70)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server.")
        print("   Make sure the server is running on http://127.0.0.1:8001")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
