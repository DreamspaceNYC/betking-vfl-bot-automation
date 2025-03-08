import requests
from telegram.ext import Updater, CommandHandler
import openai
from bs4 import BeautifulSoup

# Configuration
TELEGRAM_TOKEN = "7418409797:AAEiO6OWdmjyIkjV89PTJDNaUc1uGGErrcY"
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# Scrape Betking Virtual Football League
def scrape_betking_vfl():
    url = "https://m.betking.com/virtual/league"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    matches = soup.find_all('div', {'data-testid': 'match-content'})
    match_data = []

    for match in matches:
        teams = match.find_all('div', {'class': 'home-team'})[0].text.strip() + " vs " + match.find_all('div', {'class': 'away-team'})[0].text.strip()
        odds = match.find_all('span', {'data-testid': 'match-odd-value'})
        if odds and len(odds) >= 2:
            match_data.append(f"{teams} | Over: {odds[0].text.strip()} | Under: {odds[1].text.strip()}")

    return "\n".join(match_data)

# GPT-4 Turbo Prediction
def get_predictions(matches):
    prompt = f"Predict matches likely to end over 3.5 goals based on these fixtures:\n{matches}"
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

# Telegram Bot Commands
def start(update, context):
    matches = scrape_betking_vfl()
    prediction = get_predictions(matches)
    update.message.reply_text(f"Today's Predictions:\n{prediction}")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
