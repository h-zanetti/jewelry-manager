from webdev.financeiro.models import Receita
from dateutil.relativedelta import relativedelta
from django.http.response import Http404, HttpResponseRedirect
from django.urls.base import reverse
from django.utils import timezone
from webdev.vendas.forms import ClienteForm, VendaForm
from webdev.vendas.models import Cliente, Venda
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

# Clientes
@login_required
def clientes(request):
    context = {
        'title': 'Meus clientes',
        'clientes': Cliente.objects.all()
    }
    return render(request, 'vendas/clientes.html', context)

@login_required
def novo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            next_url = request.POST.get('next')
            if 'submit-stay' in request.POST:
                return redirect('vendas:novo_cliente')
            elif next_url:
                return redirect(f'{next_url}')
            else:
                return redirect('vendas:clientes')
    else:
        form = ClienteForm()

    context = {
        'title': 'Novo cliente',
        'form': form
    }

    return render(request, 'vendas/novo_cliente.html', context)

@login_required
def editar_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.get(id=cliente_id)
    except:
        raise Http404('Cliente não encontrado')

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('vendas:clientes')
    else:
        form = ClienteForm(instance=cliente)

    context = {
        'title': 'Editar cliente',
        'form': form
    }

    return render(request, 'vendas/novo_cliente.html', context)

@login_required
def deletar_cliente(request, cliente_id):
    if request.method == 'POST':
        Cliente.objects.get(id=cliente_id).delete()
    return HttpResponseRedirect(reverse('vendas:clientes'))

# Vendas
@login_required
def minhas_vendas(request):
    context = {
        'title': 'Vendas Cadastradas',
        'vendas': Venda.objects.all()
    }
    return render(request, 'vendas/minhas_vendas.html', context)

@login_required
def nova_venda(request):
    if request.method == 'POST':
        form = VendaForm(request.POST, initial={'data': timezone.now})
        if form.is_valid():
            venda = form.save()
            for i in range(venda.parcelas):
                Receita.objects.create(
                    data=venda.data + relativedelta(months=i),
                    categoria='Venda',
                    valor=venda.get_valor_parcela()
                )
            next_url = request.POST.get('next')
            if 'submit-stay' in request.POST:
                return redirect('vendas:nova_venda')
            elif next_url:
                return redirect(f'{next_url}')
            else:
                return redirect('vendas:minhas_vendas')
    else:
        form = VendaForm(initial={'data': timezone.now})

    context = {
        'title': 'Nova Venda',
        'form': form
    }

    return render(request, 'vendas/nova_venda.html', context)

@login_required
def editar_venda(request, venda_id):
    try:
        venda = Venda.objects.get(id=venda_id)
    except:
        raise Http404('Cliente não encontrado')

    if request.method == 'POST':
        form = VendaForm(request.POST, instance=venda)
        if form.is_valid():
            form.save()
            return redirect('vendas:minhas_vendas')
    else:
        form = VendaForm(instance=venda)

    context = {
        'title': 'Editar venda',
        'form': form
    }

    return render(request, 'vendas/nova_venda.html', context)

@login_required
def deletar_venda(request, venda_id):
    if request.method == 'POST':
        Venda.objects.get(id=venda_id).delete()
    return HttpResponseRedirect(reverse('vendas:minhas_vendas'))
