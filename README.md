# learntocode
A tutorial to help beginners learn coding through simple answers, powered by ChatGPT to create unique and interesting prompts.  
  
## Local Development
### frontend 
npm install   
npm run dev  

### backend  
source ./env/Scripts/activate  
uvicorn main:app --reload  

## TODO  
### User impact features  
* Add rubber ducky decoding feature (popup modal, button similar to lightbulb, possibly on timer)
* Polish each page for grammar and clarity of explanation/examples  
* Improve performance in regards to memory, it seems webpage can be very RAM greedy especially if open for a while  
  
### Nice to haves  
* Add actual testing framework for backend code 
* Change passwords from hardcoded to queried from DB  
* Enforce code character length limit  
* Log key data points to Mongo in order to get a picture of overall performance  
    * Everytime a process is orphaned (include code blob)  
    * Response time for each API call, with endpoint labeling  
* Look to improve OpenAI query response times  
  
### Done    
* ~~Migrate code execution engine to use multiprocessing~~  
* ~~Create prompts for 'data' section~~  
* ~~Create prompts for 'conditionals' section~~  
* ~~Create prompts for 'oop' section~~  
* ~~Add loading behavior to indicate that code is currently in execution~~  
* ~~Add timeout to code to prevent hanging requests~~
    * ~~User facing timeout~~
    * ~~Actual process termination past timeout limit~~
* ~~Implement validation to screen for improper code and deliver message to user~~ 
* ~~Reformat tutorial page home and logo buttons for smaller screens (possibly into nav column)~~ 
    * ~~Add and format button to clear exercises and reload open ai data~~(REMOVED)  
* ~~Implement persistent state~~  
    * ~~Save OpenAI requests~~  
    * ~~Save user code~~  
* ~~Possibly add page for brief introduction to concepts and have a link/button to show reference page~~ 
    * ~~Variables page~~  
    * ~~Data page~~  
    * ~~Conditionals page~~  
    * ~~Loops page~~  
* ~~Add hover effect for prev/next buttons in exercise steps display~~    
* ~~Add opening screen requesting access code before allowing visitors in~~  
* ~~Strip HTML tags from gpt responses~~   
* ~~Add login page which will be thrown up before each router action if user is not authenticated~~  
* ~~Set up basic mongo instance to store session data/tokens~~  
* ~~Add token auth to every call~~  
* ~~Dockerize back-end~~  
* ~~Dockerize front-end~~  
* ~~Deploy front and back end to GCP~~   
* ~~Change to use learn to code designated keys rather than personal~~
* ~~Transition intro modal to be in-page~~
* ~~Implement token cache to speed up response times. Do in-mem per-server cache first, can switch to Redis or similar if necessary later.~~  
* ~~Need to add NGINX configuration and apply to dockerfile for cloud hosting~~
* ~~Create env file in dockerfile~~  
* ~~Check caching behavior when running on docker/nginx~~  
* ~~Refactor backend code to be more neatly packed into modular classes/files~~  
