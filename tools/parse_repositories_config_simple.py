#!/usr/bin/env python3
"""
Simple script to read repositories configuration without external dependencies.
Uses a simple text-based format instead of YAML for better compatibility.
"""

import argparse
import sys
import os

def load_config(config_file):
    """Load the repositories configuration from a simple text file."""
    repositories = []
    
    try:
        with open(config_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Configuration file {config_file} not found", file=sys.stderr)
        return []
    
    current_repo = {}
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
        
        # Look for repository entries
        if line.startswith('  - url:'):
            # Save previous repo if it exists
            if current_repo:
                repositories.append(current_repo)
            # Start new repo
            url = line.split('url:', 1)[1].strip().strip('"\'')
            current_repo = {'url': url}
        elif line.startswith('    branch:') and current_repo:
            branch = line.split('branch:', 1)[1].strip().strip('"\'')
            current_repo['branch'] = branch
        elif line.startswith('    path:') and current_repo:
            path = line.split('path:', 1)[1].strip().strip('"\'')
            current_repo['path'] = path
    
    # Add the last repository
    if current_repo:
        repositories.append(current_repo)
    
    return repositories

def build_repository_urls(repositories, branch_override=None):
    """Convert repository configurations to URLs expected by create_repository.py."""
    urls = []
    
    for repo in repositories:
        url = repo.get('url', '')
        if not url:
            print("Warning: Repository entry missing URL, skipping", file=sys.stderr)
            continue
            
        # Use branch override if provided, otherwise use configured branch
        branch = branch_override or repo.get('branch', '')
        path = repo.get('path', '')
        
        # Build the URL in the format: REPOSITORY_URL#BRANCH:PATH
        repo_url = url
        if branch:
            repo_url += f"#{branch}"
        if path:
            repo_url += f":{path}"
            
        urls.append(repo_url)
    
    return urls

def main():
    parser = argparse.ArgumentParser(
        description='Generate repository URLs from configuration file')
    parser.add_argument(
        'config_file',
        help='Path to the repositories configuration file')
    parser.add_argument(
        '--branch-override',
        help='Override branch for all repositories (useful for CI/CD)')
    parser.add_argument(
        '--output-format',
        choices=['space-separated', 'newline-separated'],
        default='space-separated',
        help='Output format for the repository URLs')
    
    args = parser.parse_args()
    
    repositories = load_config(args.config_file)
    if not repositories:
        print("No repositories found in configuration", file=sys.stderr)
        return 1
    
    urls = build_repository_urls(repositories, args.branch_override)
    
    if args.output_format == 'space-separated':
        print(' '.join(f'"{url}"' for url in urls))
    else:
        for url in urls:
            print(url)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
