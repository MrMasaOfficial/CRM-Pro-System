import sys
from db import Database
from ui import CRMApplication

def main():
    app = CRMApplication(sys.argv)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
