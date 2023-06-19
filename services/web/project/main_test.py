
import logging
import json

import requests

from requests.exceptions import HTTPError



from flask import Response,request



logging.basicConfig(level=logging.INFO)


def getQuote(format, key, lang):
    logging.info('Hitting the "/getQuote" route')
    data = {}
    data['format'] = format
    data['key'] = key
    data['lang'] = lang
   
    try:
            response = requests.post(url='http://api.forismatic.com/api/1.0/',
                                data=data, headers={})  
            #print("response is:"+ str(response) )                          
            response.raise_for_status()
            # access JSOn content
            jsonResponse = response.json()
            #print(jsonResponse)
            logging.debug("Entire JSON response")
            logging.debug(jsonResponse)

    except HTTPError as http_err:
        print('HTTP error occurred when connected to {0}: {1}'.format('/getQuote', http_err))
    except Exception as err:
        print('Connection to {} failed: {}'.format('/getQuote',err))
   
   
    return response


if __name__ == "__main__":
    print(getQuote("json", "123", "en"))