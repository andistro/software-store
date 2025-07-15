# Software Store

Loja de aplicativos gráfica para Debian/Ubuntu rodando no Termux (proot-distro), compatível com arm64/armhf, leve e integrada ao sistema.

## Instalação

1. Baixe ou clone os arquivos do projeto para uma pasta (ex: `~/Downloads/software-store`).
2. Abra o terminal na pasta do projeto.
3. Execute o instalador:

   ```bash
   chmod +x install.sh
   ./install.sh
   ```

4. Após a instalação, execute o Software Store:

   ```bash
   software-store
   ```

## Funcionalidades

- Busca e instala pacotes dos repositórios apt do sistema.
- Interface gráfica responsiva, integrada ao tema GTK.
- Suporte a múltiplos idiomas (pt-br, en-us).
- Página inicial com saudação dinâmica e campo de busca.
- Página de detalhes do pacote com ícone, versão, descrição e screenshots.
- Deep link para abrir detalhes de pacotes diretamente.
- Botão para procurar e instalar atualizações.
- Ignora Snap e Flatpak (não suportados no Termux/proot-distro).
- Cria atalho no menu de aplicativos.

## Deeplink

Você pode abrir detalhes de um pacote diretamente pelo navegador ou outro app usando o esquema:

```
software-store://pkg?search=nome-do-pacote
```

Exemplo para o Inkscape:

```
software-store://pkg?search=inkscape
```

Ao acessar esse link, o Software Store abrirá uma janela de detalhes do pacote solicitado.

## Testando Deeplink pelo Terminal

Você pode testar o deeplink diretamente pelo terminal, passando a URI como argumento para o comando:

```bash
software-store "software-store://pkg?search=inkscape"
```

Se houver algum erro, a mensagem será exibida no terminal.  
Isso é útil para depuração e para garantir que o Software Store está interpretando corretamente o argumento.

## Como usar

- **Buscar aplicativos:** Digite o nome do aplicativo no campo de busca e pressione Enter ou clique em "Pesquisar".
- **Instalar/Remover:** Clique no botão "Instalar" ao lado do aplicativo desejado. Para remover, abra os detalhes e clique em "Remover".
- **Atualizar pacotes:** Clique em "Procurar atualizações" na página inicial.
- **Abrir pelo menu:** Após instalar, procure por "Software Store" no menu de aplicativos do seu ambiente gráfico.

## Observações

- O Software Store só funciona com pacotes apt dos repositórios configurados no sistema.
- Snap e Flatpak não são suportados.
- Para que o atalho apareça no menu, o instalador copia o arquivo `.desktop` para `/usr/share/applications`.
- Pacotes que exigem parâmetros especiais (ex: `--no-sandbox`) são tratados automaticamente.

## Observações sobre Deeplink

- O deeplink funciona diretamente pelo terminal, passando a URI como argumento para o comando `software-store`.
- Para que o deeplink funcione ao clicar em links no navegador, é necessário que o sistema esteja configurado para associar o esquema `software-store://` ao aplicativo Software Store.
- Caso o navegador apenas tente abrir o comando `software-store://pkg?search=inkscape`, sem passar como argumento para o aplicativo, a página inicial será aberta.
- Para integração total, edite o arquivo `.desktop` do Software Store e adicione a linha abaixo para registrar o esquema de URI:

  ```
  MimeType=x-scheme-handler/software-store;
  ```

- Após isso, atualize o banco de dados de aplicativos do sistema com:

  ```bash
  update-desktop-database
  ```

- Assim, ao clicar em links `software-store://...` no navegador, o Software Store será chamado com o argumento correto e abrirá a página de detalhes do pacote.

## Suporte

Para dúvidas, sugestões ou problemas, abra uma issue neste repositório.