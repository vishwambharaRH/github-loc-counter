"""
Fetch all repositories from a GitHub user account.
Excludes forks and archived repositories as per requirements.
"""
import os
import requests
from typing import List, Dict
import json


def fetch_user_repos(username: str, token: str = None) -> List[Dict]:
    """
    Fetch all repositories for a given GitHub user.
    
    Args:
        username: GitHub username
        token: GitHub personal access token (optional, for higher rate limits)
    
    Returns:
        List of repository dictionaries
    """
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    repos = []
    page = 1
    per_page = 100
    
    while True:
        url = f'https://api.github.com/users/{username}/repos'
        params = {
            'page': page,
            'per_page': per_page,
            'type': 'owner',  # Only repos owned by user, not contributed to
            'sort': 'updated',
            'direction': 'desc'
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching repos: {response.status_code}")
            print(response.text)
            break
        
        page_repos = response.json()
        
        if not page_repos:
            break
        
        # Filter out forks and archived repos
        filtered_repos = [
            repo for repo in page_repos
            if not repo['fork'] and not repo['archived']
        ]
        
        repos.extend(filtered_repos)
        page += 1
    
    print(f"Found {len(repos)} repositories (excluding forks and archived)")
    return repos


def save_repos_list(repos: List[Dict], output_file: str = 'repos.json'):
    """Save the list of repositories to a JSON file."""
    with open(output_file, 'w') as f:
        json.dump(repos, f, indent=2)
    print(f"Saved {len(repos)} repositories to {output_file}")


if __name__ == '__main__':
    # Get username and token from environment variables
    username = os.environ.get('GITHUB_USERNAME')
    token = os.environ.get('GITHUB_TOKEN')
    
    if not username:
        print("Please set GITHUB_USERNAME environment variable")
        exit(1)
    
    repos = fetch_user_repos(username, token)
    save_repos_list(repos)