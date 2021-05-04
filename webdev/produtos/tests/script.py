def get_dados_do_produto(model):
    doc = model.__doc__.split(', ')
    attr = []
    for a in doc:
        if a == doc[0]:
            attr.append(a.split('(')[1])
        elif a == doc[-1]:
            attr.append(a.split(')')[0])
        else: 
            attr.append(a)

    data = {}
    for a in attr:
        if model.__dict__[a] != None:
            if a == 'foto':
                data[a] = model.foto.url
            else:
                data[a] = model.__dict__[a]

    return data
