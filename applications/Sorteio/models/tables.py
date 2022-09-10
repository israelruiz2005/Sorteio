# -*- coding: utf-8 -*-
# Definição da tabela grupo e seus campos para criação 

Grupo = db.define_table('grupo',
    Field('nome', label ='Nome'),
    Field('data_sorteio', 'date', label =T('Data do sorteio')),
    Field('data_revelacao','date', label =T('Data de revelação')),
    Field('valor_maximo','float', label =T('Valor máximo')),
    Field('hash_id'),
    auth.signature
)
# Definição da tabela usuario_grupo e seus campos para criação
Usuario_Grupo = db.define_table('usuario_grupo',
    Field('id_auth_user','reference auth_user', label =T('Código do usuário')),
    Field('id_grupo','reference grupo', label =T('Código do grupo'))
)

# Definição da tabela forum e seus campos para criação
Forum = db.define_table('forum',
    Field('mensagem','text', label =T('Mensagem')),
    Field('id_grupo','reference grupo', label =T('Código do grupo')),
    auth.signature
)

# Definição da tabela lista de desejos e seus campos para criação
Lista_Desejos = db.define_table('lista_desejos',
    Field('presente', label =T('Presente')),
    Field('imagem', 'upload', label =T('Imagem do presente')),
    Field('id_auth_user', 'reference auth_user', label =T('Código do usuário'))
)

Sorteio = db.define_table('sorteio',
    Field('participantes', 'list:reference auth_user'),
    Field('id_grupo','reference grupo'),
    auth.signature
    )