#!/bin/sh


# Here we will be spinning up multiple threads with multiple worker processess(-w) and perform a binding.

exec  gunicorn -w 4 -b 0.0.0.0:3020 manage:app & 
exec  python3 video_streams.py
