from django.shortcuts import render

from django.http import HttpResponse

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView

from .models import Certificate


def index(request):
    return HttpResponse("You're at the certs index.")


class IndexView(generic.ListView):
    template_name = 'certs/index.html'
    context_object_name = 'certificate_list'

    def get_queryset(self):
        return Certificate.objects.order_by('-creation_date')


class CertificateCreate(CreateView):
    model = Certificate
    fields = ['common_name', 'certificate', 'signing_request', 'key', 'creation_date']
    template_name = 'certs/create.html'
    success_url = reverse_lazy('certs:index')


class DetailView(generic.DetailView):
    model = Certificate
    template_name = 'certs/detail.html'


# def detail(request, certificate_common__name):
#     certificate = get_object_or_404(Certificate, common_name=certificate_common__name)
#     return render(request, 'certs/detail.html', {
#             'certificate': certificate,
#         })
