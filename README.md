# [Meu Site](https://www.gustavofurtado.com/)

Repositório para os arquivos do meu website, que inclui **[currículo](https://www.gustavofurtado.com/pt/#curriculo)**, **[publicações](https://www.gustavofurtado.com/pt/#publicacoes)** e **[projetos diversos](https://www.gustavofurtado.com/pt/#projetos)**.

Sinceramente, você não encontrará nada interessante aqui. Mas que tal dar uma olhada no meu projeto **[Dados Abertos Brasil](https://github.com/GusFurtado/DadosAbertosBrasil)**?

## Como o site é gerado

O site tem duas versões: inglês em `/` (padrão) e português em `/pt/`. Quem chega em `/` com o navegador em português é redirecionado para `/pt/`, a menos que já tenha escolhido um idioma no seletor.

- `site/template.html`: template único das páginas
- `site/strings.yaml`: textos fixos de cada idioma
- `cv/en.yaml` e `cv/pt.yaml`: currículo (fonte única), lido pelo site e pelo [RenderCV](https://rendercv.com/)

A cada push que altera `cv/` ou `site/`, a GitHub Action `Site e currículo` roda `site/build.py` (gera `index.html` e `pt/index.html`) e o RenderCV (gera os PDFs em `documents/curriculum/`), e faz commit do resultado. Não edite `index.html` nem `pt/index.html` à mão.

Os cards de projetos vêm de `site/projects.yaml`, com o fundo em `assets/img/projects/<id>.svg`. As hero images dos READMEs e o fundo do cabeçalho de cada documentação apontam para esses arquivos: depois de mudar um card, rode `python site/heroes.py` (requer o Playwright) para regenerar os PNGs.

Para o LinkedIn, que não tem API para editar o perfil, `python cv/linkedin.py pt` (ou `en`) imprime o currículo no formato das seções do perfil, para copiar e colar.
