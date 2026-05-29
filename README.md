# Dashboard IA - A Explosão da Inteligência Artificial

Este projeto é um dashboard web sobre o crescimento da Inteligência Artificial, feito para uma atividade acadêmica.

O tema é:

**A Explosão da Inteligência Artificial: Adoção e Impacto**

O dashboard mostra investimentos privados em IA, adoção por setor e crescimento de ferramentas como ChatGPT, Midjourney, Claude, Gemini e Copilot.

## Modelo de governança usado

A interface foi organizada no formato de **dashboard de governança**, parecido com um painel executivo de KPIs.

O painel usa a lógica do **Balanced Scorecard (BSC)**, separando a análise em quatro perspectivas:

- **Financeira**: acompanha o investimento privado global em IA.
- **Mercado**: mostra a adoção de IA por setores da economia.
- **Processos**: avalia a concentração internacional dos investimentos.
- **Aprendizado**: acompanha o crescimento do uso das ferramentas de IA.

Essa estrutura facilita a apresentação porque mostra que o dashboard não é apenas um conjunto de gráficos. Ele conecta dados, objetivos estratégicos, KPIs e resultados.

## Formas de usar o projeto

O projeto funciona de duas formas:

1. **Com Flask**, rodando `python app.py`.
2. **Como página estática**, abrindo o arquivo `index.html` da raiz da pasta.

Essa segunda opção ajuda em apresentação e GitHub Pages, porque não exige abrir um servidor local. Basta clicar em:

```txt
index.html
```

O arquivo estático usa os mesmos dados tratados pelo Python. Sempre que você rodar o projeto com internet, o Python atualiza `data/investimentos_ia.csv` e também recria o `index.html` estático.

## Tecnologias usadas

- Python
- Flask
- Pandas
- Plotly
- HTML5
- CSS3
- JavaScript
- CSV local

## Estrutura de pastas

```txt
dashboard-ia/
│
├── app.py
├── index.html
├── requirements.txt
├── README.md
│
├── data/
│   ├── investimentos_ia.csv
│   ├── setores_adocao_ia.csv
│   └── trafego_ferramentas_ia.csv
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── plotly.min.js
│       └── script.js
│
└── templates/
    └── index.html
```

## O que cada arquivo faz

### `app.py`

É o backend em Python. Ele:

- baixa dados reais de investimento em IA da Our World in Data;
- trata os dados com Pandas;
- salva o resultado em `data/investimentos_ia.csv`;
- calcula os cards no formato Balanced Scorecard;
- envia os dados para o template Flask;
- gera o arquivo estático `index.html`;
- inicia o servidor local quando você roda `python app.py`.

### `index.html`

É a versão estática do dashboard. Pode ser aberta diretamente no navegador, sem Flask.

Essa versão é útil para:

- apresentação em sala;
- GitHub Pages;
- abrir o projeto com duplo clique;
- evitar depender de servidor local no momento da apresentação.

### `templates/index.html`

É o template usado pelo Flask. Ele gera a página quando o projeto roda com `python app.py`.

### `static/css/style.css`

Contém todo o visual do dashboard:

- fundo tecnológico;
- cards;
- responsividade para notebook, tablet e celular;
- tema claro e escuro;
- organização dos gráficos.

### `static/js/script.js`

Contém as interações do frontend:

- renderização dos gráficos com Plotly;
- filtro de país no gráfico de investimentos;
- alternância de tema;
- animação dos cards;
- ajuste dos gráficos em telas menores.

### `data/investimentos_ia.csv`

Contém dados reais de investimento privado em IA, tratados para o formato:

```csv
ano,pais,investimento_bilhoes
```

### `data/setores_adocao_ia.csv`

Contém dados demonstrativos sobre adoção de IA por setor.

### `data/trafego_ferramentas_ia.csv`

Contém dados demonstrativos sobre crescimento de usuários de ferramentas de IA.

## Atualização dos dados reais de investimento em IA

Os dados de investimento em IA agora vêm da **Our World in Data**, com base pública relacionada a investimento privado em empresas de Inteligência Artificial.

