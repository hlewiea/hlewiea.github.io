

import configparser
import os

   
class GitRepository(object):
    """A git repository"""

    worktree = None
    gitdir = None
    conf = None

    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")
        
        # load .git/configuration file
        self.conf = configparser.ConfigParser()
        config_file  = self.create_filerepo("config")
        
        if force:
            return
        if not os.path.isdir(self.gitdir):
            raise Exception("Not a Git repository %s" % path)
        if not os.path.exists(config_file):
            raise Exception("Config file missing %s" % config_file)

        self.conf.read([config_file])
        vers = int(self.conf.get("core", "repositoryformatversion"))
        if vers != 0:
            raise Exception("Unsupported repositoryformatversion %s" % vers)

    
    def init_repo(self, path):
        """Create a new repository at path."""
        # makesure gitdir is empty (which is already create in init)
        if os.path.exists(self.gitdir) and os.listdir(self.gitdir):
            raise Exception("%s is not empty!" % self.gitdir)
        # .git/branches, .git/objects, .git/refs/tags, .git/refs/heads
        assert self.create_repo("branches", mkdir=True)
        assert self.create_repo("objects", mkdir=True)
        assert self.create_repo("refs", "tags", mkdir=True)
        assert self.create_repo("refs", "heads", mkdir=True)
        # .git/description
        with open(self.create_filerepo("description"), "w") as f:
            f.write("Unnamed repository; edit this file 'description' to name the repository.\n")
        # .git/HEAD
        with open(self.create_filerepo("HEAD"), "w") as f:
            f.write("ref: refs/heads/master\n")
        # .git/config
        with open(self.create_filerepo("config"), "w") as f:
            self.repo_default_config()
            self.conf.write(f)

    def repo_default_config(self):
        self.conf.add_section("core")
        self.conf.set("core", "repositoryformatversion", "0")
        self.conf.set("core", "filemode", "false")
        self.conf.set("core", "bare", "false")
    
    def create_filerepo(self, *path, mkdir=False):
        """Same as repo_path, but create dirname(*path) if absent.  For
        example, create_filerepo(r, \"refs\", \"remotes\", \"origin\", \"HEAD\") will create
        .git/refs/remotes/origin."""

        if self.create_repo(*path[:-1], mkdir=mkdir):
            return os.path.join(self.gitdir, *path)

    def create_repo(self, *path, mkdir=False):
        """Same as repo_path, but mkdir *path if absent if mkdir."""
        path = os.path.join(self.gitdir, *path)
        
        if not os.path.exists(path):
            if mkdir:
                os.makedirs(path)
                return path
            return None
            
        if os.path.isdir(path):
            return path
        else:
            raise Exception("Not a directory %s" % path)

def find_git_repo(path="."):
    path = os.path.realpath(path)
    if os.path.isdir(os.path.join(path, ".git")):
        return GitRepository(path)

    # If we haven't returned, recurse in parent, if w
    parent = os.path.realpath(os.path.join(path, ".."))
    if parent == path:
        raise Exception("No git directory.")

    # Recursive case
    return find_git_repo(parent)