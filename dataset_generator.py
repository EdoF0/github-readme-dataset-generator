from os.path import isfile
from random_repo import randomRepo
from repo_data import repoHasRelease, repoLanguage, repoReadme, repoStars
from write_dataset import create_dataset, count_lines, DATASET_NAME, DATASET_NAME_TEST

# settings

TEST = True

DATASET = DATASET_NAME
ROWS = 10000
APPEND = True

DATASET_TEST = DATASET_NAME_TEST
ROWS_TEST = 5
APPEND_TEST = True

if __name__ == "__main__":

    dataset = DATASET
    rows = ROWS
    append = APPEND
    print_end = '\r' # to overwrite lines on console
    if (TEST):
        dataset = DATASET_TEST
        rows = ROWS_TEST
        append = APPEND_TEST
        print_end = '\n'

    print("writing to " + dataset)
    print("target csv rows: " + str(rows))

    i = 0  # counts writes to dataset
    i0 = 0 # counts requests and not writes
    exists = isfile(dataset)
    if append:
        if exists:
            written_rows = count_lines(dataset)
            written_rows -= 1 # do not count header
            i = written_rows
            print("append mode on, " + str(written_rows) + " already in file (header excluded)")
        else:
            print("append mode on, creating new dataset " + dataset)
    else:
        if exists:
            print("warning! overwriting dataset " + dataset)
        else:
            print("creating new dataset, file: " + dataset)

    write, close = create_dataset(dataset, append=append)
    while i < rows:
        owner, repo = randomRepo()
        language, percent = repoLanguage(owner, repo)
        stars = repoStars(owner, repo)
        i0 += 1
        if (percent > 0.80 and stars > 200):
            write(
                owner=owner,
                repo=repo,
                release=repoHasRelease(owner, repo),
                language=language,
                stars=stars,
                readme=repoReadme(owner, repo)
            )
            i += 1
            print(f"request {i0} - line {i} of {rows} -- written {owner}/{repo} ({stars} stars, lang {language} {percent*100}%)               ", end=print_end)
        else:
            print(f"request {i0} - line {i} of {rows} -- skipped {owner}/{repo} ({stars} stars, lang {language} {percent*100}%)               ", end=print_end)
    print(f"finished writing {rows} rows                                                                               ")
    close()
