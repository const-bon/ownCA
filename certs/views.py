from django.shortcuts import render

from django.http import HttpResponse

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, FormView

from .models import Certificate, CACertificate

from .forms import CertificateForm


# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/thanks/')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()
#
#     return render(request, 'certs/test.html', {'form': form})

#
# def index(request):
#     return HttpResponse("You're at the certs index.")


class IndexView(generic.ListView):
    template_name = 'certs/index.html'
    context_object_name = 'certificate_list'

    def get_queryset(self):
        return Certificate.objects.order_by('-creation_date')


class DetailView(generic.DetailView):
    model = Certificate
    template_name = 'certs/detail.html'


class CertificateCreateView(FormView):
    template_name = 'certs/create.html'
    form_class = CertificateForm
    success_url = reverse_lazy('certs:index')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.create_certificate()
        return super(CertificateCreateView, self).form_valid(form)


class CertificateCreateCAView(FormView):
    template_name = 'certs/create.html'
    form_class = CertificateForm
    success_url = reverse_lazy('certs:index')

    def form_valid(self, form):

        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.create_ca_certificate(form.cleaned_data)
        return super(CertificateCreateCAView, self).form_valid(form)

# def detail(request, certificate_common__name):
#     certificate = get_object_or_404(Certificate, common_name=certificate_common__name)
#     return render(request, 'certs/detail.html', {
#             'certificate': certificate,
#         })
