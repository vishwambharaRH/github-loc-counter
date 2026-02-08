"""
Clone or update repositories locally for analysis.
"""
import os
import json
import subprocess
from pathlib import Path
from typing import List, Dict


REPOS_DIR = Path('repos')


def ensure_repos_dir():
    """Create the repos directory if it doesn't exist."""
    REPOS_DIR.mkdir(exist_ok=True)


def clone_or_update_repo(repo: Dict) -> bool:
    """
    Clone a repository if it doesn't exist, otherwise pull latest changes.
    
    Args:
        repo: Repository dictionary from GitHub API
    
    Returns:
        True if successful, False otherwise
    """
    repo_name = repo['name']
    repo_url = repo['clone_url']
    repo_path = REPOS_DIR / repo_name
    
    try:
        if repo_path.exists():
            print(f"Updating {repo_name}...")
            result = subprocess.run(
                ['git', '-C', str(repo_path), 'pull'],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode != 0:
                print(f"  Warning: Failed to update {repo_name}")
                print(f"  {result.stderr}")
                return False
        else:
            print(f"Cloning {repo_name}...")
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', repo_url, str(repo_path)],
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.returncode != 0:
                print(f"  Error: Failed to clone {repo_name}")
                print(f"  {result.stderr}")
                return False
        
        return True
    except subprocess.TimeoutExpired:
        print(f"  Timeout while processing {repo_name}")
        return False
    except Exception as e:
        print(f"  Error processing {repo_name}: {e}")
        return False


def clone_or_update_all(repos_file: str = 'repos.json') -> List[str]:
    """
    Clone or update all repositories from the repos list.
    
    Returns:
        List of successfully processed repository names
    """
    ensure_repos_dir()
    
    with open(repos_file, 'r') as f:
        repos = json.load(f)
    
    successful = []
    
    for repo in repos:
        if clone_or_update_repo(repo):
            successful.append(repo['name'])
    
    print(f"\nSuccessfully processed {len(successful)}/{len(repos)} repositories")
    return successful


if __name__ == '__main__':
    clone_or_update_all()