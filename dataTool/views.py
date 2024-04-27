from django.shortcuts import render
from django.views import View
from company.models import Company

# Create your views here.
class checkNewRecords(View):
    template_name = 'dataTool/check_new_records.html'

    def get(self,request,*args,**kwargs):
        companies = Company.objects.all()
        context={
            'all_companies': companies 
        }
        print(context)
        return render(request, self.template_name,context)
