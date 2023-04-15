# Import necessary libraries and packages
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError, InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, FollowEvent
import requests, traceback, logging, boto3, json, os, random, time

# Create S3 client and DynamoDB resource
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Get the name of the DynamoDB table from environment variable
table_name = os.getenv('LINE_BOT_TABLE', None)

# Access the DynamoDB table
table = dynamodb.Table(table_name)

# Get channel secret and channel access token from environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

# Create LineBotApi object and WebhookHandler object
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO) 

def lambda_handler(event, context):

    # Define function to get message information (type and ID)
    def get_message_info(m_event):
        m_tpye = m_event.source.type
        if m_tpye == "user":
            return m_tpye, m_event.source.user_id
        elif m_tpye == "group":
            return m_tpye, m_event.source.group_id
        else:
            return "notype", "noid"
    
    # Define function to update trigger count in DynamoDB
    def update_trigger_count(m_id):
        table.update_item(
            Key={"user_id": m_id},
            UpdateExpression="set trigger_count = trigger_count + :n",
            ExpressionAttributeValues={":n": 1},
            ReturnValues="UPDATED_NEW"
        )
    
    # Define function to append user data to DynamoDB
    def append_data(m_id):
        table.put_item(
            Item={
                "user_id": m_id,
                "status": "offline",
                "trigger_count": 0
            }
        )
    
    # Define function to update user status in DynamoDB
    def update_status(m_id, text, m_event):
        # dictionary of status change commands and their corresponding status values
        command2mode = {"茉茉": "online", "安靜": "offline", "找圖": "search_mode", "辨識": "classify_mode", "卡通化": "cartoonize_mode"}
        
        if text not in command2mode:
            return False # if not a status change command, return False
        
        else:
            table.update_item(
                Key={"user_id": m_id},
                UpdateExpression="set #name = :n",
                ExpressionAttributeNames={"#name": "status"},
                ExpressionAttributeValues={":n": command2mode[text]},
                ReturnValues="UPDATED_NEW"
            )
            logger.info(f'change status to {command2mode[text]}')
            
            # reply to the user with the appropriate message for the command
            start_message = "茉茉目前有四個指令可以用:\n\n"\
                            "1.找圖:輸入關鍵字，幫你找圖\n\n"\
                            "2.辨識:上傳圖片，幫你辨識\n\n"\
                            "3.卡通化:將照片中的人卡通化\n\n"\
                            "4.安靜:茉茉會安靜，直到你叫他\n\n"\
                            "註:為保持群組內的清靜，在群組內每呼叫一個指令，只會執行一次命令"           
            classify_message = "把要辨識的圖傳上來吧!"
            search_message = "要找什麼圖呢? 建議使用英文喔"
            cartoonize_message = "把要將人物卡通化的圖傳上來吧!"
            offline_message = "了解!"
                             
            command2message = {"茉茉": start_message, "辨識": classify_message, "找圖": search_message, "卡通化": cartoonize_message, "安靜": offline_message}
            line_bot_api.reply_message(m_event.reply_token,TextSendMessage(text=command2message[text]))
            return True
    
    # Define function to get user status from DynamoDB
    def get_status(m_id):
        user_data = table.get_item(Key={'user_id': m_id})
        if "Item" in user_data:
            return user_data["Item"]["status"]
        
        # if user's data not exist, append user's data to DynamoDB
        else:
            append_data(m_id)
            return "offline"
    
    # Define function to set the status of a user to offline.
    def set_offline(m_id):
        table.update_item(
            Key={"user_id": m_id},
            UpdateExpression="set #name = :n",
            ExpressionAttributeNames={"#name": "status"},
            ExpressionAttributeValues={":n": "offline"},
            ReturnValues="UPDATED_NEW"
        )
    
    # Handler for Text messages
    @handler.add(MessageEvent, message=TextMessage)
    def handle_text_message(event):
        # Get message info
        m_type, m_id = get_message_info(event)
        logger.info(f'receive a Text message from {m_type} {m_id}')
        
        # Increment the user's trigger count
        update_trigger_count(m_id)
    
        # Get the message text and current status
        messageText = event.message.text
        status = get_status(m_id)
        logger.info(f'current status is : {status}')
    
        # Confirm if the message is a state change command
        if not update_status(m_id, messageText, event):
            
            # Handle messages based on status
            if status == "search_mode":
                
                # Get Pixabay API's key from environment variables
                pixabay_key = os.getenv('pixabay_key', None)
                
                # Search for images using Pixabay API
                url = "https://pixabay.com/api/?key=" + pixabay_key + "&q=" + messageText + "&lang=zh&image_type=photo"
                response = requests.get(url)
                data_json = response.json()
                
                # Check if any images were found
                if not data_json["hits"]:
                    # If not found, send a message to tell the user
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='好像找不到相關圖片欸...'))
                    logger.info('Can not find suitable image')
                
                else:
                    # If images were found, send a randomly selected image to the user
                    respone_url = random.choice(data_json["hits"])["webformatURL"]
                    img_message = ImageSendMessage(original_content_url=respone_url, preview_image_url=respone_url)
                    line_bot_api.reply_message(event.reply_token,img_message)
                    logger.info(f'Image has been send to {m_type} {m_id} !')
                    
                    # If the message was sent in a group chat, set the bot to offline mode
                    if m_type == "group":
                        set_offline(m_id)
    
            if status == "classify_mode":
                # Ask user to send an image
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text='現在是辨識模式，傳圖上來吧'))
                logger.info(f'get text in {status}')
    
            if status == "cartoonize_mode":
                # Ask user to send an image
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text='現在是卡通化模式，傳圖上來吧'))
                logger.info(f'get text in {status}')


    # handler for Image messages
    @handler.add(MessageEvent, message=ImageMessage)
    def handle_image_message(event):
        # Get message info
        m_type, m_id = get_message_info(event)
        logger.info(f'receive a Image message from {m_type} {m_id}')
        
        # Increment the user's trigger count
        update_trigger_count(m_id)
        
        # Get current status
        status = get_status(m_id)
        logger.info(f'current status is : {status}')
        
        # Handle messages based on status
        if status == "classify_mode" or status == "cartoonize_mode":
            
            # Get the ID and content of the image message
            message_id = event.message.id
            message_content = line_bot_api.get_message_content(message_id)
            
            # Save the image to a file
            path = '/tmp/' + message_id + '.jpg'
            with open(path, 'wb') as fd:
                for chunk in message_content.iter_content():
                    fd.write(chunk)
    
            # Get the output S3 bucket information from environment variables
            image_bucket = os.getenv('image_bucket', None)
            image_bucket_path = os.getenv('image_bucket_path', None)
            
            # Create an empty list to store the bot's reply messages
            reply = []
            
            if status == "classify_mode":
                
                # Get the input S3 bucket information from environment variables
                classify_bucket = os.getenv('classify_bucket', None)
                
                # Upload the image to the S3 bucket for the classification model
                s3.upload_file(path, classify_bucket, message_id + '.jpg')
                logger.info('Image has been sent to the classify model !')
                
                # Wait until the image processing is completed
                while True:
                    try:
                        s3.download_file(image_bucket, message_id + '.txt', '/tmp/output.txt')
                        logger.info('Image processing completed !')
                        s3.delete_object(Bucket=classify_bucket, Key=message_id + '.jpg')
                        break
                    except:
                        logger.info('Image still processing, Waiting 1 second...')
                        time.sleep(1)
        
                # Read the output text file from the classification model and format the results as a string
                path = '/tmp/output.txt'
                string = 'there are\n'
                with open(path) as f:
                    count = 0
                    for line in f.readlines():
                        string += line
                        count += 1
                if count == 0:
                    string += 'nothing\n'
                string += 'in the photo'
                
                # Create a TextSendMessage object with the results and add it to the bot's reply messages
                txt_msg = TextSendMessage(text=string)
                reply.append(txt_msg)
            
            if status == "cartoonize_mode":
                
                # Get the input S3 bucket information from environment variables
                cartoonize_bucket = os.getenv('cartoonize_bucket', None)
                
                # Upload the image to the S3 bucket for the cartoonization model
                s3.upload_file(path, cartoonize_bucket, message_id + '.jpg')
                logger.info('Image has been sent to the cartoonize model !')
                
                # Wait until the image processing is completed
                while True:
                    try:
                        s3.head_object(Bucket=image_bucket, Key=message_id + '.jpg')
                        logger.info('Image processing completed !')
                        s3.delete_object(Bucket=cartoonize_bucket, Key=message_id + '.jpg')
                        break
                    except:
                        logger.info('Image still processing, Waiting 1 second...')
                        time.sleep(1)
            
            # Create a ImageSendMessage object with the result and add it to the bot's reply messages
            img_url = image_bucket_path + message_id + '.jpg'
            send_img = ImageSendMessage(original_content_url=img_url, preview_image_url=img_url)
            reply.append(send_img)
            
            # Reply to the user with the list of replies
            line_bot_api.reply_message(event.reply_token,reply)
            logger.info(f'Image has been send to {m_type} {m_id} !')
            
            # If the message was sent in a group chat, set the bot to offline mode
            if m_type == "group":
                set_offline(m_id)
    
    # Handle for Follow events when a user adds the bot as a friend             
    @handler.add(FollowEvent)  
    def handle_follow(event):
        # Get user's ID)
        userId = event.source.user_id
        logger.info (f'Received FollowEvent event {userId}')
        
        # Append user's data to DynamoDB
        append_data(userId)
        
        # Reply to user and welcome him/her
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='HELLO! 我是茉茉\n\n輸入"茉茉"了解可以使用的指令吧!'))      
 
    try:
        # Retrieve the signature and body from the webhook request
        signature = event['headers']['x-line-signature']
        body = event['body']
        
        # Handle the event body with the provided signature      
        handler.handle(body, signature)
    
    except InvalidSignatureError:
        # If the signature doesn't match, return an error
        return {
            'statusCode': 400,
            'body': json.dumps('InvalidSignature') }        
    
    except LineBotApiError as e:
        # If there is an error calling the LINE Messaging API, log the details and return an error
        logger.error(f'Unexpected error occurred while calling LINE Messaging API: {e.message}')
        for m in e.error.details:
            logger.error(f'{m.property}: {m.message}')
        return {
            'statusCode': 400,
            'body': json.dumps(traceback.format_exc()) }
    
    # If everything goes well, return an OK status
    return {
        'statusCode': 200,
        'body': json.dumps('OK')}