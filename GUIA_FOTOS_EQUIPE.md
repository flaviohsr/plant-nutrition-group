# Fotos da equipe

O site suporta agora o campo opcional `photo_url` em cada integrante de `members.json`. A imagem aparece ao lado do nome, e um avatar de iniciais é usado quando não houver fotografia confirmada.

Exemplo:
```json
{"members":[{"name":"Nome Completo","role":"Pesquisador(a)","institution":"ESALQ/USP","profile_url":"https://...","photo_url":"fotos/nome.jpg"}]}
```

**Validação necessária:** antes de associar uma foto encontrada em Instagram, Lattes ou outra fonte, confirmar identidade, vínculo oficial com o grupo e permissão/licença de reutilização. Evitar usar fotos de homônimos. Para estabilidade e direitos de uso, prefira fotografias fornecidas pelos próprios integrantes e armazenadas na pasta `fotos/` do site. A lista oficial de integrantes ainda depende de uma fonte DGP/CNPq acessível; não inventar membros.
