from app.dictionary import lookup

def main():
    obj = lookup("asdba")
    if obj:
        print(obj.example)

if __name__ == "__main__":
    main()
