# To-do App

## Funcionalidades

* Criar/remover to-do's.
* Criar/remover uma secção (ex: GERAL, Escola, Filmes para ver, Tarefas diárias, etc).
* Apresentar para todas as secções os respetivos to-do's.

<img src="https://i.imgur.com/05jNN4e.png" alt="drawing" width="500"/>

## Notas

- Correr o script install.sh com o comando: 
    - `zsh install.sh` - para adicionar um alias ao ficheiro `~/.zshrc`.
    - `sh install.sh` - para adicionar um alias ao ficheiro `~/.bash_profile`.
    - para outras shells este processo terá de ser feito manualmente. 😔

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