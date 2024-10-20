# Overview
## Code Analysis and Application Security Testing Tool

CAAST.ai is an intelligent LLM based chatbot capable of accepting code in different languages which identifies potential vulnerabilities in your code along with its fixes.

<img width="1429" alt="image" src="https://github.com/user-attachments/assets/69577221-400f-45cf-8d95-81d2d0667aac">

# Working

- We used [reflex](https://reflex.dev/) to create the frontend.

  <img width="40" alt="image" src="https://github.com/user-attachments/assets/98d0bc10-1b84-437b-ba2c-437e71fbe066">

- The LLM used here is [geminiai](https://gemini.google.com/app).

  <img width="70" alt="image" src="https://github.com/user-attachments/assets/17613cce-39e6-4a5d-a2cd-e60bc6627762">


The system processes input based on whether the user provides a code snippet or a GitHub repository link.

If a code snippet is provided, the system utilizes a Large Language Model (LLM) to analyze the code and identify potential vulnerabilities. In the case of a GitHub repository link, the system retrieves the repository's code using Python's git library. The retrieved code is then processed by the LLM to detect vulnerabilities.

If neither a code snippet nor a repository link is given, the system functions as a standard generative AI chatbot, responding to general queries.

Additionally, users are given the option to clear previous chats, enhancing the functionality and user experience.

