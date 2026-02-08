#!/bin/bash
# Setup script for GitHub LOC Counter

set -e

echo "=== GitHub LOC Counter Setup ==="
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

echo "✓ Python 3 found"

# Check for Rust/Cargo
if ! command -v cargo &> /dev/null; then
    echo "Error: Rust/Cargo is required but not installed."
    echo "Install from: https://rustup.rs/"
    exit 1
fi

echo "✓ Rust/Cargo found"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Build Rust LOC counter
echo ""
echo "Building Rust LOC counter..."
cd engine
cargo build --release
cp target/release/loc_runner ./loc_runner
cd ..

echo ""
echo "✓ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Set environment variables:"
echo "   export GITHUB_USERNAME='your-username'"
echo "   export GITHUB_TOKEN='your-personal-access-token'"
echo ""
echo "2. Add markers to your README.md where you want stats:"
echo "   <!-- LOC-STATS:START -->"
echo "   <!-- LOC-STATS:END -->"
echo ""
echo "3. Run the aggregator:"
echo "   cd aggregator && python aggregate.py"
echo ""
echo "4. Update your README:"
echo "   cd updater && python update_readme.py"
echo ""