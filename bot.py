# -*- coding: utf-8 -*-
import ast
from linepy import *
from commands import commands

client = LINE("email", "passwd")
#client = LINE("authtoken")

client.log("Authtoken: " + str(client.authToken))

tracer = OEPoll(client)
command = commands()

profile = client.getProfile()

def NOTIFIED_INVITE_INTO_GROUP(op):
	try:
		if profile.mid in op.param3:
			if command.autojoin == "all":
				client.acceptGroupInvitation(op.param1)
			else:
				if op.param2 in [command.staff + command.bot]:
					client.acceptGroupInvitation(op.param1)
				else:
					client.rejectGroupInvitation(op.param1)
	except Exception as e:
		print(e)

def RECEIVE_MESSAGE(op):
	try:
		msg = op.message

		sender = msg._from
		receiver = msg.to
		#in pm, reciever = sender
		if msg.toType == 0:
			receiver = sender

		if msg.contentType == 0:
			text = msg.text.rstrip()
			if text.lower() in ["responsename","rname"]:
				client.sendMessage(receiver, command.responsename)
			elif text.lower() in ["squadname","sname"]:
				client.sendMessage(receiver, command.squadname)
			elif text.lower() == "mid":
				print(sender)
				client.sendMessage(receiver, sender)
			elif text.lower() == "gid":
				client.sendMessage(receiver, receiver)
			name_present = 0
			if text[:len(command.responsename)] == command.responsename:
				text = text[len(command.responsename):]
				name_present = 1
			elif text[:len(command.squadname)] == command.squadname:
				text = text[len(command.squadname):]
				name_present = 1
			if name_present == 1:
				if text.lower() == "autojoin:all":
					command.autojoin = "all"
					client.sendMessage(reciever, "Autojoin set to all.")
				elif text.lower() == "autojoin:staff":
					command.autojoin = "staff"
					client.sendMessage(receiver, "Autojoin set to staff.")
				elif text.lower() == "show staff":
					if sender in command.staff:
						string = "STAFF:\n"
						for i in range(len(command.staff)):
							uid = command.staff[i]
							name = client.getContact(uid).displayName
							string += "\n%s. %s" % (i,name)
						client.sendMessage(receiver,string)
				elif text.lower() == "show admin":
					if sender in command.admin:
						string = "ADMIN:\n"
						for i in range(len(command.admin)):
							uid = command.admin[i]
							name = client.getContact(uid).displayName
							string += "\n%s. %s" % (i,name)
						client.sendMessage(receiver,string)
				elif text.lower() == "show owner":
					if sender in command.owner:
						string = "OWNER:\n"
						for i in range(len(command.owner)):
							uid = command.owner[i]
							name = client.getContact(uid).displayName
							string += "\n%s. %s" % (i,name)
						client.sendMessage(receiver,string)
				elif len(msg.contentMetadata) != 0:
					#someone's been tagged
					mentions = ast.literal_eval(msg.contentMetadata["MENTION"])
					uids = [m["M"] for m in mentions["MENTIONEES"]]
					if text[:7].lower() == "staff @":
						for uid in uids:
							name = client.getContact(uid).displayName
							result = command.giveStaff(sender,uid,name)
							client.sendMessage(receiver, result)
					elif text[:7].lower() == "admin @":
						for uid in uids:
							name = client.getContact(uid).displayName
							result = command.giveAdmin(sender,uid,name)
							client.sendMessage(receiver, result)
					elif text[:7].lower() == "owner @":
						for uid in uids:
							name = client.getContact(uid).displayName
							result = command.giveOwner(sender,uid,name)
							client.sendMessage(receiver, result)
					elif text[:5].lower() == "bot @":
						for uid in uids:
							name = client.getContact(uid).displayName
							result = command.giveBot(sender,uid,name)
							client.sendMessage(receiver, result)
					elif text[:7].lower() == "expel @":
						for uid in uids:
							name = client.getContact(uid).displayName
							result = command.expel(sender,uid,name)
							client.sendMessage(receiver, result)
					elif text[:5].lower() == "ban @":
						for uid in uids:
							name = client.getContact(uid).displayName
							result = command.ban(sender,uid,name)
							client.sendMessage(receiver, result)
					elif text[:7].lower() == "unban @":
						for uid in uids:
							name = client.getContact(uid).displayName
							result = command.unban(sender,uid,name)
							client.sendMessage(receiver, result)


	except Exception as e:
		print(e)

tracer.addOpInterruptWithDict({
	OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE,
	OpType.NOTIFIED_INVITE_INTO_GROUP: NOTIFIED_INVITE_INTO_GROUP})

while True:
	tracer.trace()
