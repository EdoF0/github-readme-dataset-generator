import requests
import json
import base64

USE_TOKEN = False
TOKEN_FILE = "token.txt"

def getToken() -> str:
    with open(TOKEN_FILE) as f:
        return f.readline().strip(" \n")

def githubApiGet(url:str, useToken = USE_TOKEN) -> any:
    headers = {
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if useToken:
        if len(githubApiGet.token) <= 0:
            githubApiGet.token = getToken()
        headers["Authorization"] = "Bearer " + githubApiGet.token

    reqUrl = "https://api.github.com" + url
    # timeout for connect and read, respecting best practices (https://requests.readthedocs.io/en/stable/user/advanced/#timeouts)
    response = requests.get(reqUrl, headers = headers, timeout=(6.05, 9))
    if not response.ok:
        # check if authentication is successful
        # check for header 'X-RateLimit-Limit': '5000' (5000 for standard GitHub users)
        # can also look at 'X-RateLimit-Remaining' and 'X-RateLimit-Used' to check the usage
        # the rate limit is per-hour (see https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api?apiVersion=2022-11-28)
        # side note: anonymous rate limit is 60 requests per hour
        #print(response.headers)
        if response.status_code == 403 or response.status_code == 429:
            # see https://docs.github.com/en/rest/overview/rate-limits-for-the-rest-api?apiVersion=2022-11-28
            raise Exception("Rate limit exceeded while requesting " + reqUrl)
        elif response.status_code == 404 or response.status_code == 451:
            # if deleted or blocked due to legal reasons
            raise LookupError(reqUrl)
        else:
            raise Exception(f"Response status code {str(response.status_code)} for GET {reqUrl}")
    return json.loads(response.content)
# variable persistent across function calls, to avoid reading the token file for every request
# see https://stackoverflow.com/questions/279561/what-is-the-python-equivalent-of-static-variables-inside-a-function
githubApiGet.token = ""

def repoHasRelease(owner:str, name:str) -> bool:
    releases = githubApiGet(f"/repos/{owner}/{name}/releases")
    return len(releases) > 0

def repoReadme(owner:str, name:str) -> str:
    # f"/repos/{owner}/{name}/contents/README.md"
    readmeObj = githubApiGet(f"/repos/{owner}/{name}/readme")
    if readmeObj["encoding"] != "base64":
        raise Exception("cannot decode README with encoding " + readmeObj["encoding"])
    return base64.b64decode(readmeObj["content"]).decode()

def repoLanguage(owner:str, name:str) -> tuple[str, float]:
    # api documentation
    # https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repository-languages
    languages = githubApiGet(f"/repos/{owner}/{name}/languages")
    # find most used language and compute percentage
    totalBytesOfCode = 0
    maxLang = ""
    for language, bytesOfCode in languages.items():
        totalBytesOfCode += bytesOfCode
        if (maxLang == "" or bytesOfCode > languages[maxLang]):
            maxLang = language
    if (maxLang == ""):
        return "", 0
    else:
        return maxLang, languages[maxLang]/totalBytesOfCode

def repoStars(owner:str, name:str) -> int:
    details = githubApiGet(f"/repos/{owner}/{name}")
    return int(details["stargazers_count"])

tests = [
    ("rust-lang", "rust"),
    ("samuelcolvin", "FastUI"),
    ("LC044", "WeChatMsg"),
    ("facebookresearch", "seamless_communication")
]

if __name__ == "__main__":
    #print("token: " + getToken())
    for repo in tests:
        test_owner, test_repo = repo
        print(f"testing {test_owner}/{test_repo}")
        release = repoHasRelease(test_owner, test_repo)
        print("repo has release: " + str(release))
        language, percent = repoLanguage(test_owner, test_repo)
        print(f"repo first language: {language} ({percent*100}%)")
        readme = repoReadme(test_owner, test_repo)
        print("repo README first line: " + readme.split("\n", 1)[0])
        stars = repoStars(test_owner, test_repo)
        print("repo stars: " + str(stars))
        print("-")