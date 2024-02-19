# learntocode
A tutorial to help beginners learn coding through simple answers, powered by ChatGPT to create unique and interesting prompts.  
  
## TODO  
* Add rubber ducky decoding feature (popup modal, button similar to lightbulb, possibly on timer)
* ~~Migrate code execution engine to use multiprocessing~~  
* ~~Create prompts for 'data' section~~  
* Create prompts for 'conditionals' section  
* Create prompts for 'oop' section  
* ~~Add loading behavior to indicate that code is currently in execution~~  
* Add timeout to code to prevent hanging requests
    * ~~User facing timeout~~
    * Actual thread termination past timeout limit
* ~~Implement validation to screen for improper code and deliver message to user~~ 
* ~~Reformat tutorial page home and logo buttons for smaller screens (possibly into nav column)~~ 
    * Add and format button to clear exercises and reload open ai data (partially completed)
* Implement persistent state  
    * ~~Save OpenAI requests~~  
    * ~~Save user code~~  
* Possibly add page for brief introduction to concepts and have a link/button to show reference page 
    * Variables page  
    * Data page  
    * Conditionals page  
    * OOP page  
* ~~Add hover effect for prev/next buttons in exercise steps display~~    
* ~~Add opening screen requesting access code before allowing visitors in~~  
* ~~Strip HTML tags from gpt responses~~  
* Add actual testing framework for backend code  
* ~~Add login page which will be thrown up before each router action if user is not authenticated~~  
* ~~Set up basic mongo instance to store session data/tokens~~  
* Change passwords from hardcoded to queried from DB  
* Add token auth to every call  
  
## frontend 
npm install   
npm run dev  

## backend  
source ./env/Scripts/activate  
uvicorn main:app --reload  