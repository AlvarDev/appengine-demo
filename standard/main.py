import webapp2
import os
import MySQLdb
import time
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template  # also added
from google.appengine.api import urlfetch

# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
CLOUDSQL_DB = os.environ.get('CLOUDSQL_DB')


def connect_to_cloudsql():
    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # Connect using the unix socket located at
        # /cloudsql/cloudsql-connection-name.
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD,
            db=CLOUDSQL_DB)

    # If the unix socket is unavailable, then try to connect using TCP. This
    # will work if you're running a local MySQL server or using the Cloud SQL
    # proxy, for example:
    #
    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
    #
    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD, db=CLOUDSQL_DB)

    return db

class SQLInsertPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        db = connect_to_cloudsql()
        cursor = db.cursor()

        try:
            # Execute the SQL command
            cursor.execute('INSERT INTO gifs (name, gif, bought) VALUES ("AlvarDev", "PS4", "not");')
            db.commit()
            self.response.write('Ok')

        except:
            # Rollback in case there is any error
            db.rollback()
            self.response.write('Something went wrong :(')

        # disconnect from server
        db.close()

class SQLSelectPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        db = connect_to_cloudsql()
        cursor = db.cursor()

        try:
            cursor.execute('select * from gifs;')
            for r in cursor.fetchall():
                self.response.write('{}\n'.format(r))

        except ValueError, e:
            print e;
            # Execute the SQL command
            # Rollback in case there is any error
            db.rollback()
            self.response.write('Something went wrong :(')

        # disconnect from server
        db.close()

#Datastore
class Gif(ndb.Model):
    idUser = ndb.StringProperty(indexed=True)
    name = ndb.StringProperty(indexed=False)
    gif = ndb.StringProperty(indexed=False)
    bought = ndb.BooleanProperty(indexed=False)

class DatastoreInserttPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        gif = Gif(idUser=str(time.time()).split('.')[0], name="AlvarDev", gif="PS4", bought=False)
        gif.put()
        self.response.write('Ok')

class DatastoreSelectPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        gif_query = Gif.query().order(-Gif.idUser)
        gifs = gif_query.fetch(10)
        print gifs
        for r in gifs:
            self.response.write('{}\n'.format(r))

#Web
class WelcomePage(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'views/index.html')
        self.response.out.write(template.render(path, {}))


app = webapp2.WSGIApplication([
    ('/', WelcomePage),
    ('/sqlinsert', SQLInsertPage),
    ('/sqlselect', SQLSelectPage),
    ('/dsinsert', DatastoreInserttPage),
    ('/dsselect', DatastoreSelectPage),
], debug=True)
