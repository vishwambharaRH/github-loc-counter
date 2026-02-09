"""
Main aggregation script that orchestrates the entire counting process.
"""
import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List
from fetch_repos import fetch_user_repos, save_repos_list
from clone_or_fetch import clone_or_update_all


def run_loc_counter() -> Dict[str, int]:
    """
    Run the Rust-based LOC counter on all repositories.
    
    Returns:
        Dictionary mapping language names to line counts
    """
    print("\nCounting lines of code...")
    
    # Check if the Rust binary exists
    engine_path = Path('../engine/loc_runner')
    
    if not engine_path.exists():
        print("Building Rust LOC counter...")
        build_result = subprocess.run(
            ['cargo', 'build', '--release'],
            cwd='../engine',
            capture_output=True,
            text=True
        )
        if build_result.returncode != 0:
            print(f"Error building Rust counter: {build_result.stderr}")
            return {}
    
    # Run the counter from the engine directory with correct relative path
    result = subprocess.run(
        ['./loc_runner', '../aggregator/repos'],
        cwd='../engine',
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Error running LOC counter: {result.stderr}")
        return {}
    
    # Parse the JSON output
    try:
        loc_data = json.loads(result.stdout)
        return loc_data
    except json.JSONDecodeError as e:
        print(f"Error parsing LOC counter output: {e}")
        return {}


def aggregate_and_save(username: str, token: str = None, output_file: str = 'loc_results.json'):
    """
    Complete aggregation pipeline:
    1. Fetch repositories
    2. Clone/update them
    3. Count lines of code
    4. Save results
    """
    print("=== GitHub LOC Counter ===\n")
    
    # Step 1: Fetch repositories
    print("Step 1: Fetching repositories...")
    repos = fetch_user_repos(username, token)
    save_repos_list(repos)
    
    # Step 2: Clone/update repositories
    print("\nStep 2: Cloning/updating repositories...")
    successful_repos = clone_or_update_all()
    
    # Step 3: Count lines of code
    print("\nStep 3: Counting lines of code...")
    loc_data = run_loc_counter()
    
    # Step 4: Save results
    print("\nStep 4: Saving results...")
    results = {
        'username': username,
        'total_repos': len(repos),
        'processed_repos': len(successful_repos),
        'languages': loc_data
    }
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {output_file}")
    print("\nTop 8 languages by LOC:")
    
    # Sort languages by line count
    sorted_langs = sorted(loc_data.items(), key=lambda x: x[1], reverse=True)[:8]
    
    for lang, lines in sorted_langs:
        print(f"  {lang}: {lines:,} lines")
    
    return results


if __name__ == '__main__':
    username = os.environ.get('GITHUB_USERNAME')
    token = os.environ.get('GITHUB_TOKEN')
    
    if not username:
        print("Please set GITHUB_USERNAME environment variable")
        exit(1)
    
    aggregate_and_save(username, token)