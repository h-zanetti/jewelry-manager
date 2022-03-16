import os
import sys
import json
import datetime as dt
from webdev.settings.base import BASE_DIR
from webdev.fornecedores.models import Servico

stats = {'st_time': dt.datetime.now()}

# fornededores.Servico -> produtos.ServicoDoProduto
def gen_servico_dp_fixture(pk, servico_id, produto_id):
    servico = Servico.objects.get(pk=servico_id)
    servico_dp = {
        'model': 'produtos.servicodoproduto',
        'pk': pk,
        'fields': {
            'produto': produto_id,
            'nome': servico.nome,
            'valor': float(servico.valor)
        }
    }
    return servico_dp


# Load fixtures
produtos_path = os.path.join(BASE_DIR, 'produtos', 'fixtures', 'produtos_fixtures.json')
with open(produtos_path) as jfile:
    produtos = json.load(jfile)
    jfile.close()


fixtures = []
stats['servicos_dp_criados'] = 0
for produto in produtos:
    for servico_id in produto['fields']['servicos']:
        pk = stats['servicos_dp_criados'] + 1
        servico = gen_servico_dp_fixture(pk, servico_id, produto['pk'])
        fixtures.append(servico)

# Dump fixtures
dump_path = os.path.join(BASE_DIR, 'produtos', 'fixtures', f'servico_dp_fixture{stats["st_time"].date()}.json')
fixtures_file = open(dump_path, 'w')
json.dump(fixtures, fixtures_file)

stats = {'end_time': dt.datetime.now()}

print(f'Execution time: {stats["end_time"] - stats["st_time"]}')
print(f'ServicoDoProduto criados: {stats["servicos_dp_criados"]}')