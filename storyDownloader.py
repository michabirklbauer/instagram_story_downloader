#!/usr/bin/env python3

import urllib.request as ur
import json
import sys

def load_stories(user_name, is_user_id = False):

	if is_user_id:
		url = "https://i.instagram.com/api/v1/users/"+str(user_name)+"/info/"
		user_info = ur.urlopen(url).read()
		user_name = json.loads(user_info)["user"]["username"]

	url = "https://storiesig.com/stories/" + str(user_name)
	page = ur.urlopen(url).read().decode("utf-8")
	lines = page.splitlines()
	data = ""
	for line in lines:
		if "__NEXT_DATA__" in line:
			data = line.replace("__NEXT_DATA__ = ", "").lstrip().rstrip()
	
	if data != "":
		jdata = json.loads(data)
		stories = jdata["props"]["pageProps"]["stories"]["items"]
		for story in stories:
			original_width = story["original_width"]
			original_height = story["original_height"]
			media_type = int(story["media_type"])
			for entry in story["image_versions2"]["candidates"]:
				if entry["width"] == original_width and entry["height"] == original_height:
					ur.urlretrieve(str(entry["url"]), str(entry["url"]).split("/")[-1].split("?")[0])
			max_height = 0
			max_counter = 0
			i = 0
			if media_type == 2:
				for entry in story["video_versions"]:
					if int(entry["height"]) >= max_height:
						max_height = int(entry["height"])
						max_counter = i
					i = i + 1
				ur.urlretrieve(str(story["video_versions"][max_counter]["url"]), str(story["video_versions"][max_counter]["url"]).split("/")[-1].split("?")[0])

if __name__ == '__main__':
	if len(sys.argv) == 1:
		user_name = input("Please enter a username. If you would like to use a user ID instead, please use the commandline options!\n")
		load_stories(user_name)
	elif len(sys.argv) == 2:
		user_name = sys.argv[1]
		load_stories(user_name)
	elif len(sys.argv) == 3:
		user_name = sys.argv[1]
		is_user_id = sys.argv[2]
		if is_user_id == "False":
			load_stories(user_name)
		elif is_user_id == "True":
			load_stories(user_name, is_user_id = True)
		else:
			print("Wrong Usage: is_user_id has to be either True or False!")
	else:
		print("Wrong Usage: Wrong number of arguments!\nUsage: storyDownloader.py <user_name/user_id> <is_user_id>")