from time import time


# Print name and time for function processing
def timer(func):
    def inner(*args, **kwargs):
        s_time = time()
        ret = func(*args, **kwargs)
        print("{} took {:.2f} sec of my life".format(func.__name__, time()-s_time))
        return ret
    return inner