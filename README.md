# TaskFlow - Sistema de Gerenciamento de Tarefas

## Descrição do projeto

O TaskFlow é um sistema de gerenciamento de tarefas desenvolvido como projeto acadêmico de Engenharia de Software. Seu objetivo é permitir o cadastro, a consulta, a atualização e a exclusão de tarefas por meio de uma interface web e de uma API.

## Tecnologias utilizadas

- Python
- FastAPI
- SQLite
- SQLAlchemy
- HTML, CSS e JavaScript
- Jinja2
- Pytest
- Ruff
- Git e GitHub
- GitHub Actions

## Funcionalidades

- Criar tarefas.
- Listar todas as tarefas.
- Consultar uma tarefa pelo ID.
- Atualizar tarefas.
- Excluir tarefas.
- Definir prioridade e status das tarefas.
- Filtrar tarefas pelo status.
- Gerenciar tarefas por meio de uma interface web.

## Como executar o projeto

1. Clone o repositório.
2. Crie e ative um ambiente virtual.
3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute a aplicação:

```bash
python -m uvicorn src.main:app --reload
```

5. Acesse a aplicação pelo endereço:

`http://127.0.0.1:8000`

6. A documentação interativa da API está disponível em:

`http://127.0.0.1:8000/docs`

## Testes automatizados

Para executar os testes, utilize:

```bash
python -m pytest -v
```

O projeto possui 11 testes automatizados com Pytest, responsáveis por verificar as funcionalidades da aplicação, incluindo operações CRUD, validações, filtros e acesso à página inicial.

## Qualidade do código

O projeto utiliza o Ruff para verificar a qualidade e a organização do código Python.

Para executar a verificação manualmente:

```bash
python -m ruff check src tests
```

## Integração contínua

O GitHub Actions executa automaticamente duas verificações a cada envio de alterações ao repositório e em pull requests:

- Verificação da qualidade do código com Ruff.
- Execução dos testes automatizados com Pytest.

## Mudança de escopo

Durante o desenvolvimento, foi identificada a possibilidade de melhorar a consulta das tarefas. Inicialmente, o sistema permitia apenas listar todas as tarefas. Como mudança de escopo, foi adicionada a funcionalidade de filtragem por status.

Com essa melhoria, o usuário pode consultar tarefas específicas utilizando os status "A Fazer", "Em Progresso" ou "Concluído".

A mudança foi registrada no Kanban do GitHub Projects, implementada no código e documentada por meio de um commit específico. Também foram adicionados três testes automatizados para validar o funcionamento do filtro.