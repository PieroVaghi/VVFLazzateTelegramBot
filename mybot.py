#COMMENT
 # Ogni volta che il bot viene lanciato perde i valori salvati di vigil info e reperibiMatrix.. 
 # Cambiare il comando reperibile in qualcosa tipo "Modifica Reperibilita'"
 # Finire di scrivere l'help in config
 # se sono in sede non dovrei essere reperibile e se sono reperibile non dovrei essere in sede
 # 
 # Una persona e' in sede si segna e in caso qualcuno aggiunge o rimuove una reperibilita' gli arriva un messaggio
 # Di coseguenza al punto precedente il comando personale deve restituire sia i vigili in sede che quelli reperibili
 # 
 # Implementare comando segreto "/LaPieFraGio" con cui accedere alla "god mode": vedi reperibiMatrix e sedeMatrix, mandi messaggi singoli ecc..
 # trovare modo di hostare script di python


import telepot
import datetime
import sys, time
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN
from config import HELP
from pprint import pprint 

bot = telepot.Bot(TOKEN)
noRep = "Nessun reperibile al momento."
reperibiMatrix = [noRep]
noSede = "Nessun vigile in sede al momento."
sedeMatrix = [noSede]
vigilInfo = []
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
        [InlineKeyboardButton(text="Aggiungi la tua reperibilita'", callback_data='aggiungi_press')],
        [InlineKeyboardButton(text="Rimuovi la tua reperibilita'", callback_data='rimuovi_press')],
    ])
    keyboardSed = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Sono in sede", callback_data='sede_press')],
        [InlineKeyboardButton(text="Vado a casa", callback_data='casa_press')],
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
        bot.sendMessage(chat_id, "Personale in sede:")
        if sedeMatrix[0] == noSede :
            bot.sendMessage(chat_id, noSede)
        else:
            i = 0
            while i < len(sedeMatrix):
                bot.sendMessage(chat_id, sedeMatrix[i][1])
                i = i+1 
        bot.sendMessage(chat_id, "Personale reperibile:")
        if reperibiMatrix[0] == noRep :
            bot.sendMessage(chat_id, noRep)
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
            bot.sendMessage(chat_id, "VigilInfo:")
            bot.sendMessage(chat_id, vigilInfo[0:])
        bot.sendMessage(chat_id, "sedeMatrix:")
        bot.sendMessage(chat_id, sedeMatrix[0:])
        bot.sendMessage(chat_id, "reperibiMatrix:")
        bot.sendMessage(chat_id, reperibiMatrix[0:])      
#sede
    elif msg['text']=="/sede":
        bot.sendMessage(chat_id, "Sei appena arrivato in sede o stai andando via?", reply_markup=keyboardSed)
#VigilInfo
    elif msg['text'][0]=='_':
        temp = True
        i = 0
        while i < len(vigilInfo):
            if vigilInfo[i][0] == chat_id:
                temp = False
                bot.sendMessage(chat_id, "Sei gia' presente nel sistema come:")
                bot.sendMessage(chat_id, vigilInfo[i][1])
            i = i+1  
        if temp:
            infoV = msg['text'][1:]+" grado"
            vigilInfo.append([chat_id, infoV])
            bot.sendMessage(chat_id, "Perfetto! Grazie mille!\nIl sistema ti ha memorizzato come:")    
            bot.sendMessage(chat_id, vigilInfo[(len(vigilInfo)-1)][1])     
#help    
    elif msg['text']=="/help":
        bot.sendMessage(chat_id, HELP)
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
        flag = True    
        if reperibiMatrix[0] == noRep :
            i = 0
            while i < len(vigilInfo):
                if vigilInfo[i][0] == from_id:
                    reperibiMatrix[0]=([from_id, vigilInfo[i][1]])
                    bot.sendMessage(from_id, "abbiamo aggiunto la tua reperibilita'")
                i = i+1 
        else: 
            j = 0
            while j < len(reperibiMatrix):
                if reperibiMatrix[j][0] == from_id:
                    flag = False
                    bot.sendMessage(from_id, "Risulti essere gia' reperibile!")
                j = j+1
            i = 0
            while i < len(vigilInfo):
                if (vigilInfo[i][0] == from_id) & (flag):
                    reperibiMatrix.append([from_id, vigilInfo[i][1]])
                    bot.sendMessage(from_id, "abbiamo aggiunto la tua reperibilita'")
                i = i+1     
        i = 0
        while i < len(vigilInfo):
            if vigilInfo[i][0] == from_id:
                bot.sendMessage(from_id, vigilInfo[i][1])
            i = i+1 
      #  print(reperibiMatrix)
      #  bot.sendMessage(from_id, "Qui si andremo a creare un log per inserire la propria reperibilita'")
#rimuovi personale
    elif query_data == "rimuovi_press":
        if reperibiMatrix[0] == noRep:
            bot.sendMessage(from_id, "Non e' presente alcuna reperibilita' da rimuovere!")
        else:
            i = 0
            while i < len(reperibiMatrix):
                if reperibiMatrix[i][0] == from_id:
                    reperibiMatrix.remove(reperibiMatrix[i])
                i = i+1  

        bot.sendMessage(from_id, "abbiamo rimosso la tua reperibilita'")
        if Vuota(reperibiMatrix):
            reperibiMatrix.append(noRep)
#sono in sede
    elif query_data =="sede_press": 
        flag = True    
        if sedeMatrix[0] == noSede :
            i = 0
            while i < len(vigilInfo):
                if vigilInfo[i][0] == from_id:
                    sedeMatrix[0]=([from_id, vigilInfo[i][1]])
                    bot.sendMessage(from_id, "Sei stato inserito in sede!")
                i = i+1 
        else: 
            j = 0
            while j < len(sedeMatrix):
                if sedeMatrix[j][0] == from_id:
                    flag = False
                    bot.sendMessage(from_id, "Risulti essere gia' in sede!")
                j = j+1
            i = 0
            while i < len(vigilInfo):
                if (vigilInfo[i][0] == from_id) & (flag):
                    sedeMatrix.append([from_id, vigilInfo[i][1]])
                    bot.sendMessage(from_id, "Sei stato inserito in sede!")
                i = i+1     
        i = 0
        while i < len(vigilInfo):
            if vigilInfo[i][0] == from_id:
                bot.sendMessage(from_id, vigilInfo[i][1])
            i = i+1      
#vado a casa
    elif query_data == "casa_press":
        if sedeMatrix[0] == noSede:
            bot.sendMessage(from_id, "Non risulta esserci nessun vigile in sede")
        else:
            i = 0
            while i < len(sedeMatrix):
                if sedeMatrix[i][0] == from_id:
                    sedeMatrix.remove(sedeMatrix[i])
                i = i+1  

        bot.sendMessage(from_id, "Sei stato tolto dall'elenco dei vigili in sede")
        if Vuota(sedeMatrix):
            sedeMatrix.append(noSede)

    #bot.answerCallbackQuery(query_id, text="YEAH")

bot.message_loop({'chat': on_chat_message,'callback_query': on_callback_query})

while 1:
    time.sleep(1)