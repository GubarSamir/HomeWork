import time

def cache(max_limit=64):
    def internal(f):
       def deco(*args):
           max_lim = max_limit
           if args in deco._cache:
               return deco._cache[args]
           result = f(*args)
           deco._cache[args] = result
           if len(deco._cache) >= max_lim:
               deco._cache.popitem()

           return result

       deco._cache = {}
       return deco

    return internal

start_time = time.time()

@cache(max_limit=64)
def fibo(n):
    if n < 2:
        return n
    else:
        return fibo(n - 1) + fibo(n - 2)

for i in range(30):
    print(fibo(i))

print(time.time() - start_time, "seconds")
