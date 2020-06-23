import spider




if __name__ == "__main__":
    rawfile = open("raw.txt", 'r', encoding='UTF-8')

    rawfile.seek(27525)
    while(1):
        print(rawfile.readline())

    pass

