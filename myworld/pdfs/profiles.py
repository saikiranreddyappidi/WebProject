from django.http import HttpResponse, JsonResponse
from django.template import loader

from . Data.Primary import user as user

def profile(request):
	context={"profileData":user.profile(self=request)}
	template=loader.get_template("allProfiles.html")
	return HttpResponse(template.render(context,request))

def testing(request):
	context={'userid':'Sai Kiran','id':'211FA04563','title':'Testing','body':'This is a testing page'}
	return JsonResponse(context)