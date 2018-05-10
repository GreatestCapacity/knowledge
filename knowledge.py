import text_mode.main
import web_mode.manage
import desktop_mode.main
import sys

if __name__ == '__main__':
    if '--web_mode' in sys.argv:
        if '--localhost' in sys.argv:
            web_mode.manage.main(['knowledge.py', 'runserver'])
        else:
            web_mode.manage.main(['knowledge.py', 'runserver', '0.0.0.0:8000'])
    elif '--desktop_mode' in sys.argv:
        desktop_mode.main.main()
    else:
        text_mode.main.main()
