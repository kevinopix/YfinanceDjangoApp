from django.shortcuts import render
from django.views import View
from .models import Company

# Create your views here.
class CompanyAllView(View):
    template_name = 'home/index.html'
    def get(self,request,*args,**kwargs):
        companies = Company.objects.all()
        context={
            'all_companies': companies 
        }
        print(context)
        return render(request, self.template_name,context)



class SingleCompanyView(View):
    model = Company
    template_name = 'companies/single_company.html'

    def get(self,request,*args,**kwargs):
        company = get_object_or_404(self.model, id=kwargs['id'])
        print(str(post_obj))
        context={
            'company': company 
        }
        print(context)
        return render(request, self.template_name,context)

