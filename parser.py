from bs4 import BeautifulSoup, Tag
from collections import Counter

import requests
import re
import string


all_english_letters = set(string.ascii_uppercase)


def get_main_wiki_block(url: str = "https://en.wikipedia.org/wiki/Cryptography", path: str = "#mw-content-text > div.mw-content-ltr.mw-parser-output") -> Tag | None:
  if "en.wikipedia.org" not in url:
    return None
  response = requests.get(url)

  soup = BeautifulSoup(response.text, 'html.parser')
  main_block = soup.select_one(path)
  
  return main_block


def get_frequencies(main_block: Tag) -> dict[str, float]:
  full_text = ""
  if main_block:
    all_p = main_block.find_all("p")
    all_h2 = main_block.find_all("h2")
    all_li = main_block.find_all("li")

    for p in all_p:
      full_text += re.sub(r"[^A-Za-z]", '', p.text).upper()

    for h in all_h2:
      full_text += re.sub(r"[^A-Za-z]", '', h.text).upper()

    for li in all_li:
      full_text += re.sub(r"[^A-Za-z]", '', li.text).upper()
  
  total_count = dict(Counter(full_text))
  total_text_length = len(full_text)

  # Добавление пропущенных букв с 0 вероятностью
  for letter in all_english_letters:
    if letter not in total_count:
      total_count[letter] = 0.0

  for key, values in total_count.items():
    total_count[key] = round(values / total_text_length, 6)
  
  total_frequencies = {k: v for k, v in sorted(total_count.items(), key=lambda x: x[-1], reverse=True) }

  return total_frequencies