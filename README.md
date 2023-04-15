# Deploy image processing functions on line bot
This chatbot is developed using the LINE Messaging API and deployed on AWS Lambda functions, leveraging the power of cloud computing to provide fast and reliable image processing capabilities. Its primary function is image processing, with the chatbot capable of performing three key functions:

1. **Searching for photos based on user-defined text, enabling users to quickly find the photos they need.**

2. **Classifying objects in user-sent photos and returning a processed photo along with a text description.**

3. **Cartoonizing people in user-sent photos and replying with a processed photo featuring cartoonized people.**

With its image processing techniques and cloud-based infrastructure, this chatbot provides users with a fun and engaging way to find or enhance their photos quickly and easily.

### Scan this QR code with LINE to add this chatbot account as a friend:

<img src="https://user-images.githubusercontent.com/48171500/232252124-6b00b82c-5811-42c7-9920-56fe8bdbbc93.png" width="200"/>

# Architecture
![d8](https://user-images.githubusercontent.com/48171500/232245164-5402de9c-006e-43d0-97b3-696ed893d81e.PNG)

# User Interaction
## Start command
**Send the command 茉茉", which is the name of the chatbot, and it will tell you what commands are available now.**

<img src="https://user-images.githubusercontent.com/48171500/232253129-74a749f3-281c-44da-b23e-3178e7104340.jpg" width="500"/>

## Search command
**Send the command "找圖", which means to search for photos, and it will ask what photos are you looking for?**

**Here I want to find a photo of a human, so I type in "Human" and it replies with a photo that includes a human.**

**But as soon as you enter the word that it can't find a related photo, it will reply with a message saying it can't find anything.**

<img src="https://user-images.githubusercontent.com/48171500/232253136-433078b6-2cd3-4661-9fdd-e0bc8370bdc3.jpg" width="500"/>

## Classify command
**Send the command "辨識", which means classification, it will ask you to send a photo for classification.**

**Now, send a photo with the object you want to classify and it will return the processed photo along with a text description.**

<img src="https://user-images.githubusercontent.com/48171500/232253139-6a126245-8809-4e2f-8970-d5393a73521b.jpg" width="500"/>

**But if there is nothing in the photo to classify, it will return the original photo and say it has nothing.**

<img src="https://user-images.githubusercontent.com/48171500/232253142-1b3f049f-facb-41c3-9c34-e1c7e6746474.jpg" width="500"/>

**If you're texting in classify mode, it will tell you to send a photo.**

<img src="https://user-images.githubusercontent.com/48171500/232253146-3c4c2a93-74f1-4e90-afe7-e5e97e69178d.jpg" width="500"/>

## Cartoonize command
**Send the command "卡通化", which means cartoonization, it will ask you to send a photo for cartoonization.**

**Now, send a photo with people and it will return a processed photo featuring cartoonized people.**

**But if there is no person in the photo, it will return the original photo.**

<img src="https://user-images.githubusercontent.com/48171500/232253148-16158f72-93d8-4e0b-a07e-4e950ffbba54.jpg" width="500"/>

**If you're texting in cartoonize mode, it will tell you to send a photo.**

<img src="https://user-images.githubusercontent.com/48171500/232253150-3856d036-d19c-4d57-bc98-ac1112ad7208.jpg" width="500"/>

## Quiet commmand
**Send the command "安靜" which means quiet and it will stay quiet until you send another command.**

<img src="https://user-images.githubusercontent.com/48171500/232253152-a4a92fc8-f1fe-4b5c-bca2-52b68276d316.jpg" width="500"/>


# Development

# Limitations
Privacy & Security
Troubleshooting
Roadmap
Support & Contact
