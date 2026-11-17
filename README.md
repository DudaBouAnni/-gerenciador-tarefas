# TaskFlow - Sistema de Gerenciamento de Tarefas

## Descrição do projeto

O TaskFlow é um sistema de gerenciamento de tarefas desenvolvido como projeto acadêmico de Engenharia de Software. Seu objetivo é permitir o cadastro, a consulta, a atualização e a exclusão de tarefas.

## Tecnologias utilizadas

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pytest
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

## Como executar o projeto

1. Clone o repositório.
2. Crie e ative um ambiente virtual.
3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute a aplicação:

```bash
uvicorn src.main:app --reload
```

5. Acesse a documentação interativa da API em `http://127.0.0.1:8000/docs`.

## Testes automatizados

Para executar os testes, utilize:

```bash
pytest -v
```

O projeto possui 10 testes automatizados para verificar as funcionalidades da aplicação.

## Integração contínua

O GitHub Actions executa automaticamente os testes a cada envio de alterações ao repositório e em pull requests.

## Mudança de escopo

Durante o desenvolvimento, foi identificada a possibilidade de melhorar a consulta das tarefas. Inicialmente, o sistema permitia apenas listar todas as tarefas. Como mudança de escopo, foi adicionada a funcionalidade de filtragem por status.

Com essa melhoria, o usuário pode consultar tarefas específicas utilizando os status "A Fazer", "Em Progresso" ou "Concluído".

A mudança foi registrada no Kanban do GitHub Projects, implementada no código e documentada por meio de um commit específico. Também foram adicionados três testes automatizados para validar o funcionamento do filtro.