from random_repo import randomRepo
from repo_data import repoHasRelease, repoLanguage, repoReadme, repoStars
from write_dataset import create_dataset, DATASET_NAME, DATASET_NAME_TEST

TEST = True

DATASET = DATASET_NAME
ROWS = 10000

DATASET_TEST = DATASET_NAME_TEST
ROWS_TEST = 5

if __name__ == "__main__":

    dataset = DATASET
    rows = ROWS
    print_end = '\r' # to overwrite lines on console
    if (TEST):
        dataset = DATASET_TEST
        rows = ROWS_TEST
        print_end = '\n'

    write, close = create_dataset(dataset)
    i = 0
    while i < rows:
        owner, repo = randomRepo()
        language, percent = repoLanguage(owner, repo)
        stars = repoStars(owner, repo)
        language = "a"
        percent = 0.90
        stars = 1000
        if (percent > 0.85 and stars > 300):
            write(
                owner=owner,
                repo=repo,
                release=repoHasRelease(owner, repo),
                language=language,
                stars=stars,
                readme=repoReadme(owner, repo)
            )
            i += 1
            print(f"line {i} of {rows} -- written {owner}/{repo} ({stars} stars, lang {language} {percent*100}%)                                                    ", end=print_end)
        else:
            print(f"line {i} of {rows} -- skipped {owner}/{repo} ({stars} stars, lang {language} {percent*100}%)                                                    ", end=print_end)
    print(f"finished writing {rows} rows                                                                                                                    ")
    close()
