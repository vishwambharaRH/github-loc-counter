"""
Update GitHub profile README with LOC statistics.
"""
import json
import os
import re
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory to path to import renderer modules (insert at beginning to prioritize)
sys.path.insert(0, str(Path(__file__).parent.parent / 'renderer'))

from markdown import generate_compact_section, generate_full_section
from svg_card import save_svg_card


# Markers for identifying the section to update
START_MARKER = "<!-- LOC-STATS:START -->"
END_MARKER = "<!-- LOC-STATS:END -->"


def load_loc_results(results_file: str = '../aggregator/loc_results.json') -> dict:
    """Load the LOC counting results."""
    with open(results_file, 'r') as f:
        return json.load(f)


def update_cache(results: dict, cache_file: str = 'cache.json'):
    """Update the cache with latest results."""
    cache = {
        'last_update': datetime.now().isoformat(),
        'languages': results['languages'],
        'total_lines': sum(results['languages'].values()),
        'repos_processed': results['processed_repos']
    }
    
    with open(cache_file, 'w') as f:
        json.dump(cache, f, indent=2)
    
    print(f"Cache updated: {cache['total_lines']:,} total lines")


def update_readme(
    readme_path: str,
    loc_data: dict,
    section_type: str = 'compact',
    username: str = 'User'
) -> bool:
    """
    Update the README file with LOC statistics.
    
    Args:
        readme_path: Path to the README.md file
        loc_data: Language statistics dictionary
        section_type: 'compact' or 'full'
        username: GitHub username for the SVG card
    
    Returns:
        True if updated, False if markers not found
    """
    readme_path = Path(readme_path)
    
    if not readme_path.exists():
        print(f"README not found at {readme_path}")
        return False
    
    # Read current README
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if markers exist
    if START_MARKER not in content or END_MARKER not in content:
        print("Markers not found in README. Please add the following lines where you want the stats:")
        print(START_MARKER)
        print(END_MARKER)
        return False
    
    # Generate new section
    if section_type == 'compact':
        new_section = generate_compact_section(loc_data)
    else:
        new_section = generate_full_section(loc_data)
    
    # Replace the section between markers
    pattern = f"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}"
    replacement = f"{START_MARKER}\n{new_section}\n{END_MARKER}"
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Write updated README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"README updated at {readme_path}")
    return True


def generate_svg(loc_data: dict, username: str, output_dir: str = '.'):
    """Generate SVG card and save it."""
    output_path = Path(output_dir) / 'loc_stats.svg'
    save_svg_card(loc_data, str(output_path), username)


def main():
    """Main update workflow."""
    print("=== README Updater ===\n")
    
    # Get configuration from environment
    readme_path = os.environ.get('README_PATH', '../README.md')
    username = os.environ.get('GITHUB_USERNAME', 'User')
    section_type = os.environ.get('SECTION_TYPE', 'compact')
    generate_svg_flag = os.environ.get('GENERATE_SVG', 'true').lower() == 'true'
    
    # Load results
    print("Loading LOC results...")
    try:
        results = load_loc_results()
        loc_data = results['languages']
    except FileNotFoundError:
        print("Error: loc_results.json not found. Run aggregation first.")
        return
    except Exception as e:
        print(f"Error loading results: {e}")
        return
    
    # Update cache
    print("Updating cache...")
    update_cache(results)
    
    # Update README
    print(f"Updating README at {readme_path}...")
    if update_readme(readme_path, loc_data, section_type, username):
        print("✓ README updated successfully")
    else:
        print("✗ Failed to update README")
    
    # Generate SVG if requested
    if generate_svg_flag:
        print("Generating SVG card...")
        generate_svg(loc_data, username)
        print("✓ SVG card generated")
    
    print("\n=== Update Complete ===")


if __name__ == '__main__':
    main()