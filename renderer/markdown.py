"""
Generate markdown tables and sections for GitHub README.
"""
from typing import Dict
from badge import generate_badge_url, format_number


def generate_markdown_table(loc_data: Dict[str, int], top_n: int = 8) -> str:
    """
    Generate a markdown table with language statistics.
    
    Args:
        loc_data: Dictionary mapping languages to line counts
        top_n: Number of top languages to include
    
    Returns:
        Markdown formatted table
    """
    sorted_langs = sorted(loc_data.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    total_lines = sum(loc_data.values())
    
    # Build the table
    lines = [
        "| Language | Lines of Code | Percentage |",
        "|----------|---------------|------------|"
    ]
    
    for lang, count in sorted_langs:
        percentage = (count / total_lines * 100) if total_lines > 0 else 0
        lines.append(f"| {lang} | {count:,} | {percentage:.1f}% |")
    
    return "\n".join(lines)


def generate_badge_section(loc_data: Dict[str, int], top_n: int = 8) -> str:
    """
    Generate a section with badge images for languages.
    
    Returns:
        Markdown with badge images
    """
    sorted_langs = sorted(loc_data.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    badges = []
    for lang, lines in sorted_langs:
        badge_url = generate_badge_url(lang, lines)
        badges.append(f"![{lang}]({badge_url})")
    
    # Return badges with some spacing
    return " ".join(badges)


def generate_full_section(loc_data: Dict[str, int], top_n: int = 8, include_table: bool = True) -> str:
    """
    Generate a complete README section with badges and optionally a table.
    
    Returns:
        Complete markdown section
    """
    total_lines = sum(loc_data.values())
    
    sections = [
        "## 📊 Coding Statistics",
        "",
        f"**Total Lines of Code:** {total_lines:,}",
        "",
        "### Top Languages",
        "",
        generate_badge_section(loc_data, top_n),
    ]
    
    if include_table:
        sections.extend([
            "",
            "### Detailed Breakdown",
            "",
            generate_markdown_table(loc_data, top_n),
        ])
    
    return "\n".join(sections)


def generate_compact_section(loc_data: Dict[str, int], top_n: int = 8) -> str:
    """
    Generate a compact section with just badges and total count.
    Perfect for inserting into an existing README.
    """
    total_lines = sum(loc_data.values())
    sorted_langs = sorted(loc_data.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    sections = [
        "### 💻 Lines of Code",
        "",
        generate_badge_section(loc_data, top_n),
        "",
        f"*Total: {total_lines:,} lines across {len(loc_data)} languages*"
    ]
    
    return "\n".join(sections)


if __name__ == '__main__':
    # Example usage
    sample_data = {
        'Python': 15234,
        'JavaScript': 8521,
        'TypeScript': 6234,
        'Rust': 4123,
        'Go': 2341,
        'HTML': 1823,
        'CSS': 1234,
        'Shell': 567,
    }
    
    print(generate_full_section(sample_data))
    print("\n" + "="*50 + "\n")
    print(generate_compact_section(sample_data))