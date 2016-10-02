from django.shortcuts import render

from django.http import HttpResponse

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, FormView

from .models import Certificate, CACertificate

from .forms import CertificateForm, CACertificateForm


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
        cert = Certificate.objects.filter(pk=kwargs['object'].id).get()
        context['certificate'] = cert.__dict__
        return context


class CADetailView(generic.DetailView):
    model = CACertificate
    template_name = 'certs/detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CADetailView, self).get_context_data(**kwargs)
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


class CreateCACertificateView(FormView):
    template_name = 'certs/create.html'
    form_class = CACertificateForm
    success_url = reverse_lazy('certs:ca_index')

    def form_valid(self, form):

        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.create_certificate(form.cleaned_data)
        return super(CreateCACertificateView, self).form_valid(form)


class GetCRLView(generic.DetailView):
    model = CACertificate
    template_name = 'certs/crl.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GetCRLView, self).get_context_data(**kwargs)
        # Search revoked certificates with CA certificate 'ca_cert' in table Certificate
        crl = Certificate.get_crl(kwargs['object'])
        context['crl'] = crl
        return context


def revoke(request, pk):
    cert = get_object_or_404(Certificate, pk=pk)
    Certificate.revoke(cert)
    return redirect(reverse_lazy('certs:index'))
