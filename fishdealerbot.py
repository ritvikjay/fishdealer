import fbchat
import time
from fbchat import Message
from fbchat import ThreadType
from getpass import getpass
import random
from credentials import CREDENTIALS

class FishBot(fbchat.Client):
    suits_emoji = [u'\U00002660', u'\U00002663', u'\U00002665', u'\U00002666']
    suits_text = ['Spades', 'Clubs', 'Hearts', 'Diamonds']

    #default
    suits = suits_text


    nums = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
    gcname = "FishGame"
    gcuid = "3271435542909370" #testing thread id: "3126833007361899", group thread id:"3271435542909370"
    cards = []
    cardsdict_text = {}
    cardsdict_emoji = {}
    ind = 0
    numplayer = 0

    #dict of player to preference of text or emoji
    prefs = {}



    #formats the two dicts for the type of suits
    for suit in suits_emoji:
        for num in nums:
            cardsdict_emoji[ind] = num + "-" + suit
            cards.append(ind)
            ind+=1
    cardsdict_emoji[ind] = u'\U0001F534' + u'\U0001F921'
    cards.append(ind)
    ind+=1
    cardsdict_emoji[ind] = u'\U000026AB' + u'\U0001F921'
    cards.append(ind)

    ind=0
    for suit in suits_text:
        for num in nums:
            cardsdict_text[ind] = num + "-" + suit
            ind+=1
    cardsdict_text[ind] = 'Red Joker'
    ind+=1

    cardsdict_text[ind] = 'Black Joker'


    captturn = -1
    players = []
    playernames = set()
    pickednames = set()
    team1 = []
    team2 = []
    picking = False
    teams = ""
    hands = []
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)
        time.sleep(0.1)
        # print(message_object.text)
        if(thread_id==self.gcuid):
            if(message_object.text == '!shuffle'):
                random.shuffle(self.cards)
                self.sendMessage("Cards have been shuffled ", thread_id = self.gcuid, thread_type = ThreadType.GROUP)
            elif('!enter_players' in message_object.text):
                data = message_object.text.replace('!enter_players', '')
                self.players.clear()
                self.playernames = {x.strip() for x in data.split(',')}
                for name in self.playernames:
                    self.players.append(self.searchForUsers(name)[0])
                # print(players)
                print(self.playernames)
                self.sendMessage("Players have been entered", thread_id = self.gcuid, thread_type = ThreadType.GROUP)
            elif('!format_emoji' in message_object.text):
                self.prefs[author_id] = 'emoji'
                # suits = suits_emoji
                self.sendMessage("Cards will format as emojis for you", thread_id=self.gcuid, thread_type=ThreadType.GROUP)
            elif('!format_text' in message_object.text):
                self.prefs[author_id] = 'text'
                # suits = suits_text
                self.sendMessage("Cards will format as text for you", thread_id=self.gcuid, thread_type=ThreadType.GROUP)
            elif("!captains" in message_object.text):
                self.pickednames = set()
                self.picking = True
                self.team1 = []
                self.team2 = []
                random.shuffle(self.players)
                random.shuffle(self.players)
                self.team1.append(self.players[0])
                self.team2.append(self.players[1])
                self.pickednames.add(self.players[0].name)
                self.pickednames.add(self.players[1].name)
                cptmsg = "Captains are selected as "+self.players[0].name+" and "+self.players[1].name+". "
                self.send(Message(text=cptmsg), thread_id=self.gcuid, thread_type=ThreadType.GROUP)
                pickmsg = self.players[0].name+" pick one player"
                self.send(Message(text=pickmsg), thread_id=self.gcuid, thread_type=ThreadType.GROUP)
                available = "Available: "+str(self.playernames-self.pickednames)
                self.send(Message(text=available), thread_id=self.gcuid, thread_type=ThreadType.GROUP)
                self.captturn = 1
            elif('!pick' in message_object.text):
                if(self.picking):
                    if(author_id==self.team1[0].uid and self.captturn==1):
                        pickedname = message_object.text.replace('!pick','').strip()
                        # print(pickedname)
                        if(pickedname in self.playernames and pickedname not in self.pickednames):
                            self.pickednames.add(pickedname)
                            for player in self.players:
                                if(player.name==pickedname):
                                    self.team1.append(player)
                                    break
                            if((len(self.playernames)-len(self.pickednames))==1):
                                for player in self.players:
                                    if(player.name not in self.pickednames):
                                        self.team2.append(player)
                                self.teams = "Team 1: "+str([player.name for player in self.team1])+", Team 2: "+str([player.name for player in self.team2  ])
                                self.send(Message(text=self.teams), thread_id=self.gcuid, thread_type=ThreadType.GROUP)
                                self.picking = False
                                self.capturn = -1
                            elif(len(self.team1)<=len(self.team2)):
                                pickmsg = self.team1[0].name+" make a pick"
                                self.sendMessage(pickmsg, thread_id = self.gcuid, thread_type = ThreadType.GROUP)
                                available = "Available: "+str(self.playernames-self.pickednames)
                                self.send(Message(text=available), thread_id=self.gcuid, thread_type=ThreadType.GROUP)
                            else:
                                self.capturn = 2
                                pickmsg = self.team2[0].name+" make a pick"
                                self.sendMessage(pickmsg, thread_id = self.gcuid, thread_type = ThreadType.GROUP)
                                available = "Available: "+str(self.playernames-self.pickednames)
                                self.send(Message(text=available), thread_id=self.gcuid, thread_type=ThreadType.GROUP)
                        else:
                            self.sendMessage("Invalid pick :|", thread_id = self.gcuid, thread_type = ThreadType.GROUP)
                    elif(author_id==self.team2[0].uid):
                        pickedname = message_object.text.replace('!pick','').strip()
                        # print(pickedname)
                        if(pickedname in self.playernames and pickedname not in self.pickednames):
                            self.pickednames.add(pickedname)
                            for player in self.players:
                                if(player.name==pickedname):
                                    self.team2.append(player)
                                    break
                            if((len(self.playernames)-len(self.pickednames))==1):
                                for player in self.players:
                                    if(player.name not in self.pickednames):
                                        self.team1.append(player)
                                self.teams = "Team 1: "+str([player.name for player in self.team1])+", Team 2: "+str([player.name for player in self.team2  ])
                                self.send(Message(text=self.teams), thread_id=self.gcuid, thread_type=ThreadType.GROUP)
                                self.picking = False
                                self.capturn = -1
                            elif(len(self.team2)<=len(self.team1)):
                                pickmsg = self.team2[0].name+" make a pick"
                                self.sendMessage(pickmsg, thread_id = self.gcuid, thread_type = ThreadType.GROUP)
                                available = "Available: "+str(self.playernames-self.pickednames)
                                self.send(Message(text=available), thread_id=self.gcuid, thread_type=ThreadType.GROUP)
                            else:
                                self.capturn = 1
                                pickmsg = self.team1[0].name+" make a pick"
                                self.sendMessage(pickmsg, thread_id = self.gcuid, thread_type = ThreadType.GROUP)
                                available = "Available: "+str(self.playernames-self.pickednames)
                                self.send(Message(text=available), thread_id=self.gcuid, thread_type=ThreadType.GROUP)
                        else:
                            self.sendMessage("Invalid pick :|", thread_id = self.gcuid, thread_type = ThreadType.GROUP)
                    else:
                        self.sendMessage("Not your turn :'(", thread_id = self.gcuid, thread_type = ThreadType.GROUP)
                else:
                    self.sendMessage("Send !select_teams to start picking process", thread_id = self.gcuid, thread_type = ThreadType.GROUP)
            elif(message_object.text == '!start_game'):
                playersrestructured = []
                for i in range(len(self.team1)):
                    playersrestructured.append(self.team1[i])
                    playersrestructured.append(self.team2[i])
                self.players = playersrestructured
                if(self.teams==""):
                    random.shuffle(self.players)
                    self.teams = "Team 1: "+str([self.players[i].name for i in range(0,len(self.players),2)])+" | Team 2: "+str([self.players[i].name for i in range(1,len(self.players),2)])
                    self.send(Message(text=self.teams), thread_id=self.gcuid, thread_type=ThreadType.GROUP)

                self.starting_message = str(random.choice(self.players).name) + " gets the first ask"
                self.send(Message(text=self.starting_message), thread_id=self.gcuid, thread_type=ThreadType.GROUP)
                ind=0
                uneven = False
                handsize = int(len(self.cards)/len(self.players))
                extracards = len(self.cards)-len(self.players)*handsize
                for i in range(len(self.players)):
                    handnums = []
                    for j in range(handsize):
                        handnums.append(self.cards[ind])
                        ind+=1
                    if(extracards):
                        handnums.append(self.cards[ind])
                        ind+=1
                        extracards-=1
                    handnums.sort()
                    self.player_pref = None

                    if self.players[i].uid in self.prefs:
                        self.player_pref = self.prefs[self.players[i].uid]

                    if(self.player_pref == 'emoji'):
                        self.cardsdict = self.cardsdict_emoji
                    else:
                        self.cardsdict = self.cardsdict_text

                    handstrs = [self.cardsdict[cardnum] for cardnum in handnums]
                    self.hands.append(handstrs)

                #commented this line out bc it gives the emoji formatting someone else then, if you shuffle cards before you should be good
                #random.shuffle(self.hands)
                self.sendMessage("Sending out hands ", thread_id = self.gcuid, thread_type = ThreadType.GROUP)
                for i in range(len(self.players)):
                    # self.send(Message(text="Hello "+self.players[i].name+", here is your hand for fish: "), thread_id=self.gcuid, thread_type=ThreadType.GROUP)
                    # self.send(Message(text=str(self.hands[i])), thread_id=self.gcuid, thread_type=ThreadType.GROUP)
                    self.send(Message(text="Hello "+self.players[i].name+", here is your hand for fish: "), thread_id=self.players[i].uid, thread_type=ThreadType.USER)
                    handmsgid = self.send(Message(text=str(self.hands[i])), thread_id=self.players[i].uid, thread_type=ThreadType.USER)
                    if(self.uid!=self.players[i].uid): #delete for everyone but the person who runs the program if they are playing so they can't cheat
                        self.deleteMessages(handmsgid)
                    self.send(Message(text="Teams have been picked as "+self.teams), thread_id=self.players[i].uid, thread_type=ThreadType.USER)
                self.teams = ""
                self.hands = []
            elif("!forfeit" in message_object.text):
                self.send(Message(text="No u :)"), thread_id=self.gcuid, thread_type=ThreadType.GROUP)

# username = input("Enter fb username: ")
# password = getpass()
client = FishBot(CREDENTIALS['USERNAME'], CREDENTIALS['PASSWORD'])
client.listen()
