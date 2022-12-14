# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def index():
      
    form = SQLFORM.factory(
        Field('nome', label=T('Nome'), requires=IS_NOT_EMPTY()),
        Field('email', label=T('E-mail'), requires=IS_EMAIL()),
        Field('mensagem', label=T('Deixe sua mensagem'), requires=IS_NOT_EMPTY())
    )
    if form.process().accepted:
        msg ="""
        <html>
            <b>Você recebeu uma mensagem de %s:</b><br/>
            %s
        </html>
        """  % (form.vars.nome, form.vars.mensagem)
        mail.send(
            to = ["israel.ruiz.recupera@gmail.com"],
            reply_to = form.vars.email,
            subject=" Mensagem recebida em sorteio.com",
            message= msg
        )
        response.flash = T('Formulário enviado')
        form.vars.Nome
        form.vars.email
        form.vars.mensagem
    elif form.errors:
        response.flash = T('Ocorreram erros')
    return dict(form=form)

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    if request.args(0)== 'login':
        retorno = response.render('default/login.html', dict(form=auth()))
    elif request.args(0) == 'register':   
         retorno = response.render('default/register.html', dict(form=auth()))     
    elif request.args(0) == 'retrieve_password':   
         retorno = response.render('default/retrieve_psw.html', dict(form=auth())) 
    else:
        retorno = response.render('default/user.html', dict(form=auth()))
    
    return retorno

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

# FORMULARIO DE CONTATO SEM TABELA NO BANCO DE DADOS

# Inicia as páginas

# Grupo
@auth.requires_login()
def dashboard():
    participa_em =[]
    for grupo in db(Grupo).select():
        if participa_grupo(grupo.id):
            participa_em.append(grupo.id)

    grupos =db(Grupo.created_by == auth.user.id or
               Grupo.id.belongs(participa_em)).select()
    return dict(grupos = grupos)

@auth.requires(lambda: participa_grupo(request.args(0, cast=int)) or \
                       dono_grupo(request.args(0, cast=int)) or \
                       auth.has_membership('Administrador'))
def grupo():
    id_grupo = request.args(0, cast=int)
    grupo = db(Grupo.id == id_grupo).select().first()
    p = db(Usuario_Grupo.id_grupo == id_grupo).select()
    participantes = [ x.id_auth_user for x in p] #list compreension
    participantes.append(grupo.created_by)

    sorteio = db(Sorteio.id_grupo == grupo.id).select().first()

    return dict(grupo=grupo, participantes=participantes,sorteio=sorteio)

@auth.requires_login()
def novo_grupo():
   
    form = SQLFORM(Grupo)
    if form.process().accepted:
        response.flash = T("Registro incluido")
    elif form.errors:
        response.flash = T("O formulario contem erros")
    
    return dict(form=form)

@auth.requires(lambda: dono_grupo(request.args(0, cast=int)) or auth.has_membership('Administrador'))
def atualizar_grupo():
    id_grupo = request.args(0, cast=int)
   
    form = SQLFORM(Grupo, id_grupo, showid=False)
    if form.process().accepted:
        response.flash = T("Registro atualizado")
    elif form.errors:
        response.flash = T("O formulario contem erros")
    return dict(form=form)

@auth.requires(lambda: dono_grupo(request.args(0, cast=int)) or auth.has_membership('Administrador'))
def apagar_grupo():
    id_grupo = request.args(0, cast=int)
    db(Grupo.id == id_grupo).delete()
    redirect(URL(f='dashboard'))

#Convida amigos
@auth.requires(lambda: participa_grupo(request.args(0, cast=int)) or \
                       dono_grupo(request.args(0, cast=int))  or \
                       auth.has_membership('Administrador'))
def convidar_amigo():
    id_grupo = request.args(0, cast = int)
    grupo = db(Grupo.id == id_grupo).select().first()
    form = SQLFORM.factory (
        Field('nome', label="Nome do amigo"),
        Field('email', label="Email do amigo")
    )
    if form.process().accepted:
        mail.send(
            to = form.vars.email,
            subject = "Você foi convidado para um grupo de amigo secreto",
            message = """
                        Você foi convidado para um grupo de amigo secreto por %s %s. Para participar acesse:
                        %s
            """ % (auth.user.first_name, auth.user.last_name, URL('adiciona_amigo', args=grupo.hash_id,scheme=True, host=True))
        )
    return dict(form=form)

#Adiciona amgio
@auth.requires_login()
def adiciona_amigo():
    hash_grupo = request.args(0)
    grupo = db(Grupo.hash_id == hash_grupo).select().first()
    if not db((Usuario_Grupo.id_grupo == grupo.id) & \
             (Usuario_Grupo.id_auth_user == auth.user.id)).count() and not\
             grupo.created_by == auth.user.id:
        Usuario_Grupo.insert(id_auth_user=auth.user.id, id_grupo=grupo.id)
    redirect(URL('grupo', args=grupo.id))

