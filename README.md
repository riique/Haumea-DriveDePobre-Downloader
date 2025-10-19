# 🌟 Haumea DriveDePobre Downloader

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

**Modern and elegant downloader for DriveDePobre with beautiful dark theme UI**

[Funcionalidades](#-funcionalidades) • 
[Instalação](#-instalação) • 
[Como Usar](#-como-usar) • 
[Troubleshooting](#-troubleshooting-e-logs)

</div>

---

## 🚀 Visão Geral

O **Haumea DriveDePobre Downloader** é uma aplicação desktop moderna e intuitiva, desenvolvida em Python com `Tkinter`, projetada para simplificar o download de arquivos e pastas hospedados na plataforma de compartilhamento de arquivos `drivedepobre.com`. Com uma interface gráfica elegante e tema escuro, o aplicativo permite escanear URLs de pastas, visualizar o conteúdo de forma hierárquica e selecionar múltiplos itens para download, incluindo o conteúdo de subpastas.

Ideal para quem busca uma ferramenta eficiente e visualmente agradável para gerenciar e baixar grandes volumes de dados de forma organizada.

## ✨ Funcionalidades

*   **Interface Gráfica Moderna (GUI):** Desenvolvida com `Tkinter` usando tema escuro moderno e paleta de cores vibrante para uma experiência visual premium.
*   **Escaneamento de Pastas:** Insira uma URL de pasta (`drivedepobre.com/pasta/ID`) para escanear e listar todos os arquivos e subpastas.
*   **Visualização Hierárquica:** Exibe o conteúdo da pasta em uma estrutura de árvore (`Treeview`), facilitando a navegação e seleção.
*   **Seleção Múltipla:** Permite selecionar arquivos e pastas individualmente ou em massa para download.
*   **Download Recursivo:** Baixa automaticamente todos os arquivos dentro das pastas selecionadas, mantendo a estrutura original.
*   **Barra de Progresso:** Acompanhe o status do download com uma barra de progresso detalhada.
*   **Gerenciamento de Destino:** Escolha facilmente a pasta de destino para seus downloads.
*   **Verificação de Tipo de Item:** Heurística inteligente para diferenciar arquivos e pastas durante o escaneamento.

## 📋 Requisitos

Para executar o **Haumea DriveDePobre Downloader**, você precisará ter o Python instalado em seu sistema. As dependências adicionais são gerenciadas via `pip`.

*   **Python 3.x**
*   **Bibliotecas Python:**
    *   `requests`
    *   `beautifulsoup4`
    *   `selenium`
    *   `tqdm`

## 📦 Instalação

Siga os passos abaixo para configurar e executar o projeto em sua máquina local:

1.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/riique/Haumea-DriveDePobre-Downloader.git
    cd Haumea-DriveDePobre-Downloader
    ```
    *(Substitua pelo link real do seu repositório)*

2.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Como Usar

1.  **Inicie a Aplicação:**
    *   **Windows:** Execute o arquivo `Iniciar.bat`
    *   **Outros SOs (Linux/macOS):** Execute o script `Iniciar.py`
        ```bash
        python Iniciar.py
        ```

2.  **Insira a URL da Pasta:**
    *   Na interface gráfica, cole a URL da pasta do `drivedepobre.com` no campo "URL da Pasta". O formato esperado é `https://drivedepobre.com/pasta/ID`.

3.  **Escanear Pasta:**
    *   Clique no botão "Escanear Pasta". O aplicativo listará todos os arquivos e subpastas encontrados na URL fornecida.

4.  **Selecione os Arquivos para Download:**
    *   Use a visualização em árvore para navegar e selecionar os arquivos e pastas que deseja baixar. Você pode usar "Selecionar Todos" ou "Desmarcar Todos" para facilitar.
    *   Um clique duplo em um item alterna sua seleção.

5.  **Escolha a Pasta de Destino:**
    *   Clique no botão "..." ao lado do campo "Pasta:" para escolher onde os arquivos serão salvos. Por padrão, eles serão salvos em uma pasta `downloads` no diretório do projeto.

6.  **Inicie o Download:**
    *   Clique no botão "Baixar Selecionados" para iniciar o processo de download. A barra de progresso indicará o andamento.

## 📂 Estrutura do Projeto

```
.
├── DriveDePobre_Downloader.py  # Lógica principal da aplicação GUI e download
├── Iniciar.py                  # Script de inicialização da aplicação
├── Iniciar.bat                 # Script de inicialização para Windows
├── requirements.txt            # Lista de dependências do Python
└── README.md                   # README
```

## 🔧 Troubleshooting e Logs

O aplicativo agora inclui um sistema completo de logging para diagnosticar problemas de download.

### Localização dos Logs

Todos os logs são salvos na pasta `logs/` na raiz do projeto:
- **Logs de execução**: `logs/download_log_YYYYMMDD_HHMMSS.txt`
- **HTML de debug**: `logs/html_debug_YYYYMMDD_HHMMSS.html` (quando o padrão de URL não é encontrado)

### O que os logs contêm

- ✅ Informações detalhadas de cada download
- 🔍 Padrões de URL testados
- 🌐 Resposta HTTP completa
- ❌ Mensagens de erro detalhadas
- 📄 HTML da página quando a URL não é encontrada

### Como usar os logs para resolver problemas

1. **Tente fazer um download** que está dando erro
2. **Abra o arquivo de log** mais recente na pasta `logs/`
3. **Procure por** `❌ ERRO` para encontrar o problema
4. **Verifique o HTML salvo** se a mensagem disser "Nenhum padrão de URL de download encontrado"

### Problemas Comuns

**Erro: "Não foi possível obter URL de download"**
- O site pode ter mudado a estrutura HTML
- Verifique o arquivo HTML salvo em `logs/` para ver a nova estrutura
- Procure por padrões de URL no HTML e reporte como issue

**Erro HTTP 403/404**
- O arquivo pode ter sido removido
- O link pode ter expirado
- Verifique se consegue acessar o arquivo manualmente no navegador

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fork este repositório
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m '✨ Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

### 💡 Ideias para Contribuir

- Adicionar suporte para outros serviços de compartilhamento
- Implementar download paralelo
- Adicionar tema claro/escuro alternável
- Melhorar a detecção de URLs de download
- Adicionar testes automatizados

## 👨‍💻 Autor

Criado com 💜 por **[@riiquestudies](https://x.com/riiquestudies)**

🚀 Powered by Haumea Technology

## 🌟 Mostre seu Apoio

Se este projeto te ajudou, considere dar uma ⭐️!

## 📝 Changelog

### v2.0 (2025-10-19)
- 🎨 Interface completamente redesenhada com tema escuro moderno
- 📊 Sistema de logging completo para diagnóstico
- 🔍 Múltiplas estratégias de busca de URL de download
- 🐛 Correção de bugs e melhorias de estabilidade
- ✨ Nova identidade visual "Haumea"

### v1.0
- ✨ Versão inicial
- 📁 Escaneamento de pastas
- ⬇️ Download de arquivos individuais e em massa

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

<div align="center">

**Haumea DriveDePobre Downloader** - Baixe com estilo! 🌟

Made with ❤️ in Brazil

</div>