
import numpy as np

from cached_42 import Cached42, cache_42
import tools.pudb_hook

@cache_42()
def task_A(cfg, cache):

    print("task_A is running")
    cache_path = cache.get_path()
    cache_path.mkdir(exist_ok=True, parents=True)
    cache_path.touch()
    
    return cache

def task_B(cfg, resA):
    pass
    
    res_B = Cached42({"cfg": cfg, "resA": resA})
    if res_B.exists():
        return res_B

    print("task_B is running")
    print("res_a", resA.get_path())
    return res_B

@cache_42(ignore_args=[])
def task_C(cfg, resB, cache):
    
    print("task_C is running")
    
    print("resB path", resB.get_path())
    cache_path = cache.get_path()
    
    return cache

cfg = {
    "task_A": {"bla": 42},
    "task_B": {},
    "task_C": {"yo": 42},
}

resA = task_A(cfg["task_A"])
resB = task_B(cfg["task_B"], resA)
resC = task_C(cfg["task_C"], resB)

