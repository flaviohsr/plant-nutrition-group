# Sincronização de publicações com o Lattes

O site lê `publications.json` quando publicado em um servidor HTTP(S). O script `sync_lattes.py` importa publicações do XML oficial do currículo Lattes, preservando títulos, autores, anos, veículo e DOI quando disponíveis.

## Como ativar
1. Crie um repositório GitHub com todos os arquivos desta pasta e publique-o por GitHub Pages (Settings > Pages > Deploy from branch).
2. Exporte o currículo Lattes do coordenador em **XML** pelo sistema do CNPq e envie-o ao repositório com o nome `lattes.xml` (raiz do projeto).
3. A ação do GitHub processará o XML automaticamente após cada atualização desse arquivo e atualizará `publications.json` no repositório.
4. O site exibirá o catálogo atualizado após a publicação do novo arquivo JSON.

**Limitação:** isso NÃO detecta automaticamente uma alteração feita apenas no portal Lattes. O CNPq não disponibiliza um endpoint público estável e garantido para baixar automaticamente o XML de qualquer pesquisador. É necessário exportar e enviar um novo XML quando o currículo mudar, ou contratar/autorizar um serviço de integração institucional com acesso ao Lattes e conectá-lo ao fluxo. Não insira senhas ou credenciais do Lattes no repositório.

**Nota:** o site mantém uma seleção anterior como fallback até existir um `publications.json` válido. Para testar localmente, execute `python -m http.server 8000` na pasta e abra `http://localhost:8000`.

## Sincronização da equipe (DGP/CNPq)

A página Equipe lê `members.json` publicado no mesmo domínio. A atualização diária foi preparada em `.github/workflows/members.yml`, mas **não está ativa** até a publicação do site no GitHub e a configuração de uma fonte autorizada.

**Atenção:** o endereço `dgp.cnpq.br/dgp/espelhorh/0807911743415172#gruposPesquisa` é a página de um pesquisador, não uma exportação estruturada de integrantes de um grupo específico. O acesso automático à página falhou por redirecionamentos. Não é correto derivar membros de orientações, projetos ou outros grupos do coordenador.

Para ativar, obtenha uma fonte HTTPS confiável e autorizada que publique o grupo correto no formato JSON `{"members":[{"name":"Nome completo","role":"Pesquisador(a)","institution":"ESALQ/USP","profile_url":"https://..."}]}`. No GitHub, configure a variável de repositório `DGP_MEMBERS_FEED_URL` com essa URL (Settings > Secrets and variables > Actions > Variables). O workflow consulta a fonte diariamente, valida o JSON e publica `members.json` quando disponível. Uma página HTML do DGP **não** funciona como essa fonte sem um conector específico e autorizado.

Até a fonte ser fornecida, a seção não inventa uma relação de integrantes nem apresenta estudantes orientados como membros certificados do grupo. O coordenador continua identificado separadamente.

## Projetos e publicações (mesma fonte Lattes)
O script `sync_lattes.py` agora produz **projects.json** e **publications.json** a partir de `lattes.xml`, com validação do ID 0807911743415172. O GitHub Actions atualiza os dois arquivos quando um XML novo é enviado ao repositório. O site usa esses arquivos automaticamente, mantendo o conteúdo anterior como reserva enquanto não houver XML.

**Limitação:** o link público do Lattes não fornece, por si só, um feed aberto que permita garantir atualização automática a cada mudança do currículo. Para sincronização sem exportar XML, é preciso integrar o serviço institucional autorizado **Lattes Extrator** do CNPq, com suporte da TI da instituição, ou outra fonte autorizada. Sem essa integração, a atualização automática ocorre após o envio do XML, e não diretamente após a edição do CV no portal.
