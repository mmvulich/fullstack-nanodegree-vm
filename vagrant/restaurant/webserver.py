from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                
                output = ""
                output = "<html><body>Hello!</body></html>"
                self.wfile.write(output)
                print output
                return
        
        except IOError:
            self.send_error(404, "file Not Found %s" % self.path)

def main():
    try:
        port = 8080
        server = HTTPSErver(('',port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()
        
    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()
    
if __name__ == '__main__':
    main()