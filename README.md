# lynx_ai

Cooking dish suggestions from an image of Grocery Cash memo and stored food. Dish suggestions according to user needs. 

Advantage: 
    1. Pinpoint advertisement 


Challenges:
    1. Data 
Questions/Issues:
    1.  


Features: 
Shopping list extraction
Save item and quantity in database (Redis)  
Generate Prompt for Open AI API:
All kitchen items available → keeping the track in Redis, generating prompt from taking the data from Redis and tracking the last activity
Type of cuisine (possible)
Nutrition value (healthy or tasty or balanced)
Number of portion (sudden guest)
Vacation/Weekday/Busy Day → Preparation time for using in prompt
Accept the recipe or Not
Keeping the record of used recipe on redis and update the ingredients available
Auto generate Shopping list after each meal prep
