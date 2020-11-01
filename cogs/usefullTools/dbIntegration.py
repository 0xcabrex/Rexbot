import pymongo
from pymongo import MongoClient
import os

mongodbclient_token = os.getenv("DATABASE_CLIENT_URL")

if mongodbclient_token is None:
	try:
		with open('./mongodbclient.0', 'r', encoding='utf-8') as client_url:
			print("Using MongoDB cluster url provided in file")
			cluster = MongoClient(client_url.read())
	except FileHandleError:
		print("File not found [mongodbclient.0]")
else:
	print("Using MongoDB cluster url provided in environment variable..")
	cluster = MongoClient(mongodbclient_token)


db = cluster["rexbotdb"]
collection = db["warnings"]
warnthresh_collection = db["warnthresh"]

print("Database connection has been established\n")

def insert_warns(guild_id, member_id, mod_id, warning):

	initial_warn = None
	initial_warn = collection.find_one({"member_id": str(member_id), "guild_id" : str(guild_id)})

	if initial_warn is None:
		results = collection.insert_one({"guild_id": str(guild_id), "member_id": str(member_id), "mod_id": str(mod_id), "warning": warning})
	else:

		get_warns = collection.find_one({"member_id": str(member_id), "guild_id": str(guild_id)})
		warns = get_warns["warning"]
		modd_id = get_warns["mod_id"]
		results = collection.update_one({"member_id": str(member_id)}, {"$set": {"warning": f"{warns}\n{warning}"}})
		results1 = collection.update_one({"member_id": str(member_id)}, {"$set":{"mod_id": f"{modd_id}\n{mod_id}"}})



def fetch_warns(guild_id, member_id):
	results = collection.find_one({"member_id": str(member_id), "guild_id": str(guild_id)})
	return results

def delete_warns(guild_id, member_id):

	results = collection.delete_one({"member_id": str(member_id), "guild_id": str(guild_id)})


def fetch_warn_thresh(guild_id):

	results = warnthresh_collection.find_one({"guild_id": guild_id})
	return results

def insert_warn_thresh(guild_id, threshold):

	threshold_check = None
	threshold_check = warnthresh_collection.find_one({"guild_id": guild_id})
	
	if threshold_check is None:
		results = warnthresh_collection.insert_one({"guild_id": guild_id, "threshold": int(threshold)})
	else:
		results = warnthresh_collection.update_one({"guild_id": guild_id}, {"$set": {"threshold": int(threshold)}})

def del_warn_thresh(guild_id):

	results = warnthresh_collection.delete_one({"guild_id": guild_id})
