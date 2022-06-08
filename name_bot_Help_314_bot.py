


def message_tovar (user_id,namebot,message_id,kod_produkta,regim):    
    name = ''
    price = 0
    about = ''
    import iz_func    
    db,cursor = iz_func.connect ()
    sql = "select id,name,price,kod_1c,about from bot_product where kod_1c = "+str(kod_produkta)+"" 
    cursor.execute(sql)
    data = cursor.fetchall()
    id = 0
    for rec in data: 
        id,name,price,kod_1c,about  = rec.values()    
    if id != 0:
        from telebot import types    
        import iz_telegram
        import telebot
        markup = types.InlineKeyboardMarkup(row_width=4)
        sql = "select id,id_tovar,koll from bot_select_tovar where namebot = '"+str(namebot)+"' and user_id = '"+str(user_id)+"' and id_tovar = '"+str(kod_produkta)+"'" 
        cursor.execute(sql)
        data = cursor.fetchall()
        id = 0
        koll = 1
        for rec in data: 
            id,id_tovar,koll = rec.values() 

        if id == 0:
            sql = "INSERT INTO bot_select_tovar (id_tovar,koll,name_tovar,namebot,user_id) VALUES ('{}',{},'{}','{}','{}')".format (kod_produkta,koll,name,namebot,user_id)
            cursor.execute(sql)
            db.commit()
        mn011 = types.InlineKeyboardButton(text=  iz_telegram.get_namekey (user_id,namebot,"-1"),callback_data = "add1_"+str(kod_produkta))
        mn012 = types.InlineKeyboardButton(text=  iz_telegram.get_namekey (user_id,namebot,str(int(koll))+" шт."),callback_data = "back_"+str(kod_produkta))
        mn013 = types.InlineKeyboardButton(text=  iz_telegram.get_namekey (user_id,namebot,"+1"),callback_data = "add2_"+str(kod_produkta))
        markup.add(mn011,mn012,mn013)
        sql = "select id,`like` from bot_favorites where namebot = '{}' and user_id = {} and id_tovar = '{}' limit 1;".format(namebot,user_id,kod_produkta)
        cursor.execute(sql)
        data = cursor.fetchall()
        like = 0
        for rec in data: 
            id,like = rec.values()    
        mn021 = types.InlineKeyboardButton(text=  iz_telegram.get_namekey (user_id,namebot,"❤ ("+str(like)+")"),callback_data = "like_"+str(kod_produkta))
        mn022 = types.InlineKeyboardButton(text=  iz_telegram.get_namekey (user_id,namebot,"Корзина "+str(price)+" грв."),callback_data = "Корзина_"+str(kod_produkta))
        markup.add(mn021,mn022)
        mn031 = types.InlineKeyboardButton(text=  iz_telegram.get_namekey (user_id,namebot,"Назад"),callback_data = "back_"+str(kod_produkta))
        markup.add(mn031)
        if regim == 'new':
            message_out,menu = iz_telegram.get_message (user_id,'Шапка товара',namebot)
            message_out = message_out.replace('%%name%%',name)
            message_out = message_out.replace('%%about%%',about)
            message_out = message_out.replace('%%price%%',str(price))    
            answer = iz_telegram.bot_send (user_id,namebot,message_out,'',message_id) 
            namefile = ''
            try:        
                namefile = '/home/izofen/Data/FTP/'+str(name)
                print ('[+] Имя файла для скачивания:',namefile)
                photo = open(namefile, 'rb')
                token = iz_telegram.get_token (namebot)
                bot   = telebot.TeleBot(token)
                bot.send_photo(user_id, photo)        
            except Exception as e:
                print ('[+]',namefile,e)
                namefile = iz_telegram.bot_setting(namebot,'Файл отсутствие картинки')
                if namefile == '':
                    namefile = '/home/izofen/Studiya/FL/picture/no_foto-800x800.jpg'
                photo = open(namefile, 'rb')
                token = iz_telegram.get_token (namebot)
                try:
                    bot   = telebot.TeleBot(token)
                    bot.send_photo(user_id, photo)        
                except:
                    pass         
            message_out,menu = iz_telegram.get_message (user_id,"Описание товара",namebot)
            message_out = message_out.replace('%%name%%',name)
            message_out = message_out.replace('%%about%%',about)
            message_out = message_out.replace('%%price%%',str(price))    
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
        if regim == 'reg':
            message_out,menu = iz_telegram.get_message (user_id,"Описание товара",namebot)
            message_out = message_out.replace('%%name%%',name)
            message_out = message_out.replace('%%about%%',about)
            message_out = message_out.replace('%%price%%',str(price))    
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id) 
    else:
        print ('[+] Товар не обнаружен')    




