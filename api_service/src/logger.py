import logging
import os

Logger = logging.getLogger("nanozymes_bot")
Logger.setLevel(logging.INFO)

if not os.path.exists("logs"):
    os.mkdir("logs")

file_handler = logging.FileHandler("logs/nanozymes_bot.log")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
Logger.addHandler(file_handler)
