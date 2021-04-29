from django.test import TestCase
from django.core.files import File
from webdev.produtos.models import Categoria, Produto

class ProdutoTest(TestCase):
    def setUp(self):
        self.nome = 'Produto Legal'
        self.colecao = "d'Mentira"
        self.data_criacao = '2021-04-26'
        self.quantidade = 5
        self.tamanho = 22

        self.test_produto = Produto.objects.create(
            nome=self.nome,
            colecao=self.colecao,
            data_criacao=self.data_criacao,
            quantidade=self.quantidade,
            tamanho=self.tamanho
        )
        self.test_produto.save()
    
    def test_criar_produto(self):
        assert isinstance(self.test_produto, Produto)

    def test_foto_padrao_produto(self):
        assert self.test_produto.foto.name == 'produtos/default.jpg'

