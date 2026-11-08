git clone https://github.com/som1one/License.git
cd License
```

### Option 2: SSH (если настроен SSH ключ)

```bash
git clone git@github.com:som1one/License.git
cd License
```

### Option 3: Использовать GitHub CLI (если установлен)

```bash
# Login first
gh auth login

# Clone repository
gh repo clone som1one/License
cd License
```

### Option 4: Использовать токен доступа (personal access token)

```bash
# 1. Create personal access token on GitHub:
# Settings > Developer settings > Personal access tokens > Tokens (classic)
# Generate new token (classic)
# Select scopes: repo, gist, etc.

# 2. Clone with token
git clone https://YOUR_USERNAME:YOUR_TOKEN@github.com/som1one/License.git
cd License
```

### Option 5: Использовать SSH с персональным доступом

1. **Настроить SSH ключ:**
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Follow prompts
```

2. **Получить публичный ключ:**
```bash
cat ~/.ssh/id_ed25519.pub
```

3. **Добавить ключ на GitHub:**
   - GitHub.com > Settings > SSH and GPG keys > New SSH key
   - Добавить ключ

4. **Клонировать:**
```bash
git clone git@github.com:som1one/License.git
cd License
```

### Recommended: Store token securely (GitHub CLI)

```bash
# Install GitHub CLI
# Windows: winget install GitHub.cli
# macOS: brew install gh
# Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.sh

# Login (once)
gh auth login

# Clone
gh repo clone som1one/License
cd License
```

---

## Quick Reference

| Method | Speed | Security | Setup Required |
|--------|-------|----------|----------------|
| HTTPS + Token | ⚡ Fast | ✅ High | Token in URL |
| SSH | 🚀 Fastest | 🔒 Very High | SSH key |
| GitHub CLI | 🌟 Best | 🔒 Very High | CLI + Login |
| HTTPS + Password | 🐢 Slow | ⚠️ Medium | Password only |

---

## Error Solving

### "Permission denied (publickey)"
```bash
# Solution: Use SSH key or token
git clone git@github.com:som1one/License.git
```

### "Authentication failed"
```bash
# Solution: Regenerate token on GitHub
# Settings > Developer settings > Personal access tokens
# Create new token and use it in URL
```

### "Repository not found"
```bash
# Solution: Verify repository permission
# Ensure you have access to the private repository
```

---

## Useful Git Commands

```bash
# Check remote origin
git remote -v

# Add remote if needed
git remote add origin https://github.com/som11one/License.git

# Pull from remote (with token)
git pull https://YOUR_TOKEN@github.com/som1one/License.git main

# Fetch changes
git fetch origin

# View status
git status

# Switch branch
git checkout -b new-branch
```

---

Вам нужно перейти на страницу репозитория в GitHub и скопировать URL в формате HTTPS или SSH, затем запустить команды выше.
