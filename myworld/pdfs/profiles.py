from django.http import HttpResponse
from django.template import loader

from . Data.Primary import user as user

def profile(request):
	context={"profileData":user.profile(self=request)}
	template=loader.get_template("allProfiles.html")
	return HttpResponse(template.render(context,request))