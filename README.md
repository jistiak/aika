## AI Cook

### Introduction 
We have developed an AI-powered solution to streamline grocery shopping and cooking, with the aim of making meal preparation both more efficient and higher in quality. Our application allows users to track their grocery inventory and consumption trends, and offers recipe suggestions based on their preferences and needs.

## Details of the project: 

### AI Chef UI: 

1. The user will first scan the cash memo obtained by shopping at a grocery store.The application will extract relevant information, and the items from the memo will be automatically added to the inventory list as data.

2. Next, from the AI Chef option in the UI the user can input various parameters, including "Type of Cuisine," "Type of Diet," "Number of Portions" and "Maximum Preparation Time," to generate customized recipe suggestions.

3. The system will leverage AI-powered algorithms to analyze the user's input and generate a dish to cook. The application will also provide a list of required ingredients from the inventory and the cooking procedure.

4. The user will have the option to accept or reject the recipe suggestion. If the user selects and prepares a generated recipe, the inventory will be automatically be updated based on the amount of ingredients used. 

5. The application will save the recipes that the user cooks for future reference.

6. The application will utilize predictive analytics to track the user's grocery consumption patterns and notify the user when it is time to go shopping again. The application can also generate a list of grocery items that are running low in the inventory, allowing the user to replenish their supplies proactively. 

[User Interface: AI Chef](assets\ai_chef_ui.jpg)

### Features: 

1. Shopping list extraction
2. Save grocery item and quantity in a Redis database   
3. Generate Prompt for OpenAI API:
4. User may Accept or Decline the recipe
5. Keeping the record of used grocery items and update the inventory available
6. Generate Shopping list


## OpenAI Stack Hack
This project was built for OpenAI Stack Hack (Create Applications Using Generative AI!) which was held from 24th February to 3rd March 2023. 

Here is a link to our pitch presentation: 