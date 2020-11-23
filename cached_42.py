
import json
import hashlib
from pathlib import Path
import copy
import inspect

STORAGE = "out/cached/"

class Cached42:

    def __init__(self, params, name=None, ignore_args=[]):
        
        self.caching_params = copy.copy(params)
        self.name = name
        self.storage = Path(STORAGE)

        for arg in ignore_args:
            self.caching_params.pop(arg)

        self._hash = self._get_hash()

    def get_path(self):

        # Create storage dir if doesn't exist
        self.storage.mkdir(exist_ok=True, parents=True)

        filename = f"{self._hash}.cached"

        if self.name is not None:
            task_dir = self.storage / f"{self.name}"
            task_dir.mkdir(exist_ok=True, parents=True)

            path = task_dir / filename
        else:
            path = self.storage / filename

        return path
        
    def exists(self):
        if self.get_path().exists():
            return True
        else:
            return False

    def _get_hash(self):

        cfg_str = json.dumps(self.caching_params, separators=(',', ':'), sort_keys=True, cls=CachedObjectEncoder)
        cfg_hash = hashlib.md5(cfg_str.encode('utf-8')).hexdigest()

        return cfg_hash

class CachedObjectEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Cached42):
            # Replace the Cached42 by their hash for making new hash of all params and args
            return o._hash
        return super(CachedObjectEncoder, self).default(o)

def cache_42(ignore_args=[]):

    def cache_42_built_decorator(func):
        
        def wrapping(*args, **kwargs):
            # Create caching_params from args of the wrapped(task) function
            args_names = inspect.getfullargspec(func)[0]
            args_names.remove('cache')

            caching_params = {}
            for i in range(len(args)):
                key = args_names[i]
                value = args[i]
                caching_params[key] = value
            caching_params.update(kwargs)
            
            cached_res = Cached42(caching_params, name=func.__name__, ignore_args=ignore_args)

            if cached_res.exists():
                print(f"{func.__name__} was cached, skipping...")
                return cached_res
            else:
                return func(*args, **kwargs, cache=cached_res)
        
        return wrapping

    return cache_42_built_decorator

    