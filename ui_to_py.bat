call C:\DevelopmentTools\Miniconda3\miniconda3\Scripts\activate.bat C:\DevelopmentTools\Miniconda3\miniconda3
pyrcc5 res/app.qrc -o res/app_rc.py
python -m PyQt5.uic.pyuic ui/main_window.ui -o ui/main_window.py --import-from=res
python -m PyQt5.uic.pyuic ui/search_widget.ui -o ui/search_widget.py --import-from=res