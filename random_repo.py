import requests
import json

def randomRepo() -> tuple[str, str]:
    response = requests.get("https://gitrandom.digitalbunker.dev/fetch?topic=Any&language=")
    if not response.ok:
        raise Exception("GET request fail for random repo endpoint")
    repoDetails = json.loads(response.content)
    return repoDetails["owner"]["login"], repoDetails["name"]

if __name__ == "__main__":
    print("Random repo test")
    for _ in range(6):
        print(randomRepo())