A URL principal usada no projeto é:

```txt
https://ourworldindata.org/grapher/private-investment-in-artificial-intelligence.csv?v=1&csvType=full&useColumnShortNames=false
```

Essa base é baseada no AI Index Report / Stanford. Como a série principal pode não trazer todos os países pedidos na versão atual do CSV, o código também usa uma série pública por país da própria Our World in Data quando necessário, sem inventar dados.

O arquivo atualizado é:

```txt
data/investimentos_ia.csv
```

Os países incluídos no dashboard são:

- Global
- EUA
- China
- Reino Unido
- Brasil

Os valores estão em **bilhões de dólares** e são arredondados para duas casas decimais.

Os dados de investimento não são simulados. Eles são baixados, tratados e salvos localmente.

Se o Brasil ou outro país não tiver dado em algum ano na fonte, o projeto não cria valor artificial. O ano simplesmente fica ausente para aquele país.

Para atualizar os dados novamente, rode o projeto com internet:

```bash
python app.py
```

Se a internet falhar, o sistema usa o CSV local salvo anteriormente:

```txt
data/investimentos_ia.csv
```

Se a internet falhar e esse arquivo local também não existir, o dashboard mostra uma mensagem clara de erro.

Os dados de investimento representam financiamento privado externo em empresas de IA. Eles não representam todo o dinheiro gasto com IA em um país, pois não incluem investimento público, gastos internos de grandes empresas, P&D interno nem construção de infraestrutura própria.

## Como instalar o Python

