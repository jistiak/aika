## AI Cook

### Introduction 
We have built a solution to make grocery shopping and cooking more efficient with the help of AI. The project's goal is to save time as well as assist in quality meal preparation. The user will also be able to track his/her grocery inventory and consumption trend. 


## Details of the project: 

### User Inputs (AI Chef): 

1. The user will first scan the cash memo       obtained by shopping at a grocery store. The items from the memo will be added to the inventory list as data.  

2. Next from the AI Chef option in the UI the user can input which 'Type of Cuisine', 'Type of Diet', 'Number of Portions' and 'Maximum Preparation Time' for his/her next meal.

3. Harnessing the power of AI the application will generate a dish to cook along with a list of required ingredients needed from the inventory and the process of cooking.

4. The user can either select the suggested meal or move to the next suggestion. If the user cooks a generated meal the inventory will be adjusted accordingly. 

5. The application will save the recipes that the user cooks for future reference.

6. The application will also be able to notify the user when it is time to go shopping again. It can also generate a list of grocery items that are running low in the inventory. 


### Features: 

1. Shopping list extraction
2. Save item and quantity in a Redis database   
3. Generate Prompt for Open AI API:
        a. All kitchen items available → keeping the track in Redis, generating prompt from taking the data from Redis and tracking the last activity
        b. Type of cuisine (possible)
        c. Nutrition value (healthy or tasty or balanced)
        d. Number of portion (sudden guest)
        e. Vacation/Weekday/Busy Day → Preparation time for using in prompt
4. Accept the recipe or Not
5. Keeping the record of used recipe on redis and update the ingredients available
6. Auto generate Shopping list after each meal prep



Cooking dish suggestions from an image of Grocery Cash memo and stored food. Dish suggestions according to user needs. 

Advantage: 
    1. Pinpoint advertisement 


Challenges:
    1. Data

Questions/Issues:
    1.  

## OpenAI Stack Hack
This project was built for OpenAI Stack Hack (Create Applications Using Generative AI!) which was held from 24th February to 3rd March 2023. 

Here is a link to our pitch presentation: 