# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from biodiversity.utils import _get_elementos 
from models import *

@login_required
def privados(request):
    documentos = _get_elementos(request, 
                                 Documentos.objects.all().order_by('-fecha'))
    categorias = Categoria.objects.all()
    return render_to_response('documentos/privados.html', 
                              {'documentos': documentos,'categorias':categorias},
                              context_instance=RequestContext(request))
def documento(request, documento_id):
    documento = get_object_or_404(Documentos, pk=documento_id)
    if request.user.is_authenticated() and not documento.publico:
        return render_to_response('documentos/documento.html',
                                  {'documento': documento},
                                  context_instance=RequestContext(request))
    else:
        request.flash['message'] = 'Este documento no es público, favor inice sesión'
        #return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))
        return HttpResponseRedirect('/accounts/login?next=/documentos/documento/%s' % documento.id)

def categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    categorias = Categoria.objects.all()
    if request.user.is_authenticated():
        documentos = _get_elementos(request, 
                                     Documentos.objects.filter(categoria=categoria))
    else:
        documentos = _get_elementos(request, 
                                     Documentos.objects.filter(categoria=categoria, publico=True))
    return render_to_response('documentos/categoria.html', 
                              {'documentos': documentos, 'categorias':categorias, 'categoria':categoria},
                              context_instance=RequestContext(request))

def publicos(request):
    request.session['flag'] = 'biblioteca'
    documentos = _get_elementos(request, 
                                 Documentos.objects.filter(publico=True).order_by('-fecha'))
    categorias = Categoria.objects.all()
    return render_to_response('documentos/publicos.html', 
                              locals(),
                              context_instance=RequestContext(request))
