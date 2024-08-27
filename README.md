# Insta Downloader

Insta Downloader é um aplicativo de desktop para baixar vídeos e áudios do Instagram. Ele permite aos usuários baixar conteúdo de posts, reels e IGTV do Instagram de forma fácil e rápida.

## Características

- Interface gráfica simples e intuitiva
- Baixa vídeos do Instagram
- Opção para extrair apenas o áudio dos vídeos
- Barra de progresso para acompanhar o download
- Suporte para Windows, macOS e Linux

## Tecnologias Utilizadas

- Electron.js para a interface de desktop
- Python para o script de download
- Instaloader para interação com a API do Instagram
- MoviePy para processamento de vídeo/áudio

## Pré-requisitos

- Node.js (v12 ou superior)
- Python (v3.6 ou superior)
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/insta-downloader.git
   cd insta-downloader
   ```

2. Instale as dependências do Node.js:
   ```
   npm install
   ```

3. Instale as dependências Python:
   ```
   pip install instaloader moviepy requests
   ```

## Uso

Para iniciar o aplicativo em modo de desenvolvimento:
npm start

## Estrutura do Projeto

- `main.js`: Arquivo principal do Electron
- `renderer.js`: Script para a interface do usuário
- `preload.js`: Script de pré-carregamento para comunicação segura
- `downloader.py`: Script Python para download de vídeos/áudios
- `index.html`: Página HTML principal
- `styles.css`: Estilos CSS para a interface

## Contribuindo

Contribuições são bem-vindas! Por favor, leia as diretrizes de contribuição antes de enviar pull requests.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Autor

Lairton - [GitHub](https://github.com/Lairton)
