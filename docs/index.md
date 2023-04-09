# Overview

Network config tracker is a tool that monitors the configuration changes of your network devices using a gitlab repository. This tool requires integration to the following applications:

- [Gitlab](https://about.gitlab.com/) which is used for storing the network devices configuration and to monitor the configuration changes.
- [NetBox](https://github.com/netbox-community/netbox) which is used for maintaining the list of network devices to be monitored for configuration changes.

## Installation

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Code Logic

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

## Usage
