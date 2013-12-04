import time
import BaseHTTPServer
import urlparse
from TwitterSearch import *

def twit_search(keywords):
    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.setKeywords(keywords) # let's define all words we would like to have a look for
        tso.setLanguage('en') # we want to see English tweets only
        tso.setCount(7) # please dear Mr Twitter, only give us 7 results per page
        tso.setIncludeEntities(False) # and don't give us all those entity information

        # it's about time to create a TwitterSearch object with our secret tokens
        ts = TwitterSearch(
            consumer_key = 'asX13sgNL5fVbVfSwyaLCw',
            consumer_secret = 'Y0SkBfcxZ5Q4AVmmXEMCcWI5lfUD3JBdgtd1fioJwU',
            access_token = '956472907-NGjoV82C6UwGu4xXLod1R3SKsWG9hfCXntt8Smxr',
            access_token_secret = '98S3jvUx5TZQxHYfBcP971ow02mTzeyQUdILamHp3Oee1'
         )

        for tweet in ts.searchTweetsIterable(tso): # this is where the fun actually starts :)
            return '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] )

    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)


HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000 # Maybe set this to 9000.

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  # def do_HEAD(s):
  #   s.send_response(200)
  #   s.send_header("Content-type", "text/html")
  #   s.end_headers()
  def do_GET(s):
      """Respond to a GET request."""
      s.send_response(200)
      s.send_header("Content-type", "text/html")
      s.end_headers()
      s.wfile.write("<html><head><title>Title goes here.</title></head>")
      s.wfile.write("<body><p>This is a test.</p>")
      # If someone went to "http://something.somewhere.net/foo/bar/",
      # then s.path equals "/foo/bar/".
      keywords = urlparse.parse_qs(urlparse.urlparse(s.path).query)['keywords']
      s.wfile.write("<p>You accessed keywords: %s</p>" % twit_search(keywords))
      s.wfile.write("</body></html>")

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)