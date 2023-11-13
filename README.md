# Introduction 
Project Gutenverse is a system that takes plaintext stories as input and analyzes them to identify distinct scenes and produce metadata about each scene.   The analysis metadata is then used as inputs for the generative AI pipeline to produce a 3D world for a virtual storybook.

# Getting Started
 - Install VSCode or your preferred Python/Javascript editor
 - Install [Python](https://www.python.org/?downloads)
 - Install [NodeJS](https://nodejs.org/en/download)
 - Run npm install in /client
 - Run pip install in the root folder of the repository
 - Add your OpenAI key to an environment variable named OpenAIApiKey

# Build and Test

To test the client - run npm start in /client

To test the server - run python app.py (starts the web services)

To connect to the database - add a MongoDBConnectionString environment variable
