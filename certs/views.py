import zipfile

from django.shortcuts import get_object_or_404, render, redirect
from django.http import StreamingHttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, FormView
from wsgiref.util import FileWrapper

from .models import Certificate, CACertificate
from .forms import CertificateForm, CACertificateForm

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

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


def get_crl(request, pk):
    ca_cert = get_object_or_404(CACertificate, pk=pk)
    crl = Certificate.get_crl(ca_cert)
    temp = StringIO()
    with zipfile.ZipFile(temp, 'w') as archive:
            archive.writestr('crl.pem', str(crl))

    response = StreamingHttpResponse(FileWrapper(temp), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="crl.zip"'
    response['Content-Length'] = temp.tell()

    temp.seek(0)

    return response


def get_certificates(request, pk):
    cert_list = Certificate.objects.filter(ca_cert=pk, revoked=False)
    temp = StringIO()
    with zipfile.ZipFile(temp, 'w') as archive:
        for cert in cert_list:
            name = cert.commonName
            if name == '':
                name = cert.id
            archive.writestr('{}.crt'.format(name), str(cert.cert))
            archive.writestr('{}.key'.format(name), str(cert.key))

    response = StreamingHttpResponse(FileWrapper(temp), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="certificates.zip"'
    response['Content-Length'] = temp.tell()

    temp.seek(0)

    return response


def revoke(request, pk):
    cert = get_object_or_404(Certificate, pk=pk)
    Certificate.revoke(cert)
    return redirect(reverse_lazy('certs:index'))
