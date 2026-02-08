#!/usr/bin/env python3
"""
Test script to verify all components work without actual GitHub API calls.
"""
import json
import sys
from pathlib import Path

# Add renderer to path
sys.path.append(str(Path(__file__).parent / 'renderer'))

from renderer.badge import generate_all_badges
from renderer.markdown import generate_full_section, generate_compact_section
from renderer.svg_card import save_svg_card


def test_with_sample_data():
    """Test all renderers with sample data."""
    
    sample_data = {
        'Python': 25678,
        'JavaScript': 18234,
        'TypeScript': 15432,
        'Rust': 8921,
        'Go': 6543,
        'HTML': 4321,
        'CSS': 3210,
        'Shell': 1234,
        'Java': 987,
        'Ruby': 567,
    }
    
    print("=== GitHub LOC Counter Test ===\n")
    
    # Test badge generation
    print("1. Testing badge generation...")
    badges = generate_all_badges(sample_data)
    print(f"   ✓ Generated {len(badges)} badges")
    
    # Test markdown generation
    print("\n2. Testing markdown generation...")
    compact = generate_compact_section(sample_data)
    full = generate_full_section(sample_data)
    print(f"   ✓ Generated compact section ({len(compact)} chars)")
    print(f"   ✓ Generated full section ({len(full)} chars)")
    
    # Test SVG generation
    print("\n3. Testing SVG card generation...")
    output_file = 'test_loc_stats.svg'
    save_svg_card(sample_data, output_file, username="TestUser")
    print(f"   ✓ Generated SVG card: {output_file}")
    
    # Display output examples
    print("\n" + "="*60)
    print("COMPACT SECTION OUTPUT:")
    print("="*60)
    print(compact)
    
    print("\n" + "="*60)
    print("FULL SECTION OUTPUT:")
    print("="*60)
    print(full)
    
    print("\n" + "="*60)
    print("BADGE URLS:")
    print("="*60)
    for lang, url in list(badges.items())[:3]:
        print(f"{lang}: {url}")
    
    print("\n✓ All tests passed!")
    print(f"\nGenerated files:")
    print(f"  - {output_file}")
    
    return True


if __name__ == '__main__':
    try:
        test_with_sample_data()
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)