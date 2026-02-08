#!/bin/bash
# Run the complete LOC counter pipeline

set -e

echo "======================================"
echo "  GitHub LOC Counter - Full Pipeline"
echo "======================================"
echo ""

# Check environment variables
if [ -z "$GITHUB_USERNAME" ]; then
    echo "Error: GITHUB_USERNAME environment variable not set"
    echo "Usage: export GITHUB_USERNAME='your-username'"
    exit 1
fi

# Configuration
README_PATH="${README_PATH:-./README.md}"
SECTION_TYPE="${SECTION_TYPE:-compact}"
GENERATE_SVG="${GENERATE_SVG:-true}"

echo "Configuration:"
echo "  Username: $GITHUB_USERNAME"
echo "  README: $README_PATH"
echo "  Style: $SECTION_TYPE"
echo "  Generate SVG: $GENERATE_SVG"
echo ""

# Step 1: Aggregation
echo "Step 1/2: Counting lines of code..."
cd aggregator
python aggregate.py
cd ..

# Step 2: Update README
echo ""
echo "Step 2/2: Updating README..."
cd updater
export README_PATH="../$README_PATH"
export SECTION_TYPE
export GENERATE_SVG
python update_readme.py
cd ..

echo ""
echo "======================================"
echo "  ✓ Complete!"
echo "======================================"
echo ""
echo "Your README has been updated at: $README_PATH"

if [ "$GENERATE_SVG" = "true" ]; then
    echo "SVG card saved to: updater/loc_stats.svg"
fi

echo ""
echo "Results cached in: updater/cache.json"
echo ""