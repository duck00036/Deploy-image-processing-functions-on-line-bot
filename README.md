# Deploy image processing functions on line bot
This chatbot is developed using the LINE Messaging API and deployed on AWS Lambda functions, leveraging the power of cloud computing to provide fast and reliable image processing capabilities. Its primary function is image processing, with the chatbot capable of performing three key functions:

1. **Searching for photos based on user-defined text, enabling users to quickly find the photos they need.**

2. **Classifying objects in user-sent photos and returning a processed photo along with a text description.**

3. **Cartoonizing people in user-sent photos and replying with a processed photo featuring cartoonized people.**

With its image processing techniques and cloud-based infrastructure, this chatbot provides users with a fun and engaging way to find or enhance their photos quickly and easily.

### Scan this QR code with LINE to add this chatbot account as a friend:

<img src="https://user-images.githubusercontent.com/48171500/232252124-6b00b82c-5811-42c7-9920-56fe8bdbbc93.png" width="200"/>

# User Interaction
## Start command
Send the command 茉茉", which is the name of the chatbot, and it will tell you what commands are available now.

<img src="https://user-images.githubusercontent.com/48171500/232253129-74a749f3-281c-44da-b23e-3178e7104340.jpg" width="350"/>

## Search command
Send the command "找圖", which means to search for photos, and it will ask what photos are you looking for?

Here I want to find a photo of a human, so I type in "Human" and it replies with a photo that includes a human.

But as soon as you enter the word that it can't find a related photo, it will reply with a message saying it can't find anything.

<img src="https://user-images.githubusercontent.com/48171500/232253136-433078b6-2cd3-4661-9fdd-e0bc8370bdc3.jpg" width="350"/>

## Classify command
Send the command "辨識", which means classification, it will ask you to send a photo for classification.

Now, send a photo with the object you want to classify and it will return the processed photo along with a text description.

<img src="https://user-images.githubusercontent.com/48171500/232253139-6a126245-8809-4e2f-8970-d5393a73521b.jpg" width="350"/>

But if there is nothing in the photo to classify, it will return the original photo and say it has nothing.

<img src="https://user-images.githubusercontent.com/48171500/232253142-1b3f049f-facb-41c3-9c34-e1c7e6746474.jpg" width="350"/>

If you're texting in classify mode, it will tell you to send a photo.

<img src="https://user-images.githubusercontent.com/48171500/232253146-3c4c2a93-74f1-4e90-afe7-e5e97e69178d.jpg" width="350"/>

## Cartoonize command
Send the command "卡通化", which means cartoonization, it will ask you to send a photo for cartoonization.

Now, send a photo with people and it will return a processed photo featuring cartoonized people.

But if there is no person in the photo, it will return the original photo.

<img src="https://user-images.githubusercontent.com/48171500/232253148-16158f72-93d8-4e0b-a07e-4e950ffbba54.jpg" width="350"/>

If you're texting in cartoonize mode, it will tell you to send a photo.

<img src="https://user-images.githubusercontent.com/48171500/232253150-3856d036-d19c-4d57-bc98-ac1112ad7208.jpg" width="350"/>

## Quiet commmand
Send the command "安靜" which means quiet and it will stay quiet until you send another command.

<img src="https://user-images.githubusercontent.com/48171500/232253152-a4a92fc8-f1fe-4b5c-bca2-52b68276d316.jpg" width="350"/>

# Architecture
![d8](https://user-images.githubusercontent.com/48171500/232245164-5402de9c-006e-43d0-97b3-696ed893d81e.PNG)

# Development
This chatbot is built on a serverless architecture using AWS services. Here are the different components and features that make up the chatbot:

## API Gateway:
* API Gateway enables easy management and monitoring of the chatbot's traffic and ensures that Lambda functions are only triggered when necessary.

The chatbot uses API Gateway to receive user messages from LINE Messaging API and trigger a Lambda function that processes the messages.

## Lambda functions:
* Lambda functions provide scalability and cost-effectiveness, as they only execute when needed and can easily scale up or down based on traffic.

The chatbot uses multiple Lambda functions to perform different tasks and handle user requests.

One Lambda function handles incoming messages and calls the corresponding function based on the user's current status.

Another Lambda function performs image classification when a user sends an image in classify mode.

A third Lambda function cartoonizes images when a user sends an image in cartoonize mode.

## DynamoDB:
* DynamoDB enables fast and reliable storage and retrieval of user data, even as the chatbot's user base grows.

The chatbot uses DynamoDB as its database to store user information and status.

## Photo search function:

The chatbot uses the Pixabay API to retrieve photos based on user-sent text.

When a user sends a message in search mode, the chatbot uses the Pixabay API to search for relevant images that match the user's request.

The chatbot then sends the user a photo that corresponds to their message.

## Classify function:

When a user sends an image in classify mode, the chatbot stores it in an S3 bucket and triggers a Lambda function for object classification.

The function uses the yolov8 model deployed in the container to classify the image and puts the processed image and text description into another S3 bucket.

The main Lambda function retrieves the result from the second S3 bucket and returns it to the user.

## Cartoonize function:

When a user sends an image in cartoonize mode, the chatbot stores it in an S3 bucket and triggers a Lambda function for image processing.

The function uses an ML model deployed in the container to cartoonize the image and puts the processed image into another S3 bucket.

The main Lambda function retrieves the result from the second S3 bucket and returns it to the user.

These are the links about [this ML model](https://github.com/duck00036/Cartoonize-people-in-image) and [model deployment](https://github.com/duck00036/Deploy-image-processing-ML-model-on-aws-lambda-via-container)

# Limitations
This line bot still has some limitations, as follows:

* The language used in the search mode is English when possible
* Photos returned in search mode may not always be what you expect
* Classification and cartoonization can take seconds of image processing
* Classify and cartoonize mode results may not always be what you expect
