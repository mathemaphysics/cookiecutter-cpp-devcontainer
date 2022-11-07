# Welcome to VS Code Devcontainer Cookiecutter!

This repository is a template repository (a cookiecutter) that allows you to quickly
set up new development containers for VS Code. [Devcontainer repository](https://github.com/mathemaphysics/cookiecutter-devcontainer.git).

# Features

The core features of our VS Code Devcontainer Cookiecutter in a nutshell:

* Very simple means of choosing SSH credentials mapping from ${HOME}
* Easy to use graphical interfaces from within the development container
* Compatible with WSL X11/Xorg containment versus native Linux (Debian/Ubuntu)
* Allow you to configure a devcontainer for docker-in-docker functionality

# Using VS Code Devcontainer Cookiecutter

Simply run the cookiecutter command line interface:

```
cookiecutter gh:mathemaphysics/cookiecutter-devcontainer
```

This will start an interactive prompt that will configure and generate your project.
One of the prompts will ask you for a remote repository URL, so you should head to
the Git hosting service of your choice and add a new empty repository e.g. [on Github](https://github.com/new).

# Configuration

If you are using `cookiecutter-devcontainer` a lot, you can customize your default values
by providing a `.cookiecutterrc` file in your home directory, for more details see the
[cookiecutter documentation](https://cookiecutter.readthedocs.io/en/latest/advanced/user_config.html).

# Issues

Please report any issues you might have with template using [the Github issue
tracker](https://github.com/mathemaphysics/cookiecutter-devcontainer/issues)
