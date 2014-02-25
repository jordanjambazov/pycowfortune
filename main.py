import subprocess
from StringIO import StringIO
from wsgiref.simple_server import make_server
 
def application(environ, start_response):
    path = environ.get('PATH_INFO')[1:]
    is_valid = path in ['off', 'some', 'other', 'options']
 
    stdout = StringIO()
    if is_valid:
        out, err = subprocess.Popen(['fortune {} | cowsay'.format(path)], stdout=subprocess.PIPE, shell=True).communicate()
        for line in out.splitlines():
            print >> stdout, line
    start_response("200 OK", [('Content-Type','text/plain')])
    return [stdout.getvalue()]
 
if __name__ == '__main__':
    httpd = make_server('', 8000, application)
    print "Starting cow server on port 8000"
    httpd.serve_forever()
