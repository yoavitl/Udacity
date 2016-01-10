from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import os
import datetime


from database_setup import Base, Shelters, Puppy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import asc, desc


engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/puppies"):
            Puppies = session.execute('select * from puppies order by name;').fetchall()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "<h1>1. Query all of the puppies and return the results in ascending alphabetical order</h1></br></br>"
            message += "<a href=/puppies/2>Next > </a></br>"
            for i in Puppies:
                message += i.name + "</br>"
                message +="</body></html>"
            self.wfile.write(message)
            return

        elif self.path.endswith("/puppies/2"):
            today = datetime.date.today() - datetime.timedelta(180)
            print today
            Puppies = session.execute('select * from puppies where DOB > "%s" order by DOB desc;' % today).fetchall()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "<h1>2. Query all of the puppies that are less than 6 months old organized by the youngest first</h1></br></br>"
            message += "<a href=/puppies>< back </a><a href=/puppies/3>Next > </a></br>"
            for i in Puppies:
                message += i.name + "-------" + i.DOB + "</br>"
                message +="</body></html>"
            self.wfile.write(message)
            return
        elif self.path.endswith("/puppies/3"):
            Puppies = session.execute('select * from puppies order by weight;').fetchall()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "<h1>3. Query all puppies by ascending weight</h1></br></br>"
            message += "<a href=/puppies/2>< back </a><a href=/puppies/4>Next > </a></br>"
            for i in Puppies:
                message += i.name + "-------" + str(round(i.weight,2)) + "</br>"
                message +="</body></html>"
            self.wfile.write(message)
            return
        elif self.path.endswith("/puppies/4"):
            Puppies = session.execute('select name,shelter_id from puppies;').fetchall()
            selter = session.execute('select Sname,id from shelters;').fetchall()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>"
            message += "<h1>4. Query all puppies grouped by the shelter in which they are staying</h1></br></br>"
            message += "<a href=/puppies/3>< back </a></br>"
            for s in selter:
                message += "<h2><u> %s </u></h2><br>" % s.Sname
                for i in Puppies:
                    if i.shelter_id == s.id:
                        message += "%s<br>" % i.name
            message +="</body></html>"
            self.wfile.write(message)
            return


        else:
            self.send_error(404, 'sd Not Found: %s' % self.path)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
