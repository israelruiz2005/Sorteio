# Projeto acadêmico de sorteio para amigo secreto

* Este projeto foi desenvolvido conforme treinamento realizado de Julia Rizza, usa o framework web2py para desenvolvimento web.

## Estrutura do projeto
Propositalmente foi removida do projeto a pasta private por conter dados de conexão.

Para executar o projeto é necessário realizar o download do web2py, criar o projeto e só depois clonar ou baixar os arquivos aqui disponibilizados.

Este projeto implementará o uso de templates para login, ações de CRUD e aplicará a estrutura MVC.

## Autenticação e autorização

A autenticação é o processo de determinar se a solicitação veio de um usuário válido que possui os privilégios necessários para usar o sistema. No mundo das redes de computadores, esse é um requisito vital, pois muitos sistemas continuam interagindo entre si e o mecanismo adequado precisa garantir que apenas interações válidas ocorram entre esses programas.

A autorização já indica quais recursos podem ser acessados pelo usuário em uma aplicação após ele ser autenticado para usar o sistema, ou seja, após realizar um login bem-sucedido o que ele pode fazer.

Neste projeto utilizaremos o Auth para realizar ambas as atividades.

## Template
Foi utilizado como base o template © Copyright NiceAdmin [Designed by BootstrapMade](https://bootstrapmade.com/) com alterações para o projeto.

## Rotas
Uma vez aplicação criada, podemos utilizar personalização de rotas para facilitar a navegação, o web2py possui alguns exemplos de rota, neste app utilizaremos o mais simples conhecida como **routes parametric**, existe uma pasta exemplo com documentação completa.
Para iniciar é necessário a criação de um arquivo routes.py na raiz da aplicação, neste projeto deixamos um arquivo dentro da pasta, porém ele deverá ser movido após instalação.
