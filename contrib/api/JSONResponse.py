from django.http import HttpResponse
from django.utils import simplejson as json

class JSONResponse(HttpResponse):
	def __init__(self, content, mimetype = "application/json",*args,**kwargs):
		#content = json.dumps(content)
		super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)
