PyCowFortune
------------
The purpose of this small project is to explain what does shell injection mean by example.

Initially, this post was published at Empybit company blog.

[What is shell injection and how to avoid it?][1]


Shell Injections
----------------

It is a well known fact that developers should be paranoid about security. In this post I am going to briefly describe what is Shell Injection and general principles to avoid it.

Generally, shell injection can be considered as a software bug in input data processing that allows the user to inject code and execute commands on the server machine.

Let’s consider the following example:

    import subprocess
    from StringIO import StringIO
    from wsgiref.simple_server import make_server
     
    def application(environ, start_response):
        path = environ.get('PATH_INFO')[1:]
     
        stdout = StringIO()
        out, err = subprocess.Popen(['fortune {} | cowsay'.format(path)], stdout=subprocess.PIPE, shell=True).communicate()
        for line in out.splitlines():
            print >> stdout, line
        start_response("200 OK", [('Content-Type','text/plain')])
        return [stdout.getvalue()]
     
    if __name__ == '__main__':
        httpd = make_server('', 8000, application)
        print "Starting cow server on port 8000"
        httpd.serve_forever()

It’s a very simple web application that relies on the fortune and cowsay tools to generate wise quotes and display them to the user in a funny way.

     ______________________________________
    / Do you mean that you not only want a \
    | wrong answer, but a certain wrong    |
    | answer?                              |
    |                                      |
    \ -- Tobaben                           /
     --------------------------------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||

The application accepts user input, so that we could show different types of quotations. Let’s consider that the user requests offensive quotations and navigates to the following URL: http://localhost:8000/off. The /off parameter would be passed to the command we are executing and the output would be something like this:

     ________________________________________
    / You have been bi*chy since Tuesday and \
    \ you'll probably get fired today.       /
     ----------------------------------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||

But what’s the problem with the code above? We accept user input which is used to format the command without applying any filtration or normalization on it. The cracker can execute any command on the server and see it’s output: http://localhost:8000/ cat cowfortune.py #.

    Everything should be made as simple as possible, but not simpler.
    		-- Albert Einstein
     ________________________________________
    / import subprocess from StringIO import \
    | StringIO from wsgiref.simple_server    |
    | import make_server                     |
    |                                        |
    | def application(environ,               |
    | start_response):                       |
    |                                        |
    | path = environ.get('PATH_INFO')[1:]    |
    |                                        |
    | stdout = StringIO()                    |
    |                                        |
    | out, err = subprocess.Popen(['fortune  |
    | {} | cowsay'.format(path)],            |
    | stdout=subprocess.PIPE,                |
    | shell=True).communicate()              |
    |                                        |
    | for line in out.splitlines():          |
    |                                        |
    | print >> stdout, line                  |
    |                                        |
    | start_response("200 OK",               |
    | [('Content-Type','text/plain')])       |
    |                                        |
    | return [stdout.getvalue()]             |
    |                                        |
    | if __name__ == '__main__':             |
    |                                        |
    | httpd = make_server('', 8000,          |
    | application)                           |
    |                                        |
    | print "Starting cow server on port     |
    | 8000"                                  |
    |                                        |
    \ httpd.serve_forever()                  /
     ----------------------------------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||

As you see, the “cow” answers absolutely everything we ask about, so the solution is to filter the questions.

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

What are the golden rules to avoid injection vulnerabilities?

* Always verify user input.
* Never use direct user input to format commands, SQL code or anything that executes.
* Make sure you think about security on the go and don’t leave it for further refactoring.
* Be paranoid.


  [1]: http://empybit.com/what-is-shell-injection-and-how-to-avoid-it/
