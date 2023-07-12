import json
from instaloader import Instaloader, Profile
import requests

def sendData(data):
    # call api and populate db
    # url = 'https://www.test.com/posts'
    # # converted json not required for api call
    data=json.dumps(data)
    print(data)
    # x = requests.post(url, json = data)
    # print(x.text)

def updateInstaPosts(profileList):
    res={}
    # Get instance
    L = Instaloader()

    # Optionally, login or load session
    # L.login(USER, PASSWORD)        # (login)
    # L.interactive_login(USER)      # (ask password on terminal)
    # L.load_session_from_file(USER) # (load session created w/
                                #  `instaloader -l USERNAME`)
    for profileName in profileList:
        dataList = []
        profile = Profile.from_username(L.context, profileName)
        posts = profile.get_posts()
        for i in posts:
            data={
                'id':  i.mediaid,
                'likes': i.likes,
                'comments': i.comments
            }
            if i.video_view_count is not None:
                data['view_count'] = i.video_view_count
                data['url'] = i.video_url
                data['type'] = 'video'
            else:
                data['view_count'] = 0
                data['url'] = i.url
                data['type'] = 'image/post'
            dataList.append(data)
        res[profileName] = dataList
    sendData(res)
profileList = ["independent.calmmind", "bhosale_kirti"]
updateInstaPosts(profileList)