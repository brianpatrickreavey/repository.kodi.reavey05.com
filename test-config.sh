#!/bin/bash
# Test script to validate the repository configuration locally

set -e

echo "Testing repository configuration..."

# Test the config parser
echo "1. Testing config parser..."
REPO_URLS=$(python3 ./tools/parse_repositories_config.py repositories-config.yml --branch-override main)
echo "   Generated URLs: $REPO_URLS"

# Test that create_repository.py accepts the URLs (dry run)
echo "2. Testing repository generation (with --help to avoid actual build)..."
python3 ./tools/create_repository.py --help > /dev/null
echo "   create_repository.py is working"

# Show what would be executed
echo "3. Command that would be executed:"
echo "   python3 ./tools/create_repository.py --datadir=./test-output repository.kodi.reavey05.com $REPO_URLS"

echo ""
echo "Configuration validation complete!"
echo ""
echo "To add more repositories, edit repositories-config.yml and add entries like:"
echo "  - url: \"https://github.com/username/repo.git\""
echo "    branch: \"main\""
echo "    # path: \"subfolder\"  # optional"
