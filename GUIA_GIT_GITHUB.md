# 🚀 Guia de Deploy no GitHub - Haumea DriveDePobre Downloader

## 📝 Passo 1: Configurar o Git (Primeira Vez)

Abra o **PowerShell** ou **CMD** e execute os seguintes comandos:

```bash
# Configurar seu nome (use seu nome real ou nome de usuário)
git config --global user.name "Seu Nome"

# Configurar seu email (use o email da sua conta GitHub)
git config --global user.email "seuemail@exemplo.com"

# Verificar as configurações
git config --list
```

**Exemplo:**
```bash
git config --global user.name "Henri"
git config --global user.email "henri@exemplo.com"
```

---

## 📁 Passo 2: Inicializar o Repositório Git

No terminal, navegue até a pasta do projeto:

```bash
# Entrar na pasta do projeto
cd "C:\Users\Henri\Documents\00 - Outros\DriveDownloader"

# Inicializar o repositório Git
git init

# Verificar status dos arquivos
git status
```

---

## 📋 Passo 3: Adicionar Arquivos ao Git

```bash
# Adicionar todos os arquivos ao staging
git add .

# OU adicionar arquivos específicos
git add DriveDePobre_Downloader.py
git add README.md
git add requirements.txt
git add .gitignore

# Verificar o que foi adicionado
git status
```

---

## 💾 Passo 4: Fazer o Primeiro Commit

```bash
# Criar o primeiro commit
git commit -m "🌟 Initial commit - Haumea DriveDePobre Downloader v2.0"

# Verificar o histórico
git log --oneline
```

---

## 🌐 Passo 5: Criar Repositório no GitHub

1. **Acesse:** https://github.com
2. **Faça login** na sua conta
3. **Clique no botão "+"** no canto superior direito
4. **Selecione "New repository"**
5. **Configure o repositório:**
   - **Repository name:** `Haumea-DriveDePobre-Downloader`
   - **Description:** `🌟 Modern downloader for DriveDePobre with beautiful dark theme UI`
   - **Public** ou **Private** (sua escolha)
   - **NÃO** marque "Add a README file" (já temos um)
   - **NÃO** marque "Add .gitignore" (já temos um)
6. **Clique em "Create repository"**

---

## 🔗 Passo 6: Conectar ao Repositório do GitHub

Após criar o repositório, o GitHub mostrará comandos. Use estes:

```bash
# Adicionar o repositório remoto
git remote add origin https://github.com/SEU_USUARIO/Haumea-DriveDePobre-Downloader.git

# Verificar se o remote foi adicionado
git remote -v

# Renomear a branch para main (padrão do GitHub)
git branch -M main
```

**Substitua `SEU_USUARIO` pelo seu nome de usuário do GitHub!**

---

## 🚀 Passo 7: Fazer o Push (Enviar para o GitHub)

```bash
# Enviar o código para o GitHub
git push -u origin main
```

**Se pedir autenticação:**
- Use seu **username** do GitHub
- Use um **Personal Access Token** como senha (não a senha normal)

---

## 🔑 Como Criar Personal Access Token (Se Necessário)

1. Vá em: https://github.com/settings/tokens
2. Clique em "Generate new token" → "Generate new token (classic)"
3. Dê um nome: "Haumea Downloader"
4. Marque o scope: **repo** (todos os sub-itens)
5. Clique em "Generate token"
6. **COPIE O TOKEN** (você não verá ele novamente!)
7. Use esse token como senha quando o Git pedir

---

## 📊 Comandos Git Úteis para o Dia a Dia

### Ver o status dos arquivos
```bash
git status
```

### Adicionar mudanças
```bash
# Adicionar todos os arquivos modificados
git add .

# Adicionar arquivo específico
git add nome_do_arquivo.py
```

### Fazer commit
```bash
git commit -m "Descrição da mudança"
```

### Enviar para o GitHub
```bash
git push
```

### Ver histórico de commits
```bash
git log --oneline
git log --graph --oneline --all
```

### Desfazer mudanças (antes do commit)
```bash
git restore nome_do_arquivo.py
```

### Ver diferenças
```bash
git diff
```

---

## 📝 Exemplo Completo de Workflow

```bash
# 1. Fazer mudanças no código
# 2. Ver o que mudou
git status

# 3. Adicionar as mudanças
git add .

# 4. Fazer commit
git commit -m "✨ Adicionar nova funcionalidade X"

# 5. Enviar para o GitHub
git push
```

---

## 🎯 Comandos Para Este Projeto Agora

Execute estes comandos em ordem:

```bash
# 1. Navegar até a pasta
cd "C:\Users\Henri\Documents\00 - Outros\DriveDownloader"

# 2. Configurar Git (se ainda não fez)
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# 3. Inicializar repositório
git init

# 4. Adicionar arquivos
git add .

# 5. Fazer primeiro commit
git commit -m "🌟 Initial commit - Haumea DriveDePobre Downloader v2.0"

# 6. Criar repositório no GitHub (via navegador)
#    https://github.com/new

# 7. Adicionar remote (substituir SEU_USUARIO)
git remote add origin https://github.com/SEU_USUARIO/Haumea-DriveDePobre-Downloader.git

# 8. Renomear branch
git branch -M main

# 9. Push
git push -u origin main
```

---

## 🎨 Sugestão de README.md Melhorado para o GitHub

Seu README já está bom, mas você pode adicionar:

- **Screenshot** do aplicativo
- **Badge** de versão e licença
- **Demo GIF** mostrando o uso
- **Link** para issues e contribuições

---

## 📦 Arquivo .gitignore Já Criado

O projeto já tem um `.gitignore` que ignora:
- ✅ Arquivos Python temporários (`__pycache__/`)
- ✅ Logs (`logs/`)
- ✅ Downloads (`downloads/`)
- ✅ Arquivos do IDE

---

## 🆘 Problemas Comuns

### Erro: "fatal: not a git repository"
**Solução:** Execute `git init` primeiro

### Erro: "remote origin already exists"
**Solução:** Execute `git remote remove origin` e adicione novamente

### Erro de autenticação
**Solução:** Use Personal Access Token ao invés da senha

### Erro: "failed to push some refs"
**Solução:** Execute `git pull origin main --rebase` primeiro, depois `git push`

---

## 🎉 Pronto!

Após seguir estes passos, seu projeto estará no GitHub!

Acesse: `https://github.com/SEU_USUARIO/Haumea-DriveDePobre-Downloader`

---

## 📚 Recursos Adicionais

- **Git Docs:** https://git-scm.com/doc
- **GitHub Guides:** https://guides.github.com
- **Git Cheat Sheet:** https://education.github.com/git-cheat-sheet-education.pdf
