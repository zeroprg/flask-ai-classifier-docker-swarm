#!/bin/sh


# Here we will be spinning up multiple threads with multiple worker processess(-w) and perform a binding.

exec  python3 video_streams.py &
exec  gunicorn --env TMPDIR=./ -w 4 -b 0.0.0.0:3020 manage:app 

