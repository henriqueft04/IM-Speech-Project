wt --window 0 --title FUSION --suppressApplicationTitle -d . -p "Windows Powershell" cmd /k "cd .\FusionEngine\ && start.bat"

wt --window 0 --title CLIENT --suppressApplicationTitle -d . -p "Windows Powershell" cmd /k "cd .\IM\ && start.bat"

wt --window 0 --title RASA --suppressApplicationTitle -d . -p "Windows Powershell" cmd /k ".\venv\Scripts\activate && rasa run --enable-api -m .\rasaDemo\models\ --cors "*""

wt --window 0 --title WEBAPP --suppressApplicationTitle -d . -p "Windows Powershell" cmd /k ".\venv\Scripts\activate && cd .\WebAppAssistantV2 && python server.py"

wt --window 0 --title SERVER --suppressApplicationTitle -d . -p "Windows Powershell" cmd /k ".\venv\Scripts\activate && python .\Assistant\main.py"

openpage.bat