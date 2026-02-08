"""
Generate badge URLs for displaying language statistics.
Uses shields.io for badge generation.
"""
from urllib.parse import quote
from typing import Dict


def format_number(num: int) -> str:
    """Format large numbers with K/M suffixes."""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return str(num)


def get_language_color(language: str) -> str:
    """Get the standard color for a programming language."""
    colors = {
        'Python': '3776AB',
        'JavaScript': 'F7DF1E',
        'TypeScript': '3178C6',
        'Rust': 'DEA584',
        'Go': '00ADD8',
        'Java': 'B07219',
        'C': 'A8B9CC',
        'C++': 'F34B7D',
        'C#': '239120',
        'Ruby': 'CC342D',
        'PHP': '777BB4',
        'Swift': 'F05138',
        'Kotlin': 'A97BFF',
        'Shell': '89E051',
        'HTML': 'E34C26',
        'CSS': '563D7C',
        'Vue': '4FC08D',
        'Dart': '00B4AB',
    }
    return colors.get(language, '555555')


def generate_badge_url(language: str, lines: int, style: str = 'flat-square') -> str:
    """
    Generate a shields.io badge URL for a language.
    
    Args:
        language: Programming language name
        lines: Number of lines of code
        style: Badge style (flat, flat-square, plastic, etc.)
    
    Returns:
        shields.io badge URL
    """
    label = quote(language)
    message = quote(f"{format_number(lines)} lines")
    color = get_language_color(language)
    
    return f"https://img.shields.io/badge/{label}-{message}-{color}?style={style}"


def generate_all_badges(loc_data: Dict[str, int], top_n: int = 8, style: str = 'flat-square') -> Dict[str, str]:
    """
    Generate badge URLs for the top N languages.
    
    Returns:
        Dictionary mapping language names to badge URLs
    """
    sorted_langs = sorted(loc_data.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    badges = {}
    for lang, lines in sorted_langs:
        badges[lang] = generate_badge_url(lang, lines, style)
    
    return badges


if __name__ == '__main__':
    # Example usage
    sample_data = {
        'Python': 15000,
        'JavaScript': 8500,
        'TypeScript': 6200,
        'Rust': 4100,
    }
    
    badges = generate_all_badges(sample_data)
    for lang, url in badges.items():
        print(f"{lang}: {url}")