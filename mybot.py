#COMMENT
 # Ogni volta che il bot viene lanciato perde i valori salvati di vigil info e reperibiMatrix.. 
 # da provare il funzionamento con bot da telefoni diversi contemporaneamente
 # trovare modo per tenere reperibiMatrix on line e consultabile da tutti..
 # mettere aposto rimuovi personale: deve cercare in base al ID;
 # Cambiare il comando reperibile in qualcosa tipo "Modifica Reperibilita'"
 # vigilInfo deve essere una matrice in cui ognuno salva il proprio ID assieme alle proprie informazioni 
 # 
 # Pensare ad un eventuale "VIGILI IN SEDE" dove quando una persona e' in sede si segna e in caso qualcuno aggiunge o rimuove una reperibilita' gli arriva un messaggio
 # Di coseguenza al punto precedente il comando personale deve restituire sia i vigili in sede che quelli reperibili
 # 
 # Implementare comando segreto "/LaPieFraGio" con cui accedere alla "god mode": vedi reperibiMatrix e sedeMatrix, mandi messaggi singoli ecc..
 # trovare modo di hostare script di python


import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN
import sys, time
from pprint import pprint 

bot = telepot.Bot(TOKEN)
reperibiMatrix = ["Nessun reperibile al momento."]
sedeMatrix = ["Nessun vigile in sede al momento."]
vigilInfo = ""
def Testa(Lista):
    return Lista[0]
def Vuota(Lista):
    if len(Lista)==0:
        return True
    else:
        return False


#--------------ON_CHAT_MESSAGE------------

def on_chat_message(msg):
    global reperibiMatrix
    global sedeMatrix
    global vigilInfo
    content_type, chat_type, chat_id = telepot.glance(msg)
#InlineKeyboard:
    keyboardRep = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Aggiungi Reperibile", callback_data='aggiungi_press')],
        [InlineKeyboardButton(text="Rimuovi Reperibile", callback_data='rimuovi_press')],
    ])


#COMANDI:
#start
    if msg['text']=="/start":
        bot.sendMessage(chat_id, "Ciao! benvenuto sul bot dei Vigili del Fuoco di Lazzate! Serve fare questo? Se e' la prima volta che avvii questo bot digita /settings.\nUsa /help per avere altre informazioni.")
#settings
    elif msg['text']=="/settings":
        bot.sendMessage(chat_id, "Scrivi in un messaggio il tuo nome, cognome e grado di patente ministeriale preceduto da _ in questo modo:\n_Nome Cognome 1")
#personale 
    elif msg['text']=="/personale": 
        if reperibiMatrix[0] == "Nessun reperibile al momento." :
            bot.sendMessage(chat_id, "Nessun reperibile al momento.")
        else:
            i = 0
            while i < len(reperibiMatrix):
                bot.sendMessage(chat_id, reperibiMatrix[i][1])
                i = i+1         
#reperibile    
    elif msg['text']=="/reperibile":
        bot.sendMessage(chat_id, "Vuoi aggiungerti come reperibile o vuoi rimuovere la tua reperibilita'?", reply_markup=keyboardRep)
#prova    
    elif msg['text']=="/prova":
        if Vuota(vigilInfo):
            bot.sendMessage(chat_id, "Nessun profilo salvato")
        else:
            bot.sendMessage(chat_id, vigilInfo[0:])
        bot.sendMessage(chat_id, reperibiMatrix[0:])
#sede
    elif msg['text']=="/sede":
        bot.sendMessage("289847356", "Vediamo se funziona il sendMessage con il codice ID")
        bot.sendMessage(chat_id, "Hai attivato il comando sono in sede.. Lo stiamo Implementando")
#help    
    elif msg['text']=="/help":
        bot.sendMessage(chat_id, "Hai attivato il comando help.. BRAVO!")
#VigilInfo
    elif msg['text'][0]=='_':
        temp = True
        i = 0
        while i < len(reperibiMatrix):
            if vigilInfo[i][0] == chat_id:
                temp = False
                bot.sendMessage(chat_id, "Sei gia' presente nel sistema come:")
                bot.sendMessage(chat_id, vigilInfo[i][1])
            i = i+1  
        if temp:
            vigilInfo.append([chat_id, msg['text'][1:]+" grado"])
            bot.sendMessage(chat_id, "Perfetto! Grazie mille!\nIl sistema ti ha memorizzato come:")    
            bot.sendMessage(chat_id, vigilInfo)[len(vigilInfo)-1:]          
#default    
    else:
        bot.sendMessage(chat_id, "Non hai inserito un comando valido.. Non che ce ne siano molti.. Ma il tuo non vale!")



#--------------ON_CALLBACK_QUERY--------------

def on_callback_query(msg):
    global reperibiMatrix
    global sedeMatrix
    global vigilInfo
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

#RISPOSTE ALLA TASTIERA INLINE:
#aggiungi personale
    if query_data =="aggiungi_press":     
    #    bot.answerCallbackQuery(query_id, text="La tua reperibilita' e' stata inserita! /personale per vedere i reperibili al momento")
        if reperibiMatrix[0] == "Nessun reperibile al momento." :
            reperibiMatrix[0] = [from_id, vigilInfo]
        else: 
            reperibiMatrix.append([from_id, vigilInfo])
        bot.sendMessage(from_id, "abbiamo aggiunto la tua reperibilita'")
        bot.sendMessage(from_id, vigilInfo[0:])
      #  print(reperibiMatrix)
      #  bot.sendMessage(from_id, "Qui si andremo a creare un log per inserire la propria reperibilita'")
#rimuovi personale
    elif query_data == "rimuovi_press":
        if reperibiMatrix[0] == "Nessun reperibile al momento.":
            bot.sendMessage(from_id, "Non e' presente alcuna reperibilita' da rimuovere!")
        else:
            i = 0
            while i < len(reperibiMatrix):
                if reperibiMatrix[i][0] == from_id:
                    reperibiMatrix.remove([from_id, vigilInfo])
                i = i+1  

        bot.sendMessage(from_id, "abbiamo rimosso la tua reperibilita'")

    

    #bot.answerCallbackQuery(query_id, text="YEAH")

bot.message_loop({'chat': on_chat_message,'callback_query': on_callback_query})

while 1:
    time.sleep(1)