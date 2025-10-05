# VN-Law-Mini Quick Start Script
# Run this after setting up Supabase database

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  VN-LAW-MINI - QUICK START" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

$PROJECT_ROOT = "D:\law-advisor\VN-Law-Advisor\vn-law-mini"

# Check if Supabase is ready
Write-Host "[1/7] Checking Supabase setup..." -ForegroundColor Yellow
Write-Host "Have you run the SQL schema in Supabase? (Y/N): " -ForegroundColor Green -NoNewline
$response = Read-Host
if ($response -ne "Y" -and $response -ne "y") {
    Write-Host ""
    Write-Host "⚠️  Please setup Supabase first:" -ForegroundColor Red
    Write-Host "   1. Go to: https://app.supabase.io" -ForegroundColor White
    Write-Host "   2. Open your project: icwshxmcashujylkdlzj" -ForegroundColor White
    Write-Host "   3. Go to SQL Editor" -ForegroundColor White
    Write-Host "   4. Run the SQL from: infrastructure/supabase-schema.sql" -ForegroundColor White
    Write-Host ""
    exit
}

Write-Host "✅ Great! Continuing..." -ForegroundColor Green
Write-Host ""

# Law Service
Write-Host "[2/7] Starting Law Service..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd $PROJECT_ROOT\backend\law-service; Write-Host 'Law Service starting...' -ForegroundColor Cyan; node src/index.js"
Start-Sleep -Seconds 3

# Test Law Service
Write-Host "[3/7] Testing Law Service..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/health" -TimeoutSec 5
    Write-Host "✅ Law Service is running!" -ForegroundColor Green
    Write-Host "   URL: http://localhost:5000" -ForegroundColor White
} catch {
    Write-Host "⚠️  Law Service may not be ready yet. Check the terminal." -ForegroundColor Red
}
Write-Host ""

# RAG Service
Write-Host "[4/7] Do you want to start RAG Service? (Y/N): " -ForegroundColor Green -NoNewline
$response = Read-Host
if ($response -eq "Y" -or $response -eq "y") {
    Write-Host "Installing RAG dependencies (this may take 5-10 minutes)..." -ForegroundColor Yellow
    cd "$PROJECT_ROOT\backend\rag-service"
    pip install -r requirements.txt
    
    Write-Host ""
    Write-Host "[5/7] Have you created embeddings (run vectorize.py)? (Y/N): " -ForegroundColor Green -NoNewline
    $response = Read-Host
    if ($response -ne "Y" -and $response -ne "y") {
        Write-Host "Creating embeddings..." -ForegroundColor Yellow
        python vectorize.py
    }
    
    Write-Host ""
    Write-Host "[6/7] Starting RAG Service..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd $PROJECT_ROOT\backend\rag-service; Write-Host 'RAG Service starting...' -ForegroundColor Cyan; python app.py"
    Start-Sleep -Seconds 10
    
    Write-Host "✅ RAG Service should be running on http://localhost:5001" -ForegroundColor Green
}
Write-Host ""

# Frontend
Write-Host "[7/7] Do you want to start Frontend? (Y/N): " -ForegroundColor Green -NoNewline
$response = Read-Host
if ($response -eq "Y" -or $response -eq "y") {
    Write-Host "Installing Frontend dependencies..." -ForegroundColor Yellow
    cd "$PROJECT_ROOT\web"
    
    # Check if node_modules exists
    if (-Not (Test-Path "node_modules")) {
        npm install
    }
    
    Write-Host ""
    Write-Host "Starting Next.js dev server..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd $PROJECT_ROOT\web; Write-Host 'Frontend starting...' -ForegroundColor Cyan; npm run dev"
    Start-Sleep -Seconds 5
    
    Write-Host "✅ Frontend should be running on http://localhost:3000" -ForegroundColor Green
}

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  🎉 VN-LAW-MINI IS RUNNING!" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access points:" -ForegroundColor White
Write-Host "  🌐 Frontend:    http://localhost:3000" -ForegroundColor Cyan
Write-Host "  🔌 Law API:     http://localhost:5000" -ForegroundColor Cyan
Write-Host "  🤖 RAG API:     http://localhost:5001" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit this script..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
