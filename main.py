from aiogram import executor
from config import bot, dp
from handlers import start, echo, commands, quiz, fsm_store, group


quiz.register_quiz(dp=dp)
start.register_start(dp=dp)
commands.register_commands(dp=dp)
fsm_store.register_fsm_store(dp=dp)
group.register_group(dp=dp)
echo.register_echo(dp=dp)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)