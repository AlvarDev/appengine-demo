import endpoints
import time
from protorpc   import remote
from protorpc import message_types
from protorpc import messages
from google.appengine.ext import ndb

# [START messages]
class GifResponse(messages.Message):
    idUser = messages.StringField(1)
    name = messages.StringField(2)
    gif = messages.StringField(3)
    bought = messages.BooleanField(4)

class ApiRequest(messages.Message):
    idUser = messages.StringField(1)
    name = messages.StringField(2)
    gif = messages.StringField(3)
    bought = messages.BooleanField(4)

class ApiResponse(messages.Message):
    success = messages.BooleanField(1)
    message = messages.StringField(2)

class ApiListResponse(messages.Message):
    success = messages.BooleanField(1)
    gifs = messages.MessageField(GifResponse, 2, repeated=True)

class Gif(ndb.Model):
    idUser = ndb.StringProperty(indexed=True)
    name = ndb.StringProperty(indexed=False)
    gif = ndb.StringProperty(indexed=False)
    bought = ndb.BooleanProperty(indexed=False)

@endpoints.api(name='demo', version='v1')
class DemoApi(remote.Service):

    @endpoints.method(ApiRequest,ApiResponse,path='insert',http_method='POST',name='demo')
    def insert(self, request):
        gif = Gif(idUser=str(time.time()).split('.')[0],name=request.name, gif=request.gif, bought=request.bought)
        gif.put()
        return ApiResponse(success=True, message="Gif saved")

    @endpoints.method(ApiRequest,ApiListResponse,path='select',http_method='GET',name='select')
    def select(self, request):
        gif_query = Gif.query().order(-Gif.idUser)
        gifs = gif_query.fetch(10)
        rGifs = list()
        for r in gifs:
            rGifs.append(GifResponse(idUser=r.idUser, name= r.name, gif=r.gif, bought=r.bought))
        return ApiListResponse(success=True, gifs=rGifs)

    @endpoints.method(ApiRequest,ApiResponse,path='update',http_method='POST',name='update')
    def update(self, request):
        gif_query = Gif.query(Gif.idUser >= request.idUser).order(-Gif.idUser)
        gifs = gif_query.fetch(1)
        gifs[0].bought=True
        gifs[0].put()
        return ApiResponse(success=True, message="Gif updated")


# Server
api = endpoints.api_server([DemoApi])
