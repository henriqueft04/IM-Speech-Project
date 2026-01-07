wt --window 0 --title FUSION --suppressApplicationTitle -d . -p "Windows Powershell" cmd /k "cd .\FusionEngine\ && start.bat"

wt --window 0 --title CLIENT --suppressApplicationTitle -d . -p "Windows Powershell" cmd /k "cd .\IM\ && start.bat"

wt --window 0 --title SERVER --suppressApplicationTitle -d . -p "Windows Powershell" cmd /k "cd .\Assistant\ && python main.py"