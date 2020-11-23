# agar.io clone game with multiplayer

https://github.com/introduction-to-gamedev/assignments/blob/master/2020/assignment_3.md

### Using Python 3.8.1

Create virtualenv and activate it

Install deps:

    pip install -r requirements.txt
    
If have problems on macOS with socket error: Message too long, try this command:

    sudo sysctl -w net.inet.udp.maxdgram=65535
    
To run server:

    python server.py
    
To run client:

    python client.py
