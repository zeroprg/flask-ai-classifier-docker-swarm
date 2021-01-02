import time
import urllib.request
import urllib.error
from multiprocessing import Process

def sleep(timeout, retry=1):
 
    def the_real_decorator(function):
        def wrapper(*args, **kwargs):
            retries = 0
            print(f'--------------------------------Sleeping for {timeout} seconds ----------------------------------------')
            while retries < retry:
                try:
                    value = function(*args, **kwargs)
                    if value is None:
                        return
                except Exception as e:
                    print(f'Exception: {e}, lets sleeping for {timeout} seconds to retry')                    
                    retries += 1

        
        return wrapper
    return the_real_decorator