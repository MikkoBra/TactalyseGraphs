# Tactalyse Graph API

Setting up the api (assuming Docker Desktop is installed):
1) Run docker desktop
2) In the root directory (TwitterGraphs or whatever you called it locally), run "docker build -t test-image ." in your terminal.
3) Run "docker run -p 5001:5001 test-image". The api will now be available on localhost:5001/graph. See app.py for the endpoints and HTTP verbs.

Don't rely on code comments, they have not been updated.

Use these parameters to test line plot at /graph/line:  
"league": "eng2"  
"player": "I. Sarr" (capital i)  
"stat": "Interceptions"

Use these parameters to test radar chart at /graph/radar:  
"league": "eng2"  
"player": "I. Sarr"

