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
        return Certificate.objects.order_by('-notBeforeDate')


class CAIndexView(generic.ListView):
    template_name = 'certs/ca_index.html'
    context_object_name = 'certificate_list'

    def get_queryset(self):
        return CACertificate.objects.order_by('-notBeforeDate')


class DetailView(generic.DetailView):
    model = Certificate
    template_name = 'certs/detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        cert_obj = Certificate.objects.filter(pk=kwargs['object'].id).get()
        context['certificate'] = cert_obj.__dict__
        return context

class CADetailView(generic.DetailView):
    model = CACertificate
    template_name = 'certs/detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CADetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        cert_obj = CACertificate.objects.filter(pk=kwargs['object'].id).get()
        context['certificate'] = cert_obj.__dict__
        return context


class CreateCertificateView(FormView):
    template_name = 'certs/create.html'
    form_class = CertificateForm
    success_url = reverse_lazy('certs:index')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.create_certificate(form.cleaned_data)
        return super(CreateCertificateView, self).form_valid(form)


class CreateCertificateCAView(FormView):
    template_name = 'certs/create.html'
    form_class = CertificateForm
    success_url = reverse_lazy('certs:ca_index')

    def form_valid(self, form):

        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.create_ca_certificate(form.cleaned_data)
        return super(CreateCertificateCAView, self).form_valid(form)
