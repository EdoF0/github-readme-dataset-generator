import requests
import json
import time

def isRandomApiRandomError(response):
    return (
        response.status_code == 400 and
        (
            response.content.decode() == '{"error":true,"reason":"Value required for key \'items\'."}' or
            response.content.decode() == '{"reason":"Value required for key \'items\'.","error":true}'
        )
    )


def randomRepo() -> tuple[str, str]:
    response = requests.get("https://gitrandom.digitalbunker.dev/fetch?topic=Any&language=")
    if not response.ok:
        # sometimes the api randomly responds with an error, just ignore that
        if isRandomApiRandomError(response):
            #print("random api error, waiting 30 seconds")
            time.sleep(30)
            return randomRepo()
        raise Exception(
            "GET request fail for random repo endpoint\n" +
            "status code: " + str(response.status_code) + "\n" +
            "payload: " + response.content.decode()
        )
    repoDetails = json.loads(response.content)
    return repoDetails["owner"]["login"], repoDetails["name"]

if __name__ == "__main__":
    print("Random repo test")
    for i in range(6):
        print(str(i+1) + " ", randomRepo())