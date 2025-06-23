# Repository Configuration

This repository now supports publishing multiple Kodi add-ons from different Git repositories using a configuration file approach.

## Configuration File

The configuration is defined in `repositories-config.yml`. This file contains a list of Git repositories to include in the Kodi repository.

### Format

```yaml
repositories:
  - url: "https://github.com/username/kodi-addon.git"
    branch: "main"  # optional, defaults to repository's default branch
    path: "."       # optional, path within repository, defaults to root

  - url: "https://github.com/username/another-addon.git"
    branch: "release"
    
  - url: "https://github.com/username/third-addon.git"
    # uses default branch and root path
```

### Fields

- **url** (required): The Git repository URL
- **branch** (optional): The branch or tag to use. If not specified, uses the repository's default branch
- **path** (optional): Path within the repository where the add-on is located. Defaults to the root directory "."

## Adding a New Repository

1. Edit `repositories-config.yml`
2. Add a new entry under `repositories:`
3. Commit and push the changes
4. The GitHub Actions workflow will automatically include the new repository in the next build

## How It Works

1. The GitHub Actions workflow reads `repositories-config.yml`
2. The `tools/parse_repositories_config.py` script converts the configuration into URLs in the format expected by `create_repository.py`
3. `create_repository.py` processes all the repositories and generates the Kodi repository structure

## Manual Testing

You can test the configuration locally using:

```bash
# Test the configuration parser
python3 ./tools/parse_repositories_config.py repositories-config.yml --branch-override main

# Run the test script
./test-config.sh
```

## Branch Handling

The workflow automatically uses the current branch being built for all repositories. This means:

- When building from `main` branch, it will use the `main` branch from all configured repositories
- When building from `develop` branch, it will use the `develop` branch from all configured repositories
- If a repository doesn't have the specified branch, the build will fail (which is the desired behavior for consistency)

You can override the branch for specific repositories by setting the `branch` field in the configuration file.

## Current Repositories

The following repositories are currently configured:

- [kodi.plugin.video.angelstudios](https://github.com/brianpatrickreavey/kodi.plugin.video.angelstudios.git)

## Dependencies

The workflow requires:
- Python 3
- GitPython (for cloning repositories)
- PyYAML (for parsing the configuration file)
