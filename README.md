# lynx_ai

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
        f. Accept the recipe or Not
4. Keeping the record of used recipe on redis and update the ingredients available
5. Auto generate Shopping list after each meal prep