def add_menu (markup,user_id,namebot):
    import iz_telegram
    from telebot import types
    setting = iz_telegram.get_namekey (user_id,namebot,'Фильтр')        
    mn01 = types.InlineKeyboardButton(text=setting,callback_data = "Фильтр")
    markup.add(mn01)
    return markup



def start_prog (user_id,namebot,message_in,status,message_id,name_file_picture,telefon_nome):
    import time
    import iz_func
    import iz_telegram    
    import datetime

    if message_in == 'Отмена':
        iz_telegram.save_variable (user_id,namebot,"status",'')
        status = ""

    if message_in == '👨‍💻Поддержка':
        iz_telegram.save_variable (user_id,namebot,"status",'Поддержка')

    if status == 'Поддержка':
        import iz_func
        iz_telegram.save_variable (user_id,namebot,"status",'')
        #message_out,menu = iz_telegram.get_message (user_id,"Спасибо за ответ",namebot)
        #markup = menu_select_start (user_id,namebot,menu)
        #markup = ""
        #answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,"Спасибо за ответ",'S',0) 
        db,cursor = iz_func.connect ()
        sql = "INSERT INTO bot_support_service (answer,message,namebot,user_id) VALUES ('{}','{}','{}','{}')".format ('',message_in,namebot,user_id)
        cursor.execute(sql)
        db.commit()


    if message_in.find ('katalog_') != -1:
        word  = message_in.replace('katalog_','')
        label = 'no send'
        parents = word
        if_grup = iz_telegram.if_grup (user_id,namebot,word)        
        if if_grup == 'Да':
            sql_id = iz_telegram.start_list (user_id,namebot,10,0,'не равно 0','не равно 0')
            markup = iz_telegram.get_menu_tovar (user_id,namebot,message_id,parents,sql_id,2)
            markup = add_menu (markup,user_id,namebot)
            message_out,menu = iz_telegram.get_message (user_id,'Каталог товаров',namebot)
            answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)

        if if_grup == 'Нет' or if_grup == '':  
            db,cursor = iz_func.connect ()
            sql = "UPDATE bot_select_tovar SET koll = 1 WHERE `id_tovar` = '"+str(word)+"'"
            cursor.execute(sql)
            db.commit()   
            message_tovar (user_id,namebot,message_id,word,'new')



    if message_in == 'list_prodykt':
        label = 'no send'
        parents = "Родитель Продукта в 1С не указан"
        sql_id = iz_telegram.start_list (user_id,namebot,10,0,'не равно 0','не равно 0',parents)
        markup = iz_telegram.get_menu_tovar (user_id,namebot,message_id,parents,sql_id,2)
        markup = add_menu (markup,user_id,namebot)  
        message_out,menu = iz_telegram.get_message (user_id,'Каталог товаров',namebot)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)


    if message_in.find("next_sql_") != -1:
        word  = message_in.replace('next_sql_','')
        iz_telegram.next_menu_tovar (user_id,namebot,word)
         
        label = 'no send'
        parents = "Родитель Продукта в 1С не указан"
        #sql_id = iz_telegram.start_list (user_id,namebot,10,0,'не равно 0','не равно 0',parents)
        markup = iz_telegram.get_menu_tovar (user_id,namebot,message_id,parents,word,2)
        markup = add_menu (markup,user_id,namebot)  
        message_out,menu = iz_telegram.get_message (user_id,'Каталог товаров',namebot)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)





    if message_in == '📘 Каталог': 
        label = 'no send'
        parents = "Родитель Продукта в 1С не указан"
        sql_id = iz_telegram.start_list (user_id,namebot,10,0,'не равно 0','не равно 0',parents,0)
        markup = iz_telegram.get_menu_tovar (user_id,namebot,message_id,parents,sql_id,2)
        markup = add_menu (markup,user_id,namebot)  
        message_out,menu = iz_telegram.get_message (user_id,'Каталог товаров',namebot)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)
        #message_out,menu = iz_telegram.get_message (user_id,"Товар 1",namebot)
        ##markup = menu_select_start (user_id,namebot,menu)
        #from telebot import types  
        #markup = types.InlineKeyboardMarkup(row_width=4)
        #mn011 = types.InlineKeyboardButton(text=iz_telegram.get_namekey (user_id,namebot,"В корзину"),callback_data = "add_"+str(1))
        #markup.add(mn011)
        #answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 

        #message_out,menu = iz_telegram.get_message (user_id,"Товар 2",namebot)
        #markup = types.InlineKeyboardMarkup(row_width=4)
        #mn011 = types.InlineKeyboardButton(text=iz_telegram.get_namekey (user_id,namebot,"Открыть список товаров"),callback_data = "list_prodykt")
        #markup.add(mn011)
        #answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 

        #message_out,menu = iz_telegram.get_message (user_id,"Товар 3",namebot)
        #markup = ""
        #answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 



    if message_in == '🛒 Корзина':        
        message_out,menu = iz_telegram.get_message (user_id,"Список товаров в корзине",namebot)
        #markup = menu_select_start (user_id,namebot,menu)
        markup = ""
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 

    if message_in == 'Активные сделки':        

        message_out,menu = iz_telegram.get_message (user_id,"Активные сделки 2",namebot)
        #markup = menu_select_start (user_id,namebot,menu)
        markup = ""
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 

    if message_in == 'Кошелек':
        message_out,menu = iz_telegram.get_message (user_id,"Пополнить кошелек",namebot)
        #markup = menu_select_start (user_id,namebot,menu)
        #markup = ""
        from telebot import types  
        markup = types.InlineKeyboardMarkup(row_width=4)
        mn011 = types.InlineKeyboardButton(text=iz_telegram.get_namekey (user_id,namebot,"Bitcoin BTC"),callback_data = "cript_"+str("BTC"))
        markup.add(mn011)
        mn012 = types.InlineKeyboardButton(text=iz_telegram.get_namekey (user_id,namebot,"Litecoin LTC"),callback_data = "cript_"+str("LTC"))
        markup.add(mn012)
        mn013 = types.InlineKeyboardButton(text=iz_telegram.get_namekey (user_id,namebot,"Ether ETH"),callback_data = "cript_"+str("ETH"))
        markup.add(mn013)
        mn014 = types.InlineKeyboardButton(text=iz_telegram.get_namekey (user_id,namebot,"Monero XMR "),callback_data = "cript_"+str("XMR"))
        markup.add(mn014)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 

    if message_in == 'cript_BTC':    
        #message_out,menu = iz_telegram.get_message (user_id,"Сумма пополнения BTC",namebot)
        message_out,menu = iz_telegram.get_message (user_id,'Сумма пополнения BTC',namebot)        
        markup = ""
        amount    = 100 
        currency  = 'BTC'
        lastid,checkout_url,address,amount = iz_func.chek (amount,currency,user_id,namebot)
        print ('[+] checkout_url',checkout_url)
        message_out = message_out.replace('%%Адрес%%','<code>'+address+'</code>')   
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)

    if message_in == 'cript_XMR':    
        #message_out,menu = iz_telegram.get_message (user_id,"Сумма пополнения BTC",namebot)
        message_out,menu = iz_telegram.get_message (user_id,'Сумма пополнения BTC',namebot)        
        markup = ""
        amount    = 100 
        currency  = 'XMR'
        lastid,checkout_url,address,amount = iz_func.chek (amount,currency,user_id,namebot)
        print ('[+] checkout_url',checkout_url)
        message_out = message_out.replace('%%Адрес%%','<code>'+address+'</code>')   
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)

    if message_in == 'cript_ETH':    
        #message_out,menu = iz_telegram.get_message (user_id,"Сумма пополнения BTC",namebot)
        message_out,menu = iz_telegram.get_message (user_id,'Сумма пополнения BTC',namebot)        
        markup = ""
        amount    = 100 
        currency  = 'ETH'
        lastid,checkout_url,address,amount = iz_func.chek (amount,currency,user_id,namebot)
        print ('[+] checkout_url',checkout_url)
        message_out = message_out.replace('%%Адрес%%','<code>'+address+'</code>')   
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)

    if message_in == 'cript_LTC':    
        #message_out,menu = iz_telegram.get_message (user_id,"Сумма пополнения BTC",namebot)
        message_out,menu = iz_telegram.get_message (user_id,'Сумма пополнения BTC',namebot)        
        markup = ""
        amount    = 100 
        currency  = 'LTC'
        lastid,checkout_url,address,amount = iz_func.chek (amount,currency,user_id,namebot)
        print ('[+] checkout_url',checkout_url)
        message_out = message_out.replace('%%Адрес%%','<code>'+address+'</code>')   
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)

