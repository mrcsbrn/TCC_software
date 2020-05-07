SET scripts_path=%~dp0
set repo_path=%scripts_path%..
SET venv_name=sindri_venv
set venv_dir=%repo_path%\%venv_name%
set activate_venv="%venv_dir%\Scripts\activate.bat"
set deactivate_venv="%venv_dir%\Scripts\deactivate.bat"
set main_py_file="%repo_path%\Sindri\main.py"
set build_folder=%repo_path%\build
set dist_folder=%repo_path%\dist
set shortcut_name=Sindri.bat