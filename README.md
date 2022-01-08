# Bolster Web Scrapping Assignment

List of dependencies (python libraries) :-
  1) Playwright for Python
  2) Beautiful Soup

How to run program :-
1) Install all the packages required
2) Execute server.py file using the command :- python server.py
3) Send a CURL Request using :- 
    curl -X POST http://localhost:32002 -H 'Content-Type: application/json' -d '{"url":"http://mgttcollege.com"}'
   One can give the URL of his choice in the url param
4) After complete execution, it will return a complete status.
