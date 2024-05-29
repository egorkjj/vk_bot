import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
from DBSM import db_check, user_step_change, all_user
from aiogram import Bot
import asyncio




async def vk_apply():

    env = Env()
    env.read_env(".env")
    token = env.str("API_KEY")
    bot_token = env.str("BOT_TOKEN")
    bot = Bot(token=bot_token, parse_mode = 'HTML')

    def write_msg(user_id, message, kb):
        vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": 0, "keyboard": kb})

    def create_kb(text):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button(f'{text}', color= VkKeyboardColor.POSITIVE)
        return keyboard.get_keyboard()

    # Авторизуемся как сообщество
    vk = vk_api.VkApi(token=token)
    api = vk.get_api()

    # Работа с сообщениями
    longpoll = VkLongPoll(vk)

    # Основной цикл
    for event in longpoll.listen():

        # Если пришло новое сообщение
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:

                request = event.text

                user = api.users.get(user_ids= event.user_id, fields = "screen_name")
                name_short = user[0].get("screen_name")

                if request == "Начать":
                    if db_check(name_short):
                        user_step_change(name_short, 2)
                    text = f"Приветствую, {user[0]['first_name']}👋\n\nМы рекламное агентство в банковской сфере, которое дает своим клиентам возможность зарабатывать онлайн.\n\n💬 Вы может ознакомиться с отзывами о работе с нами, вы лично можете пообщаться с любым пользователем, как гарантом исполнения наших обязательств:\n👉 [link1]\n\n**Картинка**"
                    write_msg(event.user_id, text, create_kb("Начать работать👨‍💻"))

                elif request == "Начать работать👨‍💻":
                    if db_check(name_short):
                        user_step_change(name_short, 3)
                    text = "Каждый может начать зарабатывать уже СЕГОДНЯ👇\n\n📍 Суть подработки:\n\n— Вы оформляйте БЕСПЛАТНЫЕ продукты банка, по нашей реферальной программе.\n— После получения дебетовых карт на руки, вы сможете сразу заказать выплату, которая поступит вам в течение дня.\n— Вы ничем не рискуйте и никаких вложений.\n\nБанки платят, чтобы вы завели их дебетовую карту, а мы делимся с Вами!💶\n\nОплата сразу в день получения любой из карт, переводом!\n\nВы получайте оплату от 500₽ - 15 000₽, переводом на любой банк, в зависимости от кол-ва выполненных заданий.\n\nВыплаты проводятся ежедневно, с 8:00 - 22:00 по МСК!\n\n✅ Легальная подработка по реферальной программе известных банков РФ!"
                    write_msg(event.user_id, text, create_kb("Далее"))

                elif request == "Далее":
                    if db_check(name_short):
                        user_step_change(name_short, 4)
                    text = "📲⚒Что необходимо делать:\n\n1) Заказать по нашим ссылкам БЕСПЛАТНЫЕ дебетовые карты;\n2) Получить карты в удобном месте (доставка на дом или по любому удобному адресу);\n3) Активировать карты и сообщить нам;\n4) Получить денежное вознаграждение!💶\n\nГотовы приступить прямо сейчас? Мы уже подобрали для Вас первые задания👇"
                    write_msg(event.user_id, text, create_kb("Получить задания"))

                elif request == "Получить задания":
                    if db_check(name_short):
                        user_step_change(name_short, 5)
                    text = "Отлично!\n\nВот доступный список заданий👇\n\nЧем больше заказанных карт - тем больше оплата.\n\n⚠ Заказывайте карты только тех банков, клиентом которых вы никогда не были, иначе оплату не получить!⚠\n\n[СПИСОК ОФФЕРОВ]\n\n👉 После получения любой из карт, вы можете написать нам в сообщество или нажать на кнопку 'Карта получена' ниже;\n↪ Далее приступаем к следующим заданиям!\n\n❓При возникновении вопросов свяжитесь с нашим менеджером [link2]"
                    write_msg(event.user_id, text, create_kb("Карта получена"))

                elif request == "Карта получена":
                    if db_check(name_short):
                        user_step_change(name_short, 6)
                    text = "Здравствуйте, чтобы убедиться в том, что карта получена, и провести вам выплату средств, в скором времени с вами свяжется наш менеджер 👨‍💻\n\n❗Обратите внимание на то, что карта должна быть получена и уже активирована❗\n\nЕсли все условия соблюдены, нажмите кнопку 'Ожидаю менеджера'👇"
                    write_msg(event.user_id, text, create_kb("Ожидаю менеджера"))
                
                elif request == "Ожидаю менеджера":
                    await bot.send_message(chat_id = 398346500, text= f"Пользователь @{name_short} ожидает менеджера")
                    if db_check(name_short):
                        user_step_change(name_short, 10)
                elif request == "/admin":
                    if name_short == "madriot" or name_short == "egorkjj":
                        res = all_user()
                        text = ""
                        for i in res:
                            step = f"шаг {i['step']}" if i['step'] != 10 else "дошел до последнего шага"
                            text += f"Пользователь {i['user']}: {step}\n"
                        write_msg(event.user_id, text, None)
                

if __name__ == "__main__":
    asyncio.run(vk_apply())