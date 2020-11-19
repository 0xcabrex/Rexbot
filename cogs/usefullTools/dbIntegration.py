import pymongo
from pymongo import MongoClient
import os

mongodbclient_token = os.getenv("DATABASE_CLIENT_URL")

if mongodbclient_token is None:
	try:
		with open('./mongodbclient.0', 'r', encoding='utf-8') as client_url:
			print("Using MongoDB cluster url provided in file")
			cluster = MongoClient(client_url.read())
	except FileNotFoundError:
		print("File not found [mongodbclient.0]")
		print("Neither environment variable nor client file exist")
		print("Abort")
		exit()
else:
	print("Using MongoDB cluster url provided in environment variable..")
	cluster = MongoClient(mongodbclient_token)


db = cluster["rexbotdb"]
collection = db["warnings"]
warnthresh_collection = db["warnthresh"]
prefix_collection = db["prefixes"]

print("Database connection has been established\n")

# ----------------------------------------------------------    Warnings     --------------------------------------------------------------

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

	results = None
	results = collection.find_one({"member_id": str(member_id), "guild_id": str(guild_id)})
	return results

def delete_warns(guild_id, member_id):

	results = collection.delete_one({"member_id": str(member_id), "guild_id": str(guild_id)})


# ----------------------------------------------------------     Warn threshold     -------------------------------------------------------

def fetch_warn_thresh(guild_id):

	results = None
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


# -----------------------------------------------------     Prefixes     ------------------------------------------------------------------

def fetch_prefix(guild_id):

	results = None
	results = prefix_collection.find_one({"guild_id": guild_id})
	return results


def insert_prefix(guild_id, prefix):

	prefix_check = None
	prefix_check = prefix_collection.find_one({"guild_id": guild_id})

	if prefix_check is None:
		results = prefix_collection.insert_one({"guild_id": guild_id, "prefix": str(prefix)})
	else:
		results = prefix_collection.update_one({"guild_id": guild_id}, {"$set": {"prefix": str(prefix)}})


def del_prefix(guild_id):

	results = prefix_collection.delete_one({"guild_id": guild_id})


# -----------------------------------------------     shell session code     -----------------------------------------------

def help(arg = None):
	if arg is None or arg == '':
		print("Help command:\n")
		print("fetch [args]:")
		print("  warns [guild_id] [member_id]:\t\tGets the warnings of the user with provided guild_id and member_id")
		print("  prefix [guild_id]:\t\t\tGets the prefix of the given guild_id\n")
		
		print("del/delete [args]:")
		print("  warns [guild_id] [member_id]:\t\tDeletes the warnings of that member_id and guild_id")
		print("  prefix [guild_id]:\t\t\tDeletes the prefix of that server")
		
		print("add [args]")
		print("  warns [guild_id] [member_id] [mod_id] [warning]:\tAdds a warning")
		print("  prefix [guild_id] [prefix]:\t\t\t\tAdds the prefix")

		print("\nHelp:\tShows this help dialogue\n")

	elif arg == 'fetch':
		print("Help command for fetch\n")
		print("fetch [args]")
		print("  warns [guild_id] [member_id]:\t\tGets the warnings of the user with provided guild_id and member_id")
		print("  prefix [guild_id]:\t\t\tGets the prefix of the given guild_id\n")

	elif arg == 'add':
		print("Help command for add\n")
		print("add [args]")
		print("  warns [guild_id] [member_id] [mod_id] [warning]:\tAdds a warning")
		print("  prefix [guild_id] [prefix]:\t\t\t\tAdds the prefix")

	elif arg == 'del' or 'delete':
		print("Help command for del/delete\n")
		print("del/delete [args]")
		print("  warns [guild_id] [member_id]:\t\tDeletes the warnings of that member_id and guild_id")
		print("  prefix [guild_id]:\t\t\tDeletes the prefix of that guild_id\n")


	else:
		print(f"No help for {arg}")



if __name__ == '__main__':

	print("Shell created")

	while True:
		try:
			argument = input("~$ ")
		except KeyboardInterrupt:
			print("\nbye")
			exit()

		broken_argument = argument.split(' ')

		if broken_argument[0].lower() == 'fetch':

			if len(broken_argument) == 1 or broken_argument[1] == '':
				print("What to fetch?")
			
			elif broken_argument[1].lower() == 'prefix':
				if len(broken_argument) == 3:
					if broken_argument[2].isnumeric():
						result = fetch_prefix(int(broken_argument[2]))
						if result is not None:
							print(result['prefix'])
						else:
							print("no prefix found")
					else:
						print("Only integers accepted for guild_id")
				else:
					print("1 argument missing or is in excess")

			elif broken_argument[1].lower() == 'warns' or broken_argument[1].lower() == 'warn':
				if len(broken_argument) == 4:
					result = fetch_warns(broken_argument[2], broken_argument[3])
					if result is not None:
						warns = result['warning'].split('\n')
						mod_id = result['mod_id'].split('\n')
						member_id = result['member_id']
						guild_id = result['guild_id']

						print(f"\nGuild id: {guild_id}\nMember id: {member_id}\n\n")
						for i in range(len(warns)):
							print(f"Mod id: {mod_id[i]}\nWarning: {warns[i]}\n")
					else:
						print("no result found for that guild id and user id respectively")
				else:
					print("1 or 2 arguments missing or are in excess")
			else:
				print(f"{broken_argument[1]} does not exist")


		elif broken_argument[0].lower() == 'delete' or broken_argument[0].lower() == 'del':
			
			if len(broken_argument) == 1 or broken_argument[1] == '':
				print("What to delete?")

			elif broken_argument[1].lower() == 'prefix':
				if broken_argument[1].isnumeric():
					result = del_prefix(int(broken_argument[2]))
					print("done")
				else:
					print("only integers allowed")

			elif broken_argument[1].lower() == 'warns' or broken_argument[1].lower() == 'warn':
				if len(broken_argument) == 4:
					delete_warns(broken_argument[2], broken_argument[3])
					print("done")
				else:
					print("1 or 2 arguments missing or is in excess")

			else:
				print(f"{broken_argument[1]} does not exist")


		elif broken_argument[0].lower() == 'add':

			if len(broken_argument) == 1 or broken_argument[1] == '':
				print("What to add?")

			elif broken_argument[1].lower() == 'prefix':
				if len(broken_argument) == 4:
					if broken_argument[2].isnumeric():
						insert_prefix(int(broken_argument[2]), broken_argument[3])
						print("Done")
					else:
						print("Only integers allowed for guild_id")
				else:
					print("provide a preifx")

			elif broken_argument[1].lower() == 'warn' or broken_argument[1].lower() == 'warns':
				if len(broken_argument) >= 6:
					new_list = []
					for i in range(5, len(broken_argument), 1):
						new_list.append(broken_argument[i])
					result = insert_warns(broken_argument[2], broken_argument[3], broken_argument[4], f"{' '.join(new_list)}")
					print("Done")
				else:
					print(f"{len(broken_argument) - 4} argument(s) missing")

		elif broken_argument[0].lower() == 'exit' or broken_argument[0].lower() == 'quit' or broken_argument[0].lower() == 'q':
			print("bye")
			exit()

		elif broken_argument[0].lower() == 'clear' or broken_argument[0].lower() == 'cls':
			if os.name == 'posix':
				_ = os.system('clear')
			else:	
				_ = os.system('cls')

		elif broken_argument[0].lower() == 'help':
			if len(broken_argument) != 1:
				help(broken_argument[1].lower())
			else:
				help()

		elif broken_argument[0] == '':
			pass
		else:
			print("command not found")
	