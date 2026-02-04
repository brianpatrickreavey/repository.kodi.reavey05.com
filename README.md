# respository.kodi.reavey05.com
KODI Addons

# Current status
Building out the framework to publish to GitHub Pages under repository.kodi.reavey05.com

* repository.kodi.reavey05.com CNAME to brianpatrickreavey.github.io
* Built using the directions here: https://kodi.wiki/view/Add-on_repositories#Repository_Tools
* **Multi-repository support**: Now supports publishing multiple Kodi add-ons from different Git repositories using `repositories-config.yml`

## Adding New Add-ons

To add a new Kodi add-on to this repository:

1. Edit `repositories-config.yml`
2. Add your addon configuration with the GitHub repository details
3. In your addon repository, set up a workflow that dispatches to this repository on releases (using `repository_dispatch` event with type `addon-release` and payload containing `addon` and `tag`)
4. Commit and push changes to `repositories-config.yml` - the repository will be automatically rebuilt with all addons

See `REPOSITORIES.md` for detailed configuration instructions.





# WORKING

Desired workflow:

* publish to feature branch for local testing
* push to branch for automated testing?
* merge to develop - should create a release with a `#.#.#-develop` tag
* merge to main - should create a release with `#.#.#` matching the last tagged
  develop branch


Trunk-based:
* get rid of `develop`
* small branch for a feature
* merge back in (autotag as RC?)
* tag with release if we're happy with it (???)
* tagging triggers the publishing workflow




