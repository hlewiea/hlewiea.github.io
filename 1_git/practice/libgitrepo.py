

import configparser
from math import ceil
import os
import re
import sys

class GitIndex (object):
    version = None
    entries = []
    # ext = None
    # sha = None

    def __init__(self, version=2, entries=None):
        if not entries:
            entries = list()

        self.version = version
        self.entries = entries

class GitIndexEntry (object):
    def __init__(self, ctime=None, mtime=None, dev=None, ino=None,
                 mode_type=None, mode_perms=None, uid=None, gid=None,
                 fsize=None, sha=None, flag_assume_valid=None,
                 flag_stage=None, name=None):
      # The last time a file's metadata changed.  This is a pair
      # (timestamp in seconds, nanoseconds)
      self.ctime = ctime
      # The last time a file's data changed.  This is a pair
      # (timestamp in seconds, nanoseconds)
      self.mtime = mtime
      # The ID of device containing this file
      self.dev = dev
      # The file's inode number
      self.ino = ino
      # The object type, either b1000 (regular), b1010 (symlink),
      # b1110 (gitlink).
      self.mode_type = mode_type
      # The object permissions, an integer.
      self.mode_perms = mode_perms
      # User ID of owner
      self.uid = uid
      # Group ID of ownner
      self.gid = gid
      # Size of this object, in bytes
      self.fsize = fsize
      # The object's SHA
      self.sha = sha
      self.flag_assume_valid = flag_assume_valid
      self.flag_stage = flag_stage
      # Name of the object (full path this time!)
      self.name = name
   
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

    def rm_path(self, paths, delete=True, skip_missing=False):
         # Find and read the index
        index = self.read_index()

        worktree = self.worktree + os.sep

        # Make paths absolute
        abspaths = list()
        for path in paths:
            abspath = os.path.abspath(path)
            if abspath.startswith(worktree):
                abspaths.append(abspath)
            else:
                raise Exception("Cannot remove paths outside of worktree: {}".format(paths))

        kept_entries = list()
        remove = list()

        for e in index.entries:
            full_path = os.path.join(self.worktree, e.name)

            if full_path in abspaths:
                remove.append(full_path)
                abspaths.remove(full_path)
            else:
                kept_entries.append(e) # Preserve entry

        if len(abspaths) > 0 and not skip_missing:
            raise Exception("Cannot remove paths not in the index: {}".format(abspaths))

        if delete:
            for path in remove:
                os.unlink(path)

        index.entries = kept_entries
        write_index(repo, index)
        
    def read_index(self) -> GitIndex:
        index_file = self.create_filerepo("index")

        # New repositories have no index!
        if not os.path.exists(index_file):
            return GitIndex()

        with open(index_file, 'rb') as f:
            raw = f.read()

        header = raw[:12]
        signature = header[:4]
        assert signature == b"DIRC" # Stands for "DirCache"
        version = int.from_bytes(header[4:8], "big")
        assert version == 2, "wyag only supports index file version 2"
        count = int.from_bytes(header[8:12], "big")

        entries = list()

        content = raw[12:]
        idx = 0
        for i in range(0, count):
            # Read creation time, as a unix timestamp (seconds since
            # 1970-01-01 00:00:00, the "epoch")
            ctime_s =  int.from_bytes(content[idx: idx+4], "big")
            # Read creation time, as nanoseconds after that timestamps,
            # for extra precision.
            ctime_ns = int.from_bytes(content[idx+4: idx+8], "big")
            # Same for modification time: first seconds from epoch.
            mtime_s = int.from_bytes(content[idx+8: idx+12], "big")
            # Then extra nanoseconds
            mtime_ns = int.from_bytes(content[idx+12: idx+16], "big")
            # Device ID
            dev = int.from_bytes(content[idx+16: idx+20], "big")
            # Inode
            ino = int.from_bytes(content[idx+20: idx+24], "big")
            # Ignored.
            unused = int.from_bytes(content[idx+24: idx+26], "big")
            assert 0 == unused
            mode = int.from_bytes(content[idx+26: idx+28], "big")
            mode_type = mode >> 12
            assert mode_type in [0b1000, 0b1010, 0b1110]
            mode_perms = mode & 0b0000000111111111
            # User ID
            uid = int.from_bytes(content[idx+28: idx+32], "big")
            # Group ID
            gid = int.from_bytes(content[idx+32: idx+36], "big")
            # Size
            fsize = int.from_bytes(content[idx+36: idx+40], "big")
            # SHA (object ID).  We'll store it as a lowercase hex string
            # for consistency.
            sha = format(int.from_bytes(content[idx+40: idx+60], "big"), "040x")
            # Flags we're going to ignore
            flags = int.from_bytes(content[idx+60: idx+62], "big")
            # Parse flags
            flag_assume_valid = (flags & 0b1000000000000000) != 0
            flag_extended = (flags & 0b0100000000000000) != 0
            assert not flag_extended
            flag_stage =  flags & 0b0011000000000000
            # Length of the name.  This is stored on 12 bits, some max
            # value is 0xFFF, 4095.  Since names can occasionally go
            # beyond that length, git treats 0xFFF as meaning at least
            # 0xFFF, and looks for the final 0x00 to find the end of the
            # name --- at a small, and probably very rare, performance
            # cost.
            name_length = flags & 0b0000111111111111

            # We've read 62 bytes so far.
            idx += 62

            if name_length < 0xFFF:
                assert content[idx + name_length] == 0x00
                raw_name = content[idx:idx+name_length]
                idx += name_length + 1
            else:
                print("Notice: Name is 0x{:X} bytes long.".format(name_length))
                # This probably wasn't tested enough.  It works with a
                # path of exactly 0xFFF bytes.  Any extra bytes broke
                # something between git, my shell and my filesystem.
                null_idx = content.find(b'\x00', idx + 0xFFF)
                raw_name = content[idx: null_idx]
                idx = null_idx + 1

            # Just parse the name as utf8.
            name = raw_name.decode("utf8")

            # Data is padded on multiples of eight bytes for pointer
            # alignment, so we skip as many bytes as we need for the next
            # read to start at the right position.

            idx = 8 * ceil(idx / 8)

            # And we add this entry to our list.
            entries.append(GitIndexEntry(ctime=(ctime_s, ctime_ns),
                                        mtime=(mtime_s,  mtime_ns),
                                        dev=dev,
                                        ino=ino,
                                        mode_type=mode_type,
                                        mode_perms=mode_perms,
                                        uid=uid,
                                        gid=gid,
                                        fsize=fsize,
                                        sha=sha,
                                        flag_assume_valid=flag_assume_valid,
                                        flag_stage=flag_stage,
                                        name=name))

        return GitIndex(version=version, entries=entries)
  
class GitIgnore(object):
    absolute = None
    scoped = None

    def __init__(self, absolute, scoped):
        self.absolute = absolute
        self.scoped = scoped


def find_git_repo(path=".") -> GitRepository:
    path = os.path.realpath(path)
    if os.path.isdir(os.path.join(path, ".git")):
        return GitRepository(path)

    # If we haven't returned, recurse in parent, if w
    parent = os.path.realpath(os.path.join(path, ".."))
    if parent == path:
        raise Exception("No git directory.")

    # Recursive case
    return find_git_repo(parent)