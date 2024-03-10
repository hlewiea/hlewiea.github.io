import collections


class GitObject(object):
    def __init__(self, data=None):
        if data != None:
            self.deserialize(data)
        else:
            self.init()

    def serialize(self, repo):
        """This function MUST be implemented by subclasses.
        It must read the object's contents from self.data, a byte string, and do
        whatever it takes to convert it into a meaningful representation.  What exactly that means depend on each subclass."""
        raise Exception("Unimplemented!")

    def deserialize(self, data):
        raise Exception("Unimplemented!")

    def init(self):
        pass # Just do nothing. This is a reasonable default!
    
class GitBlob(GitObject):
    fmt=b'blob'

    def serialize(self):
        return self.blobdata

    def deserialize(self, data):
        self.blobdata = data
        
class GitCommit(GitObject):
    fmt=b'commit'

    def deserialize(self, data):
        self.kvlm = self.kvlm_parse(data)

    def serialize(self):
        return self.kvlm_serialize(self.kvlm)

    def init(self):
        self.kvlm = dict()
        
    def kvlm_parse(self, raw, start=0, dct=None):
        if not dct:
            dct = collections.OrderedDict()
            # You CANNOT declare the argument as dct=OrderedDict() or all
            # call to the functions will endlessly grow the same dict.

        # This function is recursive: it reads a key/value pair, then call
        # itself back with the new position.  So we first need to know
        # where we are: at a keyword, or already in the messageQ

        # We search for the next space and the next newline.
        spc = raw.find(b' ', start)
        nl = raw.find(b'\n', start)

        # If space appears before newline, we have a keyword.  Otherwise,
        # it's the final message, which we just read to the end of the file.

        # Base case
        # =========
        # If newline appears first (or there's no space at all, in which
        # case find returns -1), we assume a blank line.  A blank line
        # means the remainder of the data is the message.  We store it in
        # the dictionary, with None as the key, and return.
        if (spc < 0) or (nl < spc):
            assert nl == start
            dct[None] = raw[start+1:]
            return dct

        # Recursive case
        # ==============
        # we read a key-value pair and recurse for the next.
        key = raw[start:spc]

        # Find the end of the value.  Continuation lines begin with a
        # space, so we loop until we find a "\n" not followed by a space.
        end = start
        while True:
            end = raw.find(b'\n', end+1)
            if raw[end+1] != ord(' '): break

        # Grab the value
        # Also, drop the leading space on continuation lines
        value = raw[spc+1:end].replace(b'\n ', b'\n')

        # Don't overwrite existing data contents
        if key in dct:
            if type(dct[key]) == list:
                dct[key].append(value)
            else:
                dct[key] = [ dct[key], value ]
        else:
            dct[key]=value

        return self.kvlm_parse(raw, start=end+1, dct=dct)

    def kvlm_serialize(self, kvlm):
        ret = b''

        # Output fields
        for k in kvlm.keys():
            # Skip the message itself
            if k == None: continue
            val = kvlm[k]
            # Normalize to a list
            if type(val) != list:
                val = [ val ]

            for v in val:
                ret += k + b' ' + (v.replace(b'\n', b'\n ')) + b'\n'

        # Append message
        ret += b'\n' + kvlm[None] + b'\n'

        return ret
        
class GitTreeLeaf (object):
    def __init__(self, mode, path, sha):
        self.mode = mode
        self.path = path
        self.sha = sha
              
class GitTree(GitObject):
    fmt=b'tree'

    def deserialize(self, data):
        self.items = self.tree_parse(data)

    def serialize(self):
        return self.tree_serialize()

    def init(self):
        self.items = list()
    
    def tree_parse(self, data):
        pos = 0
        max = len(data)
        ret = list()
        while pos < max:
            pos, data = self.tree_parse_one(data, pos)
            ret.append(data)
        return ret
    
    def tree_parse_one(self, raw, start=0):
        # Find the space terminator of the mode
        x = raw.find(b' ', start)
        assert x - start in [5, 6]

        # Read the mode
        mode = raw[start:x]
        if len(mode) == 5:
            # Normalize to six bytes.
            mode = b" " + mode

        # Find the NULL terminator of the path
        y = raw.find(b'\x00', x)
        # and read the path
        path = raw[x+1:y]

        # Read the SHA and convert to a hex string
        sha = format(int.from_bytes(raw[y+1:y+21], "big"), "040x")
        return y+21, GitTreeLeaf(mode, path.decode("utf8"), sha)
    

    def tree_serialize(self, obj):
        # Notice this isn't a comparison function, but a conversion function.
        # Python's default sort doesn't accept a custom comparison function,
        # like in most languages, but a `key` arguments that returns a new
        # value, which is compared using the default rules.  So we just return
        # the leaf name, with an extra / if it's a directory.
        def tree_leaf_sort_key(leaf):
            if leaf.mode.startswith(b"10"):
                return leaf.path
            else:
                return leaf.path + "/"
        obj.items.sort(key=tree_leaf_sort_key)
        ret = b''
        for i in obj.items:
            ret += i.mode
            ret += b' '
            ret += i.path.encode("utf8")
            ret += b'\x00'
            sha = int(i.sha, 16)
            ret += sha.to_bytes(20, byteorder="big")
        return ret
    
class GitTag(GitCommit):
    fmt = b'tag'