# χ²stat — Testes Qui-Quadrado

Aplicação web em Flask para execução dos três principais
testes qui-quadrado de inferência estatística.

## Testes implementados

| # | Teste | Quando usar |
|---|-------|-------------|
| 1 | **Aderência** | Verificar se frequências observadas seguem uma distribuição teórica |
| 2 | **Independência** | Verificar se duas variáveis categóricas são independentes (tabela de contingência — 1 amostra) |
| 3 | **Homogeneidade** | Verificar se k populações distintas têm as mesmas proporções (k amostras separadas) |

## Estrutura do projeto

```
stat_inferencia/
├── app/
│   ├── __init__.py          # App factory (Flask)
│   ├── routes.py            # Rotas e lógica de formulário
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── aderencia.py     # Lógica do teste de aderência
│   │   ├── independencia.py # Lógica do teste de independência
│   │   └── homogeneidade.py # Lógica do teste de homogeneidade
│   └── templates/
│       ├── base.html        # Layout base (nav + estilos)
│       ├── index.html       # Página inicial
│       ├── aderencia.html
│       ├── independencia.html
│       └── homogeneidade.html
├── run.py                   # Ponto de entrada
├── requirements.txt
└── README.md
```

## Como rodar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Iniciar o servidor
python run.py

# 3. Acessar no navegador
# http://localhost:5000
```

## Como escalar futuramente

- **Novos testes**: criar `app/tests/novo_teste.py` com a lógica + rota em `routes.py` + template.
- **Banco de dados**: adicionar SQLAlchemy ao `create_app()` para salvar histórico de cálculos.
- **API REST**: expor os testes como endpoints JSON para integração com outros sistemas.
- **Upload de arquivo**: adicionar leitura de CSV/Excel nos formulários.
