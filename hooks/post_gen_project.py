# This script executes after the project is generated from your cookiecutter.
# Details about hooks can be found in the cookiecutter documentation:
# https://cookiecutter.readthedocs.io/en/latest/advanced/hooks.html
#
# An example of a post-hook would be to remove parts of the project
# directory tree based on some configuration values.

import os
import subprocess
import sys
from cookiecutter.utils import rmtree

class GitRepository(object):
    """ A context for the setup of a Git repository """
    def __init__(self):
        self.remotes = {}

    def __enter__(self):
        # Initialize the git repository
        subprocess.check_call("git init".split())
        subprocess.check_call("git checkout -b main".split())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Finalize by making an initial git commit
        subprocess.check_call("git add *".split())
        subprocess.check_call(["git", "commit", "-m", "Initial Commit"])

    def add_remote(self, name, url):
        if self.remotes.get(name, url) != url:
            sys.stderr.write("Trying to add a remote repository twice with differing URL!")
            sys.exit(1)

        if name not in self.remotes:
            self.remotes[name] = url
            subprocess.check_call(["git", "remote", "add", name, url])

    def add_submodule(self, url, location, branch=None, tag=None):
        command = ["git", "submodule", "add"]
        if branch is not None:
            command = command + ["-b", branch]
        command = command + [url, location]
        subprocess.check_call(command)
        if tag is not None:
            subprocess.check_call(["git", "checkout", tag], cwd=os.path.join(os.getcwd(), *os.path.split(location)))


# Optionally remove files whose existence is tied to disabled features
def conditional_remove(condition, path):
    if condition:
        if os.path.isfile(path):
            os.remove(path)
        else:
            rmtree(path)

# Print a message about success
print("The project {{ cookiecutter.project_slug }} was successfully generated!")
