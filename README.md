# To-do App

## Funcionalidades

* Criar/remover uma secção (ex: Escola, Filmes para ver, Tarefas diárias, etc)
* Criar/remover em cada secção um to-do
* Apresentar para todas as secções os respetivos to-do's

<img src="https://i.imgur.com/05jNN4e.png" alt="drawing" width="500"/>

## Recomendações

* Criar alias no ficheiro perfil da shell (.bashrc, .zshrc, etc), de modo a ser possível o programa ser corrido em qualquer diretoria. 
* Exemplo:

```
alias todo="python3 <path completo para ficheiro main.py>"
```

## Notas

* Alterar o path do ficheiro onde se guarda as tarefas. (ficheiro main.py, linha 7)
* Este ficheiro é o data.txt, que se encontra na mesma diretoria do main.py, sem conteúdo inicial.

## Comandos

* Mostra os to-dos de cada secção

```bash
$ todo
```

* Adiciona um novo to-do a uma secção existente, se não existir também a cria. Data limite opcional.

```bash
$ todo add "nome_secção" "tarefa" ["data"]
```

* Remove um to-do de uma secção (Uso do id em vez de ter que escrever a tarefa toda.)

```bash
$ todo rm "nome_secção" "id-tarefa"
```

* Remove uma secção, incluindo os to-dos dentro dessa secção

```bash
$ todo rs "nome_secção"
```

* Mostra apenas os to-dos com datas

```bash
$ todo datas
```

* Mostra os comandos possíveis

```bash
$ todo help
```

## Dependências

```bash
$ pip3 install tabulate
```