# To-do App

## Funcionalidades

* Criar/remover to-do's.
* Criar/remover uma secção (ex: GERAL, Escola, Filmes para ver, Tarefas diárias, etc).
* Apresentar para todas as secções os respetivos to-do's.

<img src="https://i.imgur.com/05jNN4e.png" alt="drawing" width="500"/>

## Instalação

- Colocar a pasta num local definitivo, caso contrário será preciso correr os próximos comandos outra vez.

```bash 
$ cd terminal-based-todo-app-main
$ chmod +x install
$ sh install
```

## Comandos

* Mostra os to-dos de cada secção

```bash
$ todo
```

* Adiciona um novo to-do na secção "Geral", e se não existir também a cria. Data limite opcional.

```bash
$ todo add "tarefa" ["data"]
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

- Python3
- Tabulate 

```bash
$ pip3 install tabulate
```