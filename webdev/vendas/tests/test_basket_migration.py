import pytest
from django.urls import reverse
from django.db import connection
from django.contrib.auth.models import User
from django.db.migrations.executor import MigrationExecutor
from pytest_django.asserts import assertContains, assertRedirects


def test_migrate_vendas_to_basket_based_sales(transactional_db):
    executor = MigrationExecutor(connection)
    app = "vendas"
    migrate_from = [(app, "0007_create_basket_for_existing_sales")]
    migrate_to = [(app, "0008_remove_venda_produtos_and_more")]

    executor.migrate(migrate_from)
    old_apps = executor.loader.project_state(migrate_from).apps

    # Create some old data.
    Venda = old_apps.get_model(app, "Venda")
    old_sale = Venda.objects.create(data='2022-07-08',
                                    parcelas=6,
                                    valor=1200)
    Produto = old_apps.get_model('produtos', 'Produto')
    products = [
        Produto.objects.create(nome='Produto 1', colecao="d'Mentira"),
        Produto.objects.create(nome='Produto 2', colecao="d'Mentira"),
    ]
    old_sale.produtos.add(*[p for p in products])

    # Migrate forwards.
    executor.loader.build_graph()  # reload.
    executor.migrate(migrate_to)
    new_apps = executor.loader.project_state(migrate_to).apps

    # Test the new data.
    Venda = new_apps.get_model(app, "Venda")
    Basket = new_apps.get_model(app, "Basket")
    BasketItem = new_apps.get_model(app, "BasketItem")
    assert Basket.objects.exists()
    assert Venda.objects.first().basket == Basket.objects.first()
    for product in products:
        assert BasketItem.objects.get(product=product)

