# Collection of my personal project's documentation

## Integration and Shared Assets

# Documentation Site

This repository contains the centralized documentation site for Diego Barros Araya's projects. It automatically fetches and organizes documentation from multiple repositories.

## Features

- **Automated Documentation Collection**: Fetches documentation from repositories' `/docs` directories
- **Fallback to README**: If no `/docs` directory exists, fetches the repository's README
- **Asset Management**: Downloads and stores images locally for reliable display
- **Jekyll Integration**: Built with Jekyll for GitHub Pages deployment

## How it works

1. **Repository Configuration**: Add repositories to `repos.yaml`
2. **Automated Fetching**: The `fetch_readmes.py` script processes each repository:
   - Checks for a `/docs` directory first
   - Falls back to README.md if no docs directory exists
   - Downloads and processes markdown files and images
3. **Organization**: Creates a structured project directory with proper Jekyll permalinks
4. **Automation**: GitHub Actions runs daily to keep documentation up-to-date

## Repository Structure

```
docs/
├── _config.yml              # Jekyll configuration
├── index.markdown          # Main landing page
├── repos.yaml             # List of repositories to process
├── fetch_readmes.py       # Documentation fetching script
├── projects/              # Generated project documentation
│   ├── repo1/
│   │   ├── index.md      # Main project page
│   │   └── docs/         # Full docs directory (if exists)
│   └── repo2/
│       └── index.md      # README-based page
└── .github/
    └── workflows/
        └── update-docs.yml # Automation workflow
```

## Adding New Projects

1. Add the repository to `repos.yaml`:
   ```yaml
   repos:
     - owner/repository-name
   ```

2. Run the fetch script:
   ```bash
   python3 fetch_readmes.py
   ```

3. The documentation will be automatically organized and available on the site.

## Manual Updates

To manually update the documentation:

```bash
# Install dependencies
pip3 install requests pyyaml

# Run the fetch script
python3 fetch_readmes.py
```

## Integration with Main Website

The documentation system is integrated with the main website (diegobarrosaraya.com), which includes:

- **Resume Generation**: Displays professional resume with PDF export functionality
- **Documentation Links**: Direct links to this centralized documentation
- **Cross-Platform Navigation**: Unified navigation across blog, docs, and main site

## Technical Details

- **Static Site Generator**: Jekyll with Minima theme
- **Deployment**: GitHub Pages
- **Automation**: GitHub Actions for daily updates
- **Asset Handling**: Local image storage with proper path resolution
- **Responsive Design**: Mobile-friendly documentation layout
- [Main site](https://diegobarrosaraya.com/)
- [Blog](https://blog.diegobarrosaraya.com/)

All sites share a unified navigation bar and use a common CSS theme located in the `shared-assets/shared-theme.css` file at the root of the parent repository. This ensures consistent branding and easier updates across all sites.

## Deployment

Deployment is automated using GitHub Actions. On every push to `main`, the site is built with Jekyll and deployed to GitHub Pages. See `.github/workflows/deploy.yml` for details.

## Social Links

Contact and social links are managed via the Jekyll data file `_data/social.yml` for easy updates.

---
For more details, see the main site or blog.
