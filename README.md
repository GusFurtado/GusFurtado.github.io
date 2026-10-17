# [Meu Site](https://www.gustavofurtado.com/)

Repositório para os arquivos do meu website, que inclui **[currículo](https://www.gustavofurtado.com/#curriculo)**, **[trabalhos acadêmicos](documents/README.md)** e **[projetos diversos](https://www.gustavofurtado.com/#projetos)**.

Sinceramente, você não encontrará nada interessante aqui. Mas que tal dar uma olhada no meu projeto **[Dados Abertos Brasil](https://github.com/GusFurtado/DadosAbertosBrasil)**?

## Currículo

O currículo vem de `cv/pt.yaml` e `cv/en.yaml`. A cada push que altera `cv/`, a GitHub Action `Currículo` gera os PDFs em `documents/curriculum/` (com [RenderCV](https://rendercv.com/)) e a seção "Meu currículo" do `index.html` (com `cv/build_site.py`).
