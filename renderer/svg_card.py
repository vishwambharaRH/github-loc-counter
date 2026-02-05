"""
Generate custom SVG cards for displaying LOC statistics.
Similar to github-readme-stats style.
"""
from typing import Dict, List, Tuple
from badge import format_number, get_language_color


def generate_language_bar(
    languages: List[Tuple[str, int]],
    total: int,
    width: int = 300
) -> str:
    """Generate an SVG language usage bar."""
    if total == 0:
        return ""
    
    bars = []
    x_offset = 0
    
    for lang, count in languages:
        percentage = (count / total) * 100
        bar_width = (count / total) * width
        color = f"#{get_language_color(lang)}"
        
        if bar_width < 1:  # Skip very small bars
            continue
        
        bars.append(
            f'<rect x="{x_offset}" y="0" width="{bar_width}" height="8" '
            f'fill="{color}" rx="2"/>'
        )
        x_offset += bar_width
    
    return "\n      ".join(bars)


def generate_language_list(languages: List[Tuple[str, int]], total: int) -> str:
    """Generate SVG text elements for language list."""
    items = []
    y_offset = 0
    
    for i, (lang, count) in enumerate(languages):
        percentage = (count / total) * 100 if total > 0 else 0
        color = f"#{get_language_color(lang)}"
        
        items.append(f'''
    <g transform="translate(0, {y_offset})">
      <circle cx="5" cy="6" r="5" fill="{color}"/>
      <text x="15" y="10" class="lang-name">{lang}</text>
      <text x="280" y="10" class="lang-percent" text-anchor="end">{percentage:.1f}%</text>
      <text x="440" y="10" class="lang-lines" text-anchor="end">{format_number(count)} lines</text>
    </g>''')
        y_offset += 25
    
    return "\n".join(items)


def generate_svg_card(
    loc_data: Dict[str, int],
    username: str = "User",
    top_n: int = 8,
    width: int = 495,
    title: str = "Code Statistics"
) -> str:
    """
    Generate a complete SVG card with language statistics.
    
    Args:
        loc_data: Dictionary mapping languages to line counts
        username: GitHub username
        top_n: Number of languages to display
        width: Card width in pixels
        title: Card title
    
    Returns:
        Complete SVG as a string
    """
    sorted_langs = sorted(loc_data.items(), key=lambda x: x[1], reverse=True)[:top_n]
    total_lines = sum(loc_data.values())
    
    # Calculate card height based on content
    header_height = 80
    bar_height = 30
    list_height = len(sorted_langs) * 25 + 20
    padding = 20
    height = header_height + bar_height + list_height + padding
    
    language_bar = generate_language_bar(sorted_langs, total_lines, width - 40)
    language_list = generate_language_list(sorted_langs, total_lines)
    
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" 
     xmlns="http://www.w3.org/2000/svg" role="img" 
     aria-labelledby="descId">
  <title id="titleId">{title}</title>
  <desc id="descId">Lines of code statistics for {username}</desc>
  
  <style>
    .header {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #2f80ed }}
    .stat-value {{ font: 600 20px 'Segoe UI', Ubuntu, Sans-Serif; fill: #333 }}
    .stat-label {{ font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #666 }}
    .lang-name {{ font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #333 }}
    .lang-percent {{ font: 400 11px 'Segoe UI', Ubuntu, Sans-Serif; fill: #666 }}
    .lang-lines {{ font: 400 11px 'Segoe UI', Ubuntu, monospace; fill: #666 }}
  </style>
  
  <rect width="{width}" height="{height}" fill="#fffefe" rx="4.5" stroke="#e4e2e2" stroke-width="1"/>
  
  <g transform="translate(20, 25)">
    <text x="0" y="0" class="header">{title}</text>
    
    <g transform="translate(0, 30)">
      <text x="0" y="0" class="stat-label">Total Lines of Code</text>
      <text x="0" y="20" class="stat-value">{total_lines:,}</text>
    </g>
    
    <g transform="translate(0, 70)">
      <text x="0" y="0" class="stat-label">Language Distribution</text>
      <g transform="translate(0, 15)">
        {language_bar}
      </g>
    </g>
    
    <g transform="translate(0, 110)">
      {language_list}
    </g>
  </g>
</svg>'''
    
    return svg


def save_svg_card(
    loc_data: Dict[str, int],
    output_file: str = "loc_card.svg",
    username: str = "User",
    top_n: int = 8
):
    """Generate and save SVG card to a file."""
    svg = generate_svg_card(loc_data, username, top_n)
    
    with open(output_file, 'w') as f:
        f.write(svg)
    
    print(f"SVG card saved to {output_file}")


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
    
    save_svg_card(sample_data, username="YourGitHub")