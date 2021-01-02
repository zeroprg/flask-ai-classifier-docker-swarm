import time
import urllib.request
import urllib.error
from multiprocessing import Process

def sleep(timeout, retry=1):
 
    def the_real_decorator(function):
        def wrapper(*args, **kwargs):
            retries = 0
            print('--------------------------------Sleeping for {} seconds ----------------------------------------'.format(timeout))
            while retries < retry:
                try:
                    value = function(*args, **kwargs)
                    if value is None:
                        return
                except Exception as e:
                    print('Exception: {}, lets sleeping for {} seconds to retry'.format(e,timeout))                    
                    retries += 1

        
        return wrapper
    return the_real_decorator