# discord.pyの読み込み
import discord
import requests
import transfer_notion
from pprint import pprint


#　discord botのアクセストークンを記入する
TOKEN = ''
#　botが発言するdiscordチャンネルのID（botチャンネルなど）を記入する
CHANNEL_ID = ''

# 接続に必要なオブジェクトを生成
client = discord.Client()


# 起動時にbotが挨拶するプログラム
async def greet():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('Notion: Q&A転送botが起動しました。')


@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('Discordに正常にログインできました')
    await greet()


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # Botのメッセージは除外
    if message.author.bot:
        return

    # 条件に当てはまるメッセージかチェックし正しい場合は返す
    def check(msg):
        return msg.author == message.author

    # /getとチャンネル上に打ち込むとBotが反応を示す
    if message.content.startswith("/get"):

        # /getと打ち込まれたチャンネル上に下記の文章を出力
        await message.channel.send("Notionに作成するQ&Aのタイトルを入力してください")

        # ユーザーからのメッセージを待つ
        page_title = await client.wait_for("message", check=check)

        # メッセージを打ち込まれたのを確認すると下記の文章を出力

        await message.channel.send("質問メッセージのIDを入力してください。")

        # ユーザーからのメッセージを待つ
        question_id = await client.wait_for("message", check=check)

        # メッセージを打ち込まれたのを確認すると下記の文章を出力

        await message.channel.send("解答メッセージのIDを入力してください。")

        # ユーザーからのメッセージを待つ
        answer_id = await client.wait_for("message", check=check)

        # メッセージを打ち込まれたのを確認すると下記の文章を出力
        await message.channel.send("転送するQ&Aはこちらになります")

        #チャンネルからメッセージを取得
        qa_channel = message.channel
        get_question_by_id = await qa_channel.fetch_message(question_id.content)
        get_answer_by_id = await qa_channel.fetch_message(answer_id.content)

        print('作成された記事のタイトル：', page_title.content)
        print('転送内容1：', get_question_by_id.content)
        print('転送内容2：', get_answer_by_id.content)

        # 取得したメッセージを書き込まれたチャンネルへ送信
        await message.channel.send(page_title.content)
        await message.channel.send(get_question_by_id.content)
        await message.channel.send(get_answer_by_id.content)

        # 取得したメッセージを書き込まれたチャンネルへ送信
        transfer_notion.send_to_notion(page_title.content, get_question_by_id.content, get_answer_by_id.content, get_question_by_id.author.name, get_answer_by_id.author.name, get_question_by_id.created_at)
        # 転送したことを伝えるメッセージ
        await message.channel.send("NotionにQ&Aの転送が完了しました。")

# botの起動とDiscordサーバーへの接続
client.run(TOKEN)

