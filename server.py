import tornado.ioloop
import tornado.web
import stateplane as sp

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        easting = self.get_argument('easting', None)
        northing = self.get_argument('northing', None)
        epsg = self.get_argument('epsg', None)
        fips = self.get_argument('fips', None)
        abbr = self.get_argument('abbr', None)

        if easting is None or northing is None:
            self.write('*You must given easting or northing.')
            return
        easting = float(easting) * (1200 / 3937)
        northing = float(northing) * (1200 / 3937)
        if epsg is not None:
            print('easting={}, northing={}, epsg={}'.format(easting, northing, epsg))
            self.write('{},{}'.format(*sp.to_latlon(easting, northing, epsg=epsg)))
        elif fips is not None:
            print('easting={}, northing={}, fips={}'.format(easting, northing, fips))
            self.write('{},{}'.format(*sp.to_latlon(easting, northing, fips=fips)))
        elif abbr is not None:
            print('easting={}, northing={}, abbr={}'.format(easting, northing, abbr))
            self.write('{},{}'.format(*sp.to_latlon(easting, northing, abbr=abbr)))
        else:
            self.write('*As least one of epsg, fips and abbr must be provided.')

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(3333)
    tornado.ioloop.IOLoop.current().start()