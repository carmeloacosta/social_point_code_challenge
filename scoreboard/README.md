# SOCIAL POINT CODE CHALLENGE : SCOREBOARD

 Runs a scoreboard that can be accessed using an HTTP REST API.  

# Installation

 From the same directory than this README.md file execute the following:
 
    python3 -m pip install -r requirements.txt

# Run the application

 From the root directory (where is located the main.py file) execute:

    python3 -m main.py

 Make sure that the constant DEBUG is set to False in the file constants.py
 
 Additionally, take into account that both the IPv4 address and port on which will be launched the HTTP API
 is set in the constants.py file. 
 The application is comprised of clients and server processes, that communicates using ZMQ sockets. Each client
 exposes a copy of the HTTP API in the same IPv4 address, with ports ranging from the one specified in constants.py
 to +NUM_CLIENTS (as configured in conf.py). That is, a 2-clients configuration, with configured DEFAULT_PORT equal
 to 8000, will expose the HTTP API in both 8000 and 8001 ports. This application is intended to be used in 
 conjunction with an Nginx reverse proxy, to expose the HTTP REST API on a single IP:port using its load balancing
 capabilities.  
 
# Design & Implementation considerations

 The use of Python3 as programming language is aimed to reduce development time of this time restricted Code 
 Challenge, since it is the one that currently allows me to code faster. However, Python 3 would not be the choice
 for a real production scoreboard implementation. See file scoreboard_wrapper.py for a reasoned explanation such as
 for deeper design considerations. 
 
# Using the application

 Simply make requests to the exposed HTTP REST API.
 
# HTTP REST API

    PUT /score

 Send a new score value. Both absolute and relative values accepted.

    Body: 
            {"user": <user_id>, "total": <total_score>} or {"user": <user_id>, "score": <relative_score>} 

    Examples:
    
            {"user": 123, "total": 250}
            {"user": 456, "score": "+10"}
            {"user": 789, "score": "-115"}

    Response:
    
            {"user": <user_id>, "total": <total_score>}
        
    
---------------------------------    
    GET /top/<top_size>
    
 Retrieves the Top <top_size> according to current scores.  

    Examples:
    
            /top/100  <- The Top100
            /top/500  <- The Top500

    Response:
    
            [{"user": <user_id_top1>, "total": <total_score>}, {"user": <user_id_top2>, "total": <total_score>}, 
              ... {"user": <user_id_topN>, "total": <total_score>}]

            with N == top_size


---------------------------------
    GET /top/<ranking_position>/<scope_size>

 Retrieves the relative Top around the specified ranking position. Let be X the user that occupies the specified
 ranking position, the   

    Examples:
    
            /top/50/1  <- [{"user": 12, "total": 100}, {"user": 23, "total": 96}, {"user": 111, "total": 89}]
                                  Position 49th             Position 50th                Position 51th
            
            /top/3/2   <- [{"user": 3, "total": 1000}, {"user": 7, "total": 969}, {"user": 9, "total": 898},
                           {"user": 13, "total": 777}, {"user": 17, "total": 696} ]
                                  Position 1st             Position 2nd                Position 3rd
                                  Position 4th             Position 5th

    Response:
    
            [{"user": <user_id_topN-scope_size>, "total": <total_score>}, ...  
             {"user": <user_id_topN+scope_size>, "total": <total_score>}]

            with N == ranking_position
    

# Run a single test

 From the root directory (where is located the tests folder) execute:

    python3 -m unittest tests.<test_filename>.<test_classname>.<test_name>

 Make sure that the constant DEBUG is set to True in the file constants.py

# Run a single test

 From the root directory (where is located the tests folder) execute:

    python3 -m unittest tests.<test_filename>.<test_classname>.<test_name>

    Example:

    python3 -m unittest tests.tests_scoreboard_wrapper.TestScoreboardWrapper.test_empty_creation_ok
 
 Make sure that the constant DEBUG is set to True in the file constants.py