1. Acesse [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. Baixe uma versão recente do Python 3.
3. No Windows, marque a opção **Add Python to PATH** durante a instalação.
4. Finalize a instalação.

Para conferir se funcionou, abra o terminal e rode:

```bash
python --version
```

## Como criar o ambiente virtual

Dentro da pasta `dashboard-ia`, rode:

```bash
python -m venv venv
```

No Windows, ative com:

```bash
venv\Scripts\activate
```

No Linux ou macOS, ative com:

```bash
source venv/bin/activate
```

## Como instalar as dependências

Com o ambiente virtual ativado, rode:

```bash
pip install -r requirements.txt
```

O arquivo `requirements.txt` contém:

```txt
flask
pandas
plotly
```

## Como rodar com Flask

Dentro da pasta `dashboard-ia`, rode:

```bash
python app.py
```

Depois acesse:

```txt
http://127.0.0.1:5000
```

## Como abrir sem servidor local

Depois de rodar o projeto pelo menos uma vez, abra diretamente:

```txt
index.html
```

Esse arquivo fica na raiz da pasta `dashboard-ia`.

Ele já contém os dados preparados para os gráficos, então funciona sem Flask.

## Como usar no GitHub Pages

Para usar no GitHub Pages, envie o projeto para um repositório e configure o Pages para publicar a raiz do repositório.

O GitHub Pages deve encontrar o arquivo:

```txt
index.html
```

Importante: o GitHub Pages não executa Python nem Flask. Por isso, antes de enviar para o GitHub, rode:

```bash
python app.py
```

Isso atualiza os dados e recria o `index.html` estático.

## Como alterar os dados de investimento

O arquivo de investimento é:

```txt
data/investimentos_ia.csv
```

Exemplo de linha:

```csv
2025,EUA,301.02
```

Isso significa que, em 2025, os EUA aparecem com US$ 301,02 bilhões em investimento privado externo em empresas de IA.

Se você editar esse arquivo manualmente, mantenha as colunas:

```csv
ano,pais,investimento_bilhoes
```

Para regenerar o HTML estático depois de editar dados ou textos, rode:

```bash
python app.py
```

## Como adicionar novos países

No `app.py`, procure:

```python
MAPA_PAISES
```

Adicione o nome do país como aparece na fonte e o nome que você quer mostrar no dashboard.

Depois procure:

```python
ORDEM_PAISES_INVESTIMENTO
```

Inclua o novo país na ordem desejada.

Exemplo:

```python
ORDEM_PAISES_INVESTIMENTO = ["Global", "EUA", "China", "Reino Unido", "Brasil", "Alemanha"]
```

O país só aparecerá se existir dado real na fonte usada.

## Como alterar os setores

Abra:

```txt
data/setores_adocao_ia.csv
```

Exemplo:

```csv
Marketing,74
```

Para mudar o percentual:

```csv
Marketing,80
```

Para adicionar novo setor:

```csv
Agronegócio,42
```

Depois recarregue a página.

## Como alterar as ferramentas de IA

Abra:

```txt
data/trafego_ferramentas_ia.csv
```

Exemplo:

```csv
2025,ChatGPT,320
```

Para adicionar uma nova ferramenta:

```csv
2023,Perplexity,8
2024,Perplexity,25
2025,Perplexity,50
```

## Como mudar os textos da página

Abra:

```txt
templates/index.html
```

Para trocar o título, procure:

```html
<h1>A Explosão da Inteligência Artificial</h1>
```

Para trocar o subtítulo, procure:

```html
Adoção, investimentos e impacto das ferramentas de IA no mercado global
```

Depois de alterar, rode:

```bash
python app.py
```

Assim o `index.html` estático também será atualizado.

## Como mudar as cores

Abra:

```txt
static/css/style.css
```

No começo do arquivo existem variáveis:

```css
:root {
    --accent: #42d8ff;
    --accent-2: #9b7cff;
    --accent-3: #35e0a1;
}
```

Para mudar a cor principal, altere:

```css
--accent: #00bcd4;
```

## Como alterar os gráficos

Os gráficos ficam no arquivo:

```txt
static/js/script.js
```

Funções principais:

- `renderInvestmentChart()`: gráfico de investimento em IA.
- `renderSectorChart()`: gráfico de adoção por setor.
- `renderTrafficChart()`: gráfico de crescimento de usuários.

O gráfico de investimento começa mostrando todos os países. O seletor permite filtrar para Global, EUA, China, Reino Unido ou Brasil.

## Como modificar os cards de resumo

Os cards são calculados no arquivo:

```txt
app.py
```

Procure a função:

```python
montar_cards_investimento()
```

Ela cria os cards:

- investimento global mais recente;
- país com maior investimento no ano mais recente;
- investimento mais recente dos EUA;
- investimento mais recente da China;
- investimento mais recente do Reino Unido;
- investimento mais recente do Brasil.

## Responsividade

O dashboard foi ajustado para:

- notebook;
- monitor desktop;
- tablet;
- celular.

Em telas menores:

- os cards ficam empilhados;
- o menu pode rolar horizontalmente;
- os gráficos aumentam a altura para facilitar leitura;
- margens e títulos dos gráficos ficam mais compactos.

## Erros comuns

### `python` não é reconhecido

O Python pode não estar instalado ou não foi adicionado ao PATH.

Solução:

- reinstale o Python;
- marque **Add Python to PATH**;
- feche e abra o terminal.

### `No module named flask`

As dependências não foram instaladas.

Solução:

```bash
pip install -r requirements.txt
```

### Erro ao baixar dados reais

Pode ser falha de internet ou bloqueio temporário da fonte.

Solução:

- verifique a conexão;
- rode novamente `python app.py`;
- se já existir `data/investimentos_ia.csv`, o sistema usa esse arquivo local.

### O GitHub Pages não atualizou os dados

O GitHub Pages não roda Python. Antes de enviar para o GitHub, rode localmente:

```bash
python app.py
```

Depois envie o `index.html` e os arquivos da pasta `static/` e `data/`.

### Porta 5000 em uso

Outro servidor pode estar usando a porta 5000.

No final do `app.py`, você pode trocar:

```python
app.run(debug=True, host="127.0.0.1", port=5000)
```

por:

```python
app.run(debug=True, host="127.0.0.1", port=5001)
```

## Observação final

Este projeto foi feito para fins acadêmicos. Os dados de investimento vêm de fonte pública e os demais dados servem como demonstração visual para facilitar a apresentação do tema.
# Dashboard-IA
