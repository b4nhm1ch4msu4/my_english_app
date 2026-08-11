from app.logger import setup_logging
from app.dictionary import lookup

def main():
    setup_logging()
    obj = lookup("asdba")
    if obj:
        print(obj.example)

if __name__ == "__main__":
    main()
