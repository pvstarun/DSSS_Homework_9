from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import torch
from transformers import pipeline

BOT_TOKEN = "7828989295:AAEK3h3Ff7tTWrMRCbMrFO0ad4a3vzV6b7I"

pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="auto")

def AItext(message):
    
    messages = [
        
        {"role": "user", "content": message},
    ]
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    return(outputs[0]["generated_text"])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I am your AI bot. Send me a message!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    Answer = AItext(user_message)
    Answer = Answer.replace("<|user|>\n" + user_message + "</s>\n<|assistant|>\n", "")
    print(Answer)
    await update.message.reply_text(Answer)


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

