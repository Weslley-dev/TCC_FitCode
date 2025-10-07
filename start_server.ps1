Write-Host "Ativando ambiente virtual..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Ambiente virtual ativado!" -ForegroundColor Green
Write-Host "Iniciando servidor Django..." -ForegroundColor Yellow
Write-Host ""

python manage.py runserver

Read-Host "Pressione Enter para sair"
