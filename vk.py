import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
from DBSM import user_step_change, all_link, user_step_check, for_th, loop, disable_messages, is_disabled
from aiogram import Bot
from threading import Thread as th
import asyncio
import requests
import time




async def vk_apply() -> None:
    while True:
        try:
            #read env
            env = Env()
            env.read_env(".env")
            token = env.str("API_KEY")
            bot_token = env.str("BOT_TOKEN")

            # тг бот
            bot = Bot(token=bot_token, parse_mode = 'HTML')

            # пишем сообщение
            def write_msg(user_id, message, kb) -> None:
                vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": 0, "keyboard": kb})

            #клавиатура
            def create_kb(text) -> str:
                keyboard = VkKeyboard(inline=True)
                keyboard.add_button(f'{text}', color= VkKeyboardColor.POSITIVE)
                return keyboard.get_keyboard()
            
            #клавиатура для двух последних шагов
            def create_last_kb(text) -> str:
                keyboard = VkKeyboard(inline=True)
                keyboard.add_button("Перейти к заданиям", color = VkKeyboardColor.POSITIVE)
                keyboard.add_button(f'{text}', color= VkKeyboardColor.POSITIVE)
                return keyboard.get_keyboard()
            
            def create_оff_kb(text) -> str:
                keyboard = VkKeyboard(inline=True)
                keyboard.add_button("Назад", color = VkKeyboardColor.POSITIVE)
                keyboard.add_button(f'{text}', color= VkKeyboardColor.POSITIVE)
                return keyboard.get_keyboard()
            
            #отправка фото
            def send_photo(id, text, kb) -> None:
                a = vk.method("photos.getMessagesUploadServer")
                b = requests.post(a['upload_url'], files={'photo': open('fotor.png', 'rb')}).json()
                c = vk.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
                d = "photo{}_{}".format(c["owner_id"], c["id"])
                vk.method("messages.send", {"user_id": id, "message": text, "attachment": d, "random_id": 0, "keyboard": kb})

            #формирование текста ссылок для офферов
            def links_text() -> str:
                data = all_link()
                text = ""
                for i in data:
                    text += f"\n{i}\n\n"
                return text

            # Авторизуемся как сообщество
            vk = vk_api.VkApi(token=token)
            api = vk.get_api()

            #рассылка по пользователям
            def sent_for_th(user_id, user_name):
                if not for_th(user_name):
                    return
                time.sleep(86400)
                if user_step_check(user_name) == 10:
                    return
                if user_step_check(user_name) != 7:
                    disable_messages(user_name)
                    links = links_text()
                    write_msg(user_id, f"Добрый день, ранее вы интересовались онлайн заработком на платформе WorkPoint, высылаем вам актуальный список заданий, выплату за который можно получить уже сегодня:\n{links}", None)
                else:
                    disable_messages(user_name)
                    write_msg(user_id, f"Добрый день, ранее вы получили список заданий от платформы онлайн подработки WorkPoint, подскажите, удалось ли оформить карты?", None)
            
            # Работа с сообщениями
            longpoll = VkLongPoll(vk)

            # Основной цикл
            for event in longpoll.listen():

                # Если пришло новое сообщение
                if event.type == VkEventType.MESSAGE_NEW:
                    # if message is to me
                    if event.to_me:
                        # message.text
                        request = event.text

                        # user_array and username
                        user = api.users.get(user_ids= event.user_id, fields = "screen_name")
                        name_short = user[0].get("screen_name")

                        #шаг, на котором сейчас пользователь в воронке
                        step = user_step_check(name_short)

                        # processing_messages
                        if request == "Начать":  #step2
                            user_step_change(name_short, 2)
                            loop(name_short,2)
                            th(target = sent_for_th, args=(event.user_id, name_short)).start()
                            text = f"Приветствую, {user[0]['first_name']}👋\n\nМы рекламное агентство в банковской сфере, которое дает своим клиентам возможность зарабатывать онлайн.\n\n💬 Вы может ознакомиться с отзывами о работе с нами, вы лично можете пообщаться с любым пользователем, как гарантом исполнения наших обязательств:\n👉 https://vk.com/topic-226064276_51178194\n\nДо первой выплаты осталось всего 3 шага!"
                            send_photo(event.user_id, text, create_kb("Начать работать👨‍💻"))

                        elif request == "Начать работать👨‍💻":  #step3
                            loop(name_short,3)
                            user_step_change(name_short, 3)
                            text = "Каждый может начать зарабатывать уже СЕГОДНЯ👇\n\n📍 Суть подработки:\n\n— Вы оформляйте БЕСПЛАТНЫЕ продукты банка, по нашей реферальной программе.\n— После получения дебетовых карт на руки, вы сможете сразу заказать выплату, которая поступит вам в течение дня.\n— Вы ничем не рискуйте и никаких вложений.\n\nБанки платят, чтобы вы завели их дебетовую карту, а мы делимся с Вами!💶\n\nОплата сразу в день получения любой из карт, переводом!\n\nВы получайте оплату от 500₽ - 15 000₽, переводом на любой банк, в зависимости от кол-ва выполненных заданий.\n\nВыплаты проводятся ежедневно, с 8:00 - 22:00 по МСК!\n\n✅ Легальная подработка по реферальной программе известных банков РФ!\n\nДо первой выплаты осталось всего 2 шага!"
                            write_msg(event.user_id, text, create_kb("Далее"))

                        elif request == "Далее":  #step4
                            loop(name_short,4)
                            user_step_change(name_short, 4)
                            text = "📲⚒Что необходимо делать:\n\n1) Заказать по нашим ссылкам БЕСПЛАТНЫЕ дебетовые карты;\n2) Получить карты в удобном месте (доставка на дом или по любому удобному адресу);\n3) Активировать карты и сообщить нам;\n4) Получить денежное вознаграждение!💶\n\nГотовы приступить прямо сейчас? Мы уже подобрали для Вас первые задания👇\n\nДо первой выплаты остался всего 1 шаг!"
                            write_msg(event.user_id, text, create_kb("Получить задания"))

                        elif request == "Получить задания":  #step5
                            loop(name_short, 5)
                            user_step_change(name_short, 5)
                            links = links_text()
                            text = f"Отлично!\n\nВот доступный список заданий👇\n\nЧем больше заказанных карт - тем больше оплата.\n\n⚠ Заказывайте карты только тех банков, клиентом которых вы никогда не были, иначе оплату не получить!⚠👉\n{links}После оформления любой из карт, вы можете написать нам в сообщество или нажать на кнопку 'Я оформил карту' ниже;\n↪ Далее приступаем к следующим заданиям!\n\n❓При возникновении вопросов свяжитесь с нашим менеджером: https://vk.com/madriot"
                            write_msg(event.user_id, text, create_оff_kb("Я оформил карту"))
                        
                        elif request == "Я оформил карту": #step6
                            loop(name_short,6)
                            user_step_change(name_short, 6)
                            text = "Замечательно!\n\nПоздравляем вас с оформлением, до получения выплаты осталось совсем немного!💵\n\n💬Пока вашу карту готовят к выдаче, вы можете оформить и другие карты - для этого нажмите на кнопку «Перейти к заданиям»👇\n\nПосле получения хотя бы одной из карт нажмите кнопку «Карта получена»👇"
                            write_msg(event.user_id, text, create_last_kb("Карта получена"))
                        
                        elif request == "Карта получена":  #step7
                            loop(name_short, 7)
                            user_step_change(name_short, 7)
                            text = "Здравствуйте, чтобы убедиться в том, что карта получена, и провести вам выплату средств, в скором времени с вами свяжется наш менеджер 👨‍💻\n\nЕсли все условия соблюдены, нажмите кнопку 'Ожидаю менеджера'👇"
                            write_msg(event.user_id, text, create_last_kb("Ожидаю менеджера"))
                        
                        elif request == "Ожидаю менеджера": # !! final step !!
                            loop(name_short,10)
                            #send message with bot
                            await bot.send_message(chat_id = 398346500, text= f"Пользователь https://vk.com/{name_short} ожидает менеджера")
                            user_step_change(name_short, 10)

                        elif request == "Вернуться к последнему шагу" or request == "Назад": #логика возвращения к предыдущему шагу
                            if request == "Назад":
                                stepn = step - 1
                            else:
                                stepn = step
                            if stepn == 4:
                                text = "📲⚒Что необходимо делать:\n\n1) Заказать по нашим ссылкам БЕСПЛАТНЫЕ дебетовые карты;\n2) Получить карты в удобном месте (доставка на дом или по любому удобному адресу);\n3) Активировать карты и сообщить нам;\n4) Получить денежное вознаграждение!💶\n\nГотовы приступить прямо сейчас? Мы уже подобрали для Вас первые задания👇"
                                write_msg(event.user_id, text, create_kb("Получить задания"))
                            elif stepn == 3:
                                text = "Каждый может начать зарабатывать уже СЕГОДНЯ👇\n\n📍 Суть подработки:\n\n— Вы оформляйте БЕСПЛАТНЫЕ продукты банка, по нашей реферальной программе.\n— После получения дебетовых карт на руки, вы сможете сразу заказать выплату, которая поступит вам в течение дня.\n— Вы ничем не рискуйте и никаких вложений.\n\nБанки платят, чтобы вы завели их дебетовую карту, а мы делимся с Вами!💶\n\nОплата сразу в день получения любой из карт, переводом!\n\nВы получайте оплату от 500₽ - 15 000₽, переводом на любой банк, в зависимости от кол-ва выполненных заданий.\n\nВыплаты проводятся ежедневно, с 8:00 - 22:00 по МСК!\n\n✅ Легальная подработка по реферальной программе известных банков РФ!"
                                write_msg(event.user_id, text, create_kb("Далее"))
                            elif stepn == 6:
                                text = "Замечательно!\n\nПоздравляем вас с оформлением, до получения выплаты осталось совсем немного!💵\n\n💬Пока вашу карту готовят к выдаче, вы можете оформить и другие карты - для этого нажмите на кнопку «Перейти к заданиям»👇\n\nПосле получения хотя бы одной из карт нажмите кнопку «Карта получена»👇"
                                write_msg(event.user_id, text, create_last_kb("Карта получена"))
                            elif stepn == 7:
                                text = "Здравствуйте, чтобы убедиться в том, что карта получена, и провести вам выплату средств, в скором времени с вами свяжется наш менеджер 👨‍💻\n\nЕсли все условия соблюдены, нажмите кнопку 'Ожидаю менеджера'👇"
                                write_msg(event.user_id, text, create_last_kb("Ожидаю менеджера"))
                            elif stepn == 5:
                                links = links_text()
                                text = f"Отлично!\n\nВот доступный список заданий👇\n\nЧем больше заказанных карт - тем больше оплата.\n\n⚠ Заказывайте карты только тех банков, клиентом которых вы никогда не были, иначе оплату не получить!⚠👉\n{links}После оформления любой из карт, вы можете написать нам в сообщество или нажать на кнопку 'Я оформил карту' ниже;\n↪ Далее приступаем к следующим заданиям!\n\n❓При возникновении вопросов свяжитесь с нашим менеджером: https://vk.com/madriot"
                                write_msg(event.user_id, text, create_оff_kb("Я оформил карту"))
                            elif stepn == 0:
                                keyboard = VkKeyboard(one_time=True)
                                keyboard.add_button(f'Начать', color= VkKeyboardColor.POSITIVE)
                                write_msg(event.user_id, "Я не смог распознать ваше сообщение, чтобы начать нажмите кнопку Начать", keyboard.get_keyboard())
                            elif stepn == 2:
                                text = f"Приветствую, {user[0]['first_name']}👋\n\nМы рекламное агентство в банковской сфере, которое дает своим клиентам возможность зарабатывать онлайн.\n\n💬 Вы может ознакомиться с отзывами о работе с нами, вы лично можете пообщаться с любым пользователем, как гарантом исполнения наших обязательств:\n👉 https://vk.com/topic-226064276_51178194"
                                send_photo(event.user_id, text, create_kb("Начать работать👨‍💻"))

                        
                        elif request == "Вернуться к списку заданий" or request == "Перейти к заданиям": #переход к офферам
                            if step != 0:
                                links = links_text()
                                text = f"Отлично!\n\nВот доступный список заданий👇\n\nЧем больше заказанных карт - тем больше оплата.\n\n⚠ Заказывайте карты только тех банков, клиентом которых вы никогда не были, иначе оплату не получить!⚠👉\n{links}После оформления любой из карт, вы можете написать нам в сообщество или нажать на кнопку 'Я оформил карту' ниже;\n↪ Далее приступаем к следующим заданиям!\n\n❓При возникновении вопросов свяжитесь с нашим менеджером: https://vk.com/madriot"
                                write_msg(event.user_id, text, create_оff_kb("Я оформил карту"))
                            else:
                                keyboard = VkKeyboard(one_time=True)
                                keyboard.add_button(f'Начать', color= VkKeyboardColor.POSITIVE)
                                write_msg(event.user_id, "Я не смог распознать ваше сообщение, чтобы начать нажмите кнопку Начать", keyboard.get_keyboard())
                        
                        else: #обработка левых сообщений
                            if is_disabled(name_short):
                                continue
                            if step == 0:
                                keyboard = VkKeyboard(one_time=True)
                                keyboard.add_button(f'Начать', color= VkKeyboardColor.POSITIVE)
                                write_msg(event.user_id, "Я не смог распознать ваше сообщение, чтобы начать нажмите кнопку Начать", keyboard.get_keyboard())
                            else:
                                write_msg(event.user_id, "Я не смог распознать ваше сообщение, нажмите на на кнопку ниже", create_kb("Вернуться к последнему шагу"))

        except Exception as e:
            print(e)
            pass             

if __name__ == "__main__":
    asyncio.run(vk_apply())
