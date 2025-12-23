import argparse
import requests
import yaml
import sys
import os
import json


def load_config(config_file):
    """Load the repositories configuration from a YAML file."""
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
            return config.get('addons', [])
    except FileNotFoundError:
        print(f"Configuration file not found: {config_file}", file=sys.stderr)
        return []
    except yaml.YAMLError as e:
        print(f"Error parsing YAML configuration: {e}", file=sys.stderr)
        return []

def get_latest_release_tag(repo, headers=None):
    """Get the latest release tag from GitHub API for the given repository."""
    url = f'https://api.github.com/repos/{repo}/releases/latest'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get('tag_name')

def download_addon_zip(repo, tag, zip_name, output_dir):
    """Download the addon ZIP from GitHub releases."""
    url = f"https://github.com/{repo}/releases/download/{tag}/{zip_name}-{tag}.zip"
    output_path = os.path.join(output_dir, f"{zip_name}-{tag}.zip")
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, 'wb') as f:
        f.write(response.content)
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download addon ZIPs based on repository configuration.")
    parser.add_argument("config_file", help="Path to the repositories configuration YAML file.")
    args = parser.parse_args()

    config_file = args.config_file
    addons = load_config(config_file)
    print(f"Loaded {len(addons)} addons from configuration.")
    print(json.dumps(addons, indent=2))

    env_addon_name = os.getenv('ADDON')
    env_tag = os.getenv('TAG')

    processing_list = []
    if env_addon_name and env_tag:
        print("Using addon name and tag from environment variables.")
        if env_addon_name not in addons.keys():
            print(f"Error: Addon '{env_addon_name}' not found in configuration.", file=sys.stderr)
            sys.exit(1)
        processing_list.append((env_addon_name, env_tag))
    elif env_addon_name or env_tag:
        print("Error: Both ADDON and TAG environment variables must be set to download a specific addon.", file=sys.stderr)
        sys.exit(1)
    else:
        print("No addon name and tag specified.  Processing latest tag for all addons.")
        token = os.getenv('GITHUB_TOKEN')
        headers = {'Authorization': f'token {token}'} if token else {}
        for addon_name in addons.keys():
            repo = addons[addon_name].get('repo')
            try:
                tag = get_latest_release_tag(repo, headers=headers)
            except requests.HTTPError as e:
                print(f"Error fetching latest release for {addon_name} ({repo}): {e}", file=sys.stderr)
                continue
            print(f"Adding repo to processing list: {(addon_name, tag)}")
            processing_list.append((addon_name, tag))

    output_dir = "addon_zips"
    os.makedirs(output_dir, exist_ok=True)
    zip_paths = []
    for addon_name, tag in processing_list:
        print(f"Downloading {addon_name} at tag {tag}")
        download_path = download_addon_zip(
            addons[addon_name].get('repo'),
            tag,
            addons[addon_name].get('zip_name'),
            output_dir
            )
        print(f"Downloaded to {download_path}")
        zip_paths.append(download_path)

    print(*zip_paths, sep=' ')