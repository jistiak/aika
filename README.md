## AI Cook
We have built a solution to make grocery shopping and cooking more efficient with the help of AI. The project's goal is to save time as well as assist in quality meal prep. The user will also be able to track his/her grocery inventory and consumption trend. 



Cooking dish suggestions from an image of Grocery Cash memo and stored food. Dish suggestions according to user needs. 

Advantage: 
    1. Pinpoint advertisement 


Challenges:
    1. Data

Questions/Issues:
    1.  


Features: 
1. Shopping list extraction
2. Save item and quantity in database (Redis)  
3. Generate Prompt for Open AI API:
        a. All kitchen items available → keeping the track in Redis, generating prompt from taking the data from Redis and tracking the last activity
        b. Type of cuisine (possible)
        c. Nutrition value (healthy or tasty or balanced)
        d. Number of portion (sudden guest)
        e. Vacation/Weekday/Busy Day → Preparation time for using in prompt
4. Accept the recipe or Not
5. Keeping the record of used recipe on redis and update the ingredients available
6. Auto generate Shopping list after each meal prep
