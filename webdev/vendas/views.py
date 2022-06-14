from django.http.response import Http404, HttpResponseRedirect
from django.urls.base import reverse
from webdev.vendas.forms import ClienteForm, SortSalesForm, VendaForm, SortClientsForm
from webdev.vendas.models import Cliente, Venda
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import Q

# Clientes
@login_required
def clientes(request):
    if request.GET:
        # Filters
        if 'search' in request.GET:
            clients = Cliente.objects.filter(
                Q(nome__icontains=request.GET.get('search')) |
                Q(sobrenome__icontains=request.GET.get('search')) |
                Q(email__icontains=request.GET.get('search')) |
                Q(telefone__icontains=request.GET.get('search')) |
                Q(endereco__icontains=request.GET.get('search')) |
                Q(cpf__icontains=request.GET.get('search')) |
                Q(birth_date__icontains=request.GET.get('search')) |
                Q(observacao__icontains=request.GET.get('search'))
            )
        else:
            clients = Cliente.objects.all()
        # Sort
        if 'sort-order' in request.GET:
            sort_form = SortClientsForm(request.GET, prefix='sort')
            if sort_form.is_valid():
                field = sort_form.data.get(sort_form.prefix + '-field')
                order = sort_form.data.get(sort_form.prefix + '-order')
                clients = clients.order_by(order + field)
        else:
            sort_form = SortClientsForm(prefix='sort')

    else:
        sort_form = SortClientsForm(prefix='sort')
        clients = Cliente.objects.all()

    context = {
        # TODO: create import/export views for clients
        # 'import_url': reverse('vendas:importar_produtos'),
        # 'export_url': reverse('vendas:exportar_produtos'),
        'create_url': reverse('vendas:novo_cliente'),
        # 'actions_url': reverse('vendas:product_actions'),
        'title': 'Meus clientes',
        'clientes': clients,
        'sort_form': sort_form,
        'sorting': True if 'sort-order' in request.GET else False
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
    if request.GET:
        # Filters
        if 'search' in request.GET:
            vendas = Venda.objects.filter(
                Q(data=request.GET.get('search')) |
                # Q(cliente__icontains=request.GET.get('search')) |
                # Q(produtos__icontains=request.GET.get('search')) |
                Q(observacao__icontains=request.GET.get('search')) |
                Q(valor__icontains=request.GET.get('search')) |
                Q(parcelas__icontains=request.GET.get('search'))
            )
        else:
            vendas = Venda.objects.all()
        # Sort
        if 'sort-order' in request.GET:
            sort_form = SortSalesForm(request.GET, prefix='sort')
            if sort_form.is_valid():
                field = sort_form.data.get(sort_form.prefix + '-field')
                order = sort_form.data.get(sort_form.prefix + '-order')
                vendas = vendas.order_by(order + field)
        else:
            sort_form = SortSalesForm(prefix='sort')

    else:
        sort_form = SortSalesForm(prefix='sort')
        vendas = Venda.objects.all()

    context = {
        # TODO: create import/export views for sales
        # 'import_url': reverse('vendas:importar_produtos'),
        # 'export_url': reverse('vendas:exportar_produtos'),
        'create_url': reverse('vendas:nova_venda'),
        # 'actions_url': reverse('vendas:product_actions'),
        'title': 'Vendas Cadastradas',
        'vendas': vendas,
        'sort_form': sort_form,
        'sorting': True if 'sort-order' in request.GET else False
    }
    return render(request, 'vendas/minhas_vendas.html', context)

@login_required
def nova_venda(request):
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            form.save()
            next_url = request.POST.get('next')
            if 'submit-stay' in request.POST:
                return redirect('vendas:nova_venda')
            elif next_url:
                return redirect(f'{next_url}')
            else:
                return redirect('vendas:minhas_vendas')
    else:
        form = VendaForm()

    context = {
        'title': 'Nova Venda',
        'form': form,
        'novo_obj': True
    }

    return render(request, 'vendas/form_venda.html', context)

@login_required
def editar_venda(request, venda_id):
    try:
        venda = Venda.objects.get(id=venda_id)
    except:
        raise Http404('Venda não encontrada')

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

    return render(request, 'vendas/form_venda.html', context)

@login_required
def deletar_venda(request, venda_id):
    if request.method == 'POST':
        Venda.objects.get(id=venda_id).delete()
    return HttpResponseRedirect(reverse('vendas:minhas_vendas'))
