set current_dir=%cd%
set desktop_dir=C:\Users\Marcus\Desktop

set app_name=TPCAE
set work_folder=%desktop_dir%\%app_name%_build
set code_folder="C:\Users\Marcus\Google Drive\TCC\TCC_software\TPCAE"
set db_folder=%code_folder%\db
set venv=deploy_venv
set venv_scripts=%venv%\Scripts
set logfile=deploy_time.txt
set s7z="C:\Program Files\7-Zip\7z.exe"

cd %app_name%
mkdir %work_folder%

call pyinstaller.exe -D -w --clean main.py -n %app_name% --distpath %work_folder% --workpath %work_folder%\build

cd %work_folder%
mkdir %app_name%\db
xcopy %db_folder% %app_name%\db /E

if exist %s7z% (call %s7z% a TPCAE -t"zip" TPCAE & call %s7z% a TPCAE.exe TPCAE -sfx)

cd %current_dir%