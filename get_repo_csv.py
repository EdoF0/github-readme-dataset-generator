import csv

# csv input file
# it must have the first two columns being valid owner and repository
# example: facebook,react -> https://github.com/facebook/react
REPO_CSV_PATH = "repos-src.csv"
# if repositories csv only contains repositories satisfying defined requirements (see filtering in dataset generator)
FILTERED = False

def create_getRepo(path = REPO_CSV_PATH, filtered = FILTERED):
    f = open(path, 'r', newline='', encoding="utf-8")
    reader = csv.reader(f, escapechar='\\')
    next(reader, None)  # skip the header

    def getRepo() -> tuple[str, str]:
        row = next(reader)
        return row[0], row[1]

    def close_src():
        f.close()

    return getRepo, close_src

if __name__ == "__main__":
    print("Repository list form csv test")
    getRepo, close_src = create_getRepo()
    print(getRepo())
    print(getRepo())
    print(getRepo())
    print("now reading all ...")
    try:
        while True:
            getRepo()
    except StopIteration as e:
        print("finish")
    close_src()
