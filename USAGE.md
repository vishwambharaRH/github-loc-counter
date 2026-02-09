# Usage Guide

This guide will help you set up and use the GitHub LOC Counter.

## Prerequisites

- Python 3.8+
- Rust/Cargo (install from [rustup.rs](https://rustup.rs/))
- Git
- GitHub Personal Access Token (for API access)

## Quick Start

### 1. Setup

Run the setup script:

```bash
./setup.sh
```

This will:
- Install Python dependencies
- Build the Rust LOC counter
- Verify all requirements are met

### 2. Configure Environment Variables

```bash
export GITHUB_USERNAME='your-github-username'
export GITHUB_TOKEN='your-github-token'
```

**Note:** You can create a GitHub token at https://github.com/settings/tokens
- Only need `public_repo` scope for public repositories
- For private repos, also enable `repo` scope

### 3. Prepare Your README

Add these markers to your GitHub profile README where you want the stats to appear:

```markdown
<!-- LOC-STATS:START -->
<!-- LOC-STATS:END -->
```

### 4. Run the Counter

#### Manual Run

```bash
# Aggregate all data
cd aggregator
python aggregate.py

# Update your README
cd ../updater
python update_readme.py
```

#### Automated with GitHub Actions

The workflow is already configured in `.github/workflows/update.yaml`. It will:
- Run daily at midnight UTC
- Run on manual trigger
- Run when code changes are pushed

To enable:
1. Push this repository to GitHub
2. The workflow will run automatically
3. Check the Actions tab to monitor runs

## Project Structure

```
.
├── aggregator/          # Fetch and clone repositories
│   ├── fetch_repos.py   # Fetch repo list from GitHub API
│   ├── clone_or_fetch.py # Clone/update repositories locally
│   └── aggregate.py     # Main orchestration script
│
├── engine/              # Rust-based LOC counter
│   ├── loc_runner.rs    # Main counting logic
│   ├── ignore_rules.toml # Configuration for what to count
│   └── Cargo.toml       # Rust dependencies
│
├── renderer/            # Generate output formats
│   ├── badge.py         # shields.io badge URLs
│   ├── markdown.py      # Markdown tables and sections
│   └── svg_card.py      # Custom SVG cards
│
└── updater/             # Update README
    ├── update_readme.py # Main updater script
    └── cache.json       # Cache previous results
```

## Customization

### Change Languages to Track

Edit `engine/ignore_rules.toml`:

```toml
[languages]
YourLanguage = [".ext1", ".ext2"]
```

### Change Number of Languages Displayed

Most scripts accept a `top_n` parameter (default: 8):

```python
generate_compact_section(loc_data, top_n=10)
```

### Change Section Style

The updater supports two styles:

```bash
# Compact style (badges only)
export SECTION_TYPE='compact'

# Full style (badges + table)
export SECTION_TYPE='full'
```

### Customize Badge Style

Edit `renderer/badge.py`:

```python
# Available styles: flat, flat-square, plastic, for-the-badge, social
generate_badge_url(language, lines, style='for-the-badge')
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GITHUB_USERNAME` | Your GitHub username | Required |
| `GITHUB_TOKEN` | GitHub personal access token | Optional (higher rate limits) |
| `README_PATH` | Path to your README file | `../README.md` |
| `SECTION_TYPE` | Section style (`compact` or `full`) | `compact` |
| `GENERATE_SVG` | Generate SVG card (`true` or `false`) | `true` |

## Outputs

The system generates several outputs:

1. **repos.json** - List of your repositories
2. **loc_results.json** - Complete LOC statistics
3. **Updated README.md** - Your README with stats inserted
4. **loc_stats.svg** - Custom SVG stats card (optional)
5. **cache.json** - Cached results with timestamp

## Troubleshooting

### "Error 403: API rate limit exceeded"

- Add a GitHub token: `export GITHUB_TOKEN='your-token'`
- Authenticated requests have much higher rate limits

### "Rust binary not found"

```bash
cd engine
cargo build --release
cp target/release/loc_runner ./loc_runner
```

### "Markers not found in README"

Make sure you've added the markers:
```markdown
<!-- LOC-STATS:START -->
<!-- LOC-STATS:END -->
```

### Stats not updating in GitHub Actions

1. Check the Actions tab for error logs
2. Ensure `GITHUB_TOKEN` is available (it should be automatic)
3. Verify the workflow has write permissions

## Advanced Usage

### Run Only Specific Steps

```bash
# Just fetch repos
cd aggregator
python fetch_repos.py

# Just clone/update repos
python clone_or_fetch.py

# Just count LOC (requires repos to be cloned)
cd ../engine
./loc_runner ../aggregator/repos > ../aggregator/loc_results.json
```

### Generate Only SVG Card

```python
from renderer.svg_card import save_svg_card

loc_data = {
    'Python': 15000,
    'JavaScript': 8000,
    # ...
}

save_svg_card(loc_data, 'my_stats.svg', 'your-username')
```

### Generate Only Badges

```python
from renderer.markdown import generate_badge_section

badges = generate_badge_section(loc_data, top_n=5)
print(badges)
```

## Performance

- **Initial run**: May take 5-15 minutes depending on repository count
- **Subsequent runs**: 1-3 minutes (only pulls changes)
- **Rust counter**: Processes ~100k LOC per second

## Privacy & Security

- Only processes public repositories by default
- Excludes forks and archived repos
- GitHub token is only used for API access
- All processing is local (or in your GitHub Actions)

## Contributing

Found a bug or want to improve something? Raise an issue!

## License

This is a personal project, but feel free to use it however you like.

Live long and prosper! 🖖