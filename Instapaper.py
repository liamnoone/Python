import requests


def Authenticate(user, password):
    r = requests.get("https://www.instapaper.com/api/authenticate",
                     auth=(user, password))
    return r.status_code


def AddUrl(user, password, url, title):
    if Authenticate(user, password) == 200:
        u = {"username": user, "password": password,
             "url": url, "title": title, "selection": ""}
        add = requests.post("https://www.instapaper.com/api/add", u)

        if add.status_code == 201:
            print("Link added successfully")
        elif add.status_code == 400:
            print(
                "Bad request or exceeded the rate limit. Probably missing a required parameter, such as url.")
        elif add.status_code == 500:
            print("The service encountered an error. Please try again later.")
        else:
            print("An unknown error occurred")
    else:
        print("Authentication failure")


if __name__ == "__main__":
    AddUrl(input("Username/Email: "), input("Password: "),
           input("Url to Add: "), input("Title for the link: "))
