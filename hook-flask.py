from PyInstaller.utils.hooks import collect_data_files

# Указываем, что нужно включить папку templates
datas = collect_data_files('templates')