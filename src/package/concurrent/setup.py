import numpy as np
from joblib import Parallel, delayed
from collections.abc import Iterable


def parallel(data, callback, *args, core=12):
    
    if isinstance(data, list):
        result = Parallel(n_jobs=core)(
            delayed(callback)(i, *args) for i in np.array(data)
        )
    elif isinstance(data, Iterable):
        result = Parallel(n_jobs=core)(delayed(callback)(i, *args) for i in data)
    else:
        raise TypeError("data must be list or Iterable")
    # result = np.array(result)
    # result = result[result != None]
    return result


if __name__ == "__main__":
    from time import time
    import math

    t1 = time()
    result1 = []

    def call(x):
        h = 0
        for v in range(100):
            h += math.sqrt(v) + x
        return h

    result1 = parallel(call, range(10000000))

    # for i in range(10000000):
    #     result.append(call(i))
    print(len(result1))
    t2 = time() - t1
    print(t2)
