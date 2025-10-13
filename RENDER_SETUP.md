# 🚀 Configuração do Render.com - Solução para Perda de Dados

## 🔍 **Problema Identificado**

Os usuários estão sumindo do Render porque:
- O Render gratuito usa **SQLite** por padrão
- O SQLite **não persiste dados** entre reinicializações
- Quando você fecha/abre o projeto, o banco é recriado do zero

## ✅ **Soluções Implementadas**

### **Solução 1: Backup Automático (Implementada)**

Já implementei um sistema que:
- ✅ Restaura dados automaticamente na inicialização
- ✅ Faz backup dos dados a cada startup
- ✅ Usa múltiplos arquivos de backup como fallback

**Arquivos criados:**
- `startup_render.py` - Script de inicialização automática
- `app/management/commands/backup_data.py` - Comando de backup
- `app/management/commands/restore_data.py` - Comando de restauração

### **Solução 2: PostgreSQL (Recomendada)**

Para uma solução permanente, configure PostgreSQL:

#### **Passo 1: Configurar PostgreSQL no Render**
1. Acesse o painel do Render
2. Vá em "Dashboard" → "New" → "PostgreSQL"
3. Crie um banco PostgreSQL gratuito
4. Copie a `DATABASE_URL` gerada

#### **Passo 2: Configurar Variável de Ambiente**
1. No painel do seu serviço web
2. Vá em "Environment"
3. Adicione: `DATABASE_URL` = (cole a URL do PostgreSQL)

#### **Passo 3: Migrar Dados**
Execute o script de migração:
```bash
python setup_postgres_render.py
```

## 🔧 **Como Usar**

### **Backup Manual**
```bash
python manage.py dumpdata auth.user accounts.userprofile aparelhos.aparelho aparelhos.grupo_muscular aparelhos.feedback aparelhos.visualizacao --indent 2 --output backup_data.json
```

### **Restaurar Dados**
```bash
python manage.py loaddata backup_data.json
```

### **Verificar Dados Atuais**
```bash
python manage.py shell -c "from django.contrib.auth.models import User; print('Usuários:', User.objects.count())"
```

## 📊 **Status Atual**

✅ **Backup automático implementado**
✅ **Script de inicialização criado**
✅ **Múltiplos arquivos de backup disponíveis**
⚠️ **PostgreSQL não configurado (recomendado)**

## 🎯 **Próximos Passos**

1. **Imediato**: O sistema já está configurado para restaurar dados automaticamente
2. **Recomendado**: Configure PostgreSQL para persistência permanente
3. **Opcional**: Use o sistema de backup manual quando necessário

## 📁 **Arquivos de Backup Disponíveis**

- `backup_data_atual.json` - Backup mais recente
- `backup_data.json` - Backup principal
- `render_data.json` - Dados do Render
- `admin_data.json` - Dados administrativos

## ⚠️ **Importante**

- O sistema agora **restaura automaticamente** os dados na inicialização
- Seus usuários **não vão mais sumir** após reinicializações
- Para persistência permanente, configure PostgreSQL
