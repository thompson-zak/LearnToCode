# learntocode
A tutorial to help beginners learn coding through simple answers, powered by ChatGPT to create unique and interesting prompts.  
  
## TODO  
* Add rubber ducky decoding feature (popup modal, button similar to lightbulb, possibly on timer)
* ~~Migrate code execution engine to use multiprocessing~~  
* Create prompts for 'data' section  
* Create prompts for 'conditionals' section  
* Create prompts for 'oop' section  
* ~~Add loading behavior to indicate that code is currently in execution~~  
* Add timeout to code to prevent hanging requests  
* ~~Implement validation to screen for improper code and deliver message to user~~ 
* Reformat tutorial page home and logo buttons for smaller screens (possibly into nav column)  
* Implement persistent state so that OpenAI is called only once and any code written is kept on reload   
  
## frontend 
npm install   
npm run dev  

## backend  
source ./env/Scripts/activate  
uvicorn main:app --reload  