# Sortear
def sortear():
    id_grupo = request.args(0, cast=int)
    grupo = db(Grupo.id == id_grupo).select().first()
    p = db(Usuario_Grupo.id_grupo == id_grupo).select()
    
    participantes = [x.id_auth_user for x in p]
    participantes.append(grupo.created_by)
    
    r = realizar_sorteio(participantes)
    if db(Sorteio.id_grupo == id_grupo).count():
        db(Sorteio.id_grupo == id_grupo).update(participantes=r)
    else:
        Sorteio.insert(participantes=r, id_grupo=id_grupo)
    
    for p in participantes:
        if participantes.index(p) == len(participantes)-1:
            amigo = participantes[0]
        else:
            amigo = participantes[participantes.index(p)+1]

        mail.send(
            to=p.email,
            subject = "Resultado do amgio secreto",
            message= "Você saiu com %s %s" %(amigo.first_name, amigo.last_name)
        )        
    redirect(URL('grupo', args=id_grupo))

# Forum com formulario
@auth.requires(lambda: participa_grupo(request.args(0, cast=int)) or auth.has_membership('Administrador'))
def forum():
    id_grupo = request.args(0, cast=int)
   
    # rotina para paginaçao
    if not request.vars.page or int(request.vars.page)<=0:
        redirect(URL(args=request.args, vars={'page':1}))
    else:
        pagina = int(request.vars.page)

    inicio=(pagina-1)*10
    fim=pagina*10

    # Efetua busca
    if request.vars.q:
        q = request.vars.q
        mensagens = db((Forum.id_grupo == id_grupo)&(Forum.mensagem.like('%'+q+'%'))).select(orderby=Forum.created_on, limitby=(inicio,fim))
    else:
        mensagens = db(Forum.id_grupo == id_grupo).select(orderby=Forum.created_on, limitby=(inicio,fim))
    # calcula o maximo de paginas para apresentar
    qtd_pags = int((db(Forum.id_grupo == id_grupo).count()/10)+1)
   
    if int(request.vars.page) > qtd_pags:
        redirect(URL(args=request.args,vars={'page':qtd_pags}))

    Forum.id_grupo.default = id_grupo
    Forum.id_grupo.writable = Forum.id_grupo.readable = False
   
    form = SQLFORM(Forum)
   
    if form.process().accepted:
        response.flash = T("Registro incluido")
    elif form.errors:
        response.flash = T("O formulario contem erros")
    
   
   
    return dict(mensagens = mensagens, form=form)

@auth.requires(lambda: db(Forum.id == request.args(0, cast=int)).select().first().created_by == auth.user.id or \
                       auth.has_membership("Administrador") )
def editar_mensagem():
    id_registro = request.args(0, cast=int)
    Forum.id_grupo.writable = Forum.id_grupo.readable = False
    form = SQLFORM(Forum, id_registro, showid=False)
    if form.process().accepted:
        response.flash = T("Registro atualizado")
    elif form.errors:
        response.flash = T("O formulario contem erros")
    return dict(form=form, id_grupo=db(Forum.id == id_registro).select().first().id_grupo)

@auth.requires(lambda: db(Forum.id == request.args(0, cast=int)).select().first().created_by == auth.user.id or \
                       auth.has_membership("Administrador") )
def apagar_mensagem():
    id_registro = request.args(0, cast=int)
    msg = db(Forum.id == id_registro).select().first()
    id_grupo = msg.id_grupo
    db(Forum.id == id_registro).delete()
    redirect(URL('forum', args=[id_grupo]))    

# Lista de desejos
#@auth.requires_login()
def desejos():
    
    id_usuario = request.args(0, cast=int)
    query = (Lista_Desejos.id_auth_user == id_usuario)
    desejos =db(query).select()
    usuario = db(db.auth_user.id == id_usuario).select().first()
    return dict(desejos = desejos, usuario=usuario)

    grid = SQLFORM.grid(query, args=request.args[:1])
    return dict(grid=grid)

def novo_desejo():
    id_usuario = request.args(0, cast=int)

    Lista_Desejos.id_auth_user.default = id_usuario
    Lista_Desejos.id_auth_user.writable = False

    form = SQLFORM(Lista_Desejos)
    if form.process().accepted:
        response.flash = T("Registro incluido")
    elif form.errors:
        response.flash = T("O formulario contem erros")
    
    return dict(form=form)

def editar_desejo():
    
    id_registro = request.args(0, cast=int)
    Lista_Desejos.id_auth_user.writable = False
    form = SQLFORM(Lista_Desejos, id_registro, showid=False)
    if form.process().accepted:
        response.flash = T("Registro atualizado")
    elif form.errors:
        response.flash = T("O formulario contem erros")
    return dict(form=form)


def apagar_desejo():
    id_registro = request.args(0, cast = int)
    desejo = db(Lista_Desejos.id == id_registro).select().first()
    db(Lista_Desejos.id == id_registro).delete()
    redirect(URL('desejos', args=[desejo.id_auth_user]))