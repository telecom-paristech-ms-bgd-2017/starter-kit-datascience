import requests
from bs4 import BeautifulSoup as bs

with open("C:/Users/rapto/Documents/Télécom ParisTech/Github Token.txt", mode="r") as f:
    token = f.read() 
header = {"username": token}

req = requests.get("https://gist.github.com/paulmillr/2657075/")
soup = bs(req.text, "html.parser")
selected = soup.select("tr > td:nth-of-type(1) > a")

users = []
for piece in selected:
    username = piece.text
    user = {"username": username}
    r = requests.get("https://api.github.com/users/" + username + "/repos",
                     headers=header)
    js = r.json()
    stargazers_count = 0
    for repo in js:
       stargazers_count += repo["stargazers_count"]
       
    user["mean_stargazers"] = stargazers_count / len(js)
    users.append(user)
    
print(users)