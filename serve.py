#       outcome/
# Serve AIML requests in the form:
#   POST:
#       { "msg": "hi there!" }
# to a HTTP client
#
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import io
import json
import sys

import aiml

#       understand/
# The Kernel object is the public interface to
# the AIML interpreter.
k = aiml.Kernel()

#       outcome/
# Use the 'learn' method to load the contents
# of an AIML file into the Kernel.
k.learn("std-startup.xml")

#       outcome/
# Use the 'respond' method to compute the response
# to a user's input string.  respond() returns
# the interpreter's response, which in this case
# we ignore.
k.respond("load aiml b")

#       understand/
# Use a python class to handle HTTP POST requests
# with responses from the AIML kernel
class S(BaseHTTPRequestHandler):

    #       outcome/
    # Read the data sent as JSON and respond to
    # the user message
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data_s = self.rfile.read(content_length)
        try:
            data = json.loads(data_s)
            msg = data["msg"]
            if msg:
                resp = k.respond(msg)
                self.wfile.write(resp)
            else:
                self.send_response(404)
        except:
            print sys.exc_info()
            self.send_response(400)


#       outcome/
# Start the HTTP server and handle keyboard interrupt
# as a shutdown
def run(server_class=HTTPServer, handler_class=S, port=8765):
    try:
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print 'Starting httpd...(localhost:%s)' % port
        httpd.serve_forever()
    except KeyboardInterrupt:
        print 'Shutting down...'
        httpd.socket.close()


if __name__ == "__main__":
    run()
