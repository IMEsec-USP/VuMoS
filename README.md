# RDB

## Scanner de vulnerabilidades

Antes de executar o arquivo, o OWASP ZAP deve estar rodando e a chave da API deve ser colocada
num arquivo chamado `token` para que o script possa funcionar de maneira adequada.

OWASP ZAP: <https://github.com/zaproxy>

Para pegar sua chave da API:

Vá no menu de configurações, denotado pelo símbolo de roda dentada na barra superior.
No menu __API__, copie sua chave que estará numa caixa de texto.

Na pasta obtida após clonar esse repositório, crie um arquivo chamado __token__
e cole sua chave da API nele.

## Execução

```
python3 testescan.py <url_alvo>
```

As URLs obtidas pela spider serão salvas num arquivo `spider_results.txt`, e as possíveis
vulnerabilidades serão salvas num arquivo JSON de nome vulns.json.
