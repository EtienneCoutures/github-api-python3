import requests
import json

class Client:

        def __init__(self, github_token):
            self.session =  requests.Session() 
            self.session.headers['Authorization'] = "token " + github_token
            res = self.session.get("https://api.github.com/user")
            if (res.status_code != 200):
                raise Exception("invalid credentials")
            self.user = res.json()['login']              

        def list_followers(self):
            res = self.session.get("https://api.github.com/users/" + self.user + "/followers")
            return json.dumps(res.json())

        def list_stars(self):
            res = self.session.get("https://api.github.com/users/" + self.user + "/starred")
            return json.dumps(res.json())

        def list_repo(self):
            res = self.session.get("https://api.github.com/user/repos")
            print(res.json()[4]['id'])
            print(res.json()[4]['name'])
            return json.dumps(res.json())

        def star_repo(self, repo_id):
            res = self.session.get("https://api.github.com/repositories/" + str(repo_id))
            if (res.status_code != 200):
                raise Exception("an error has occurred")
            owner = res.json()
            url = "https://api.github.com/user/starred/" + str(owner["owner"]["login"]) + "/" + owner["name"]
            star_rep = self.session.put(url)
            if (star_rep.status_code != 204):
                raise Exception("an error as occured")    
            return json.dumps({'status': 'ok',})

        def follow_user(self, user_id):
            res = self.session.get("https://api.github.com/user/" + str(user_id))
            if (res.status_code != 200):
                raise Exception("an error has occurred")
            rep = res.json()["login"]
            act = self.session.put("https://api.github.com/user/following/" + str(rep))
            if (act.status_code != 204):
                raise Exception("an error as occured")    
            return json.dumps({'status': 'ok',})


        def unfollow_user(self, user_id):
            res = self.session.get("https://api.github.com/user/" + str(user_id))
            if (res.status_code != 200):
                raise Exception("an error has occurred")
            rep = res.json()["login"]
            act = self.session.delete("https://api.github.com/user/following/" + str(rep))
            if (act.status_code != 204):
                raise Exception("an error as occured")    
            return json.dumps({'status': 'ok',})


        def create_repo(self, name):
            rep = self.session.post("https://api.github.com/user/repos", data=json.dumps({'name': name}))
            if (rep.status_code != 201):
               raise Exception("unknown error")
            return json.dumps(rep.json())

        def delete_repo(self, id):
            rep = self.session.get("https://api.github.com/repositories/" + str(id))
            if (rep.status_code != 200):
                raise Exception("an error as occured")
            res = rep.json()
            owner = res["owner"]["login"]
            name = res["name"]
            rep = self.session.delete("https://api.github.com/repos/" + owner + "/" + name)
            if (rep.status_code != 204):
                raise Exception("an error as occured")
            return json.dumps({"status": "ok"}) 

