# chat-on-flask
Simple application for chatting on flask with socket io and postgres database.
This is just for template purpose.


## Explaination about the Libraries used
SocketIO library enables BiDirectional, Realtime and event based communication between the client and the server. Here it Consists of:
* flask-socketio
* javascript client side library

It working by trying to create a websocket connection, which provides full-duplex and low-latency channel between client and server, if possible or does HTTP longpolling if websocket connection is not connected.

### How does this program work?

#### When joined from the client side
When Client Side is opened it connects to the server through a websocket and creates a event called `joined_room` sending data such as username and room number with it. While using on another platform on connection the cilent should create this event with necessary data passed. When making a proper chatting application two usernames needs to be sent. When this event is created in backend serverside there is a event handler for this which is inside `socketio_on()` decorator. Function inside it gets the data sent from the client side and then processes it such as creating room for the users from the database, storing information who joined the database etc.

In the context of this small project, Roomid and user joined are added to the database and it is checked if that room is empty or not. If the room is empty, Serverside creates `join_room_announcement` event and if the room is not empty i.e. has chat history then it creates `rejoin_room` event and fetches all the chat history from the database and sends it to the client. The `join_room_announcement` event can be used as a trigger that the message was opened. In this project, it is used to show that a person is online for simplicity. The `rejoin_room` event takes all of the data send from the server side and then displays it in proper format. It can be used as normal history displaying with trigger that the message was opened. Here on this program, This event also updates the scroll so that it shows the bottom part i.e. the latest part of the message.


#### When sending messages

When Sending messsage, client side sends message through the submit button. By default, submit button does a http POST or GET request. But since we've already connected to the server throught the socket it is not necessary. Hence onsubmit a function is executed which stops the default behavior of the submit button and using `getElementById()` of javascript takes the messages written checks if it is empty or not. If it is empty then it does nothing else it creates a event `send_message` with the datas of username, room number and the message. When that event is created in server side handle_send_message_event() function is triggered which stores messages in the database then creates an event called `recieve_message` which then sends the messages to everyone in the same room added as a parameter of `socket.emit()` function.

This `recieve_message` event is handled on client side by a function which creates a new node inside the chatting area and then inserts a new DIV with message element inside it. It then updates the scroll to show the latest message.

** This is all of the work done inorder to make the chatting feature work. **

### Typing status

This is an optional feature added to show the typing status while sending message. In javascript there is a feature called on keypress/keydown and keyup. In this case, we are using keyup since we have to take the data too. If there is something written i.e. content is more than 1 then typing status is shown and then flag is changed so that if message is cleared and then again reaches 1 then it doesn't again show the typing status. If the message is sent or message is cleared then flag is rest and typing status is removed. Typing status once creates an event named `typing_status`. This event is handled by `typing_status_handler()` function which then creates an event named `typing_on`  broadcasting to everyone excluding self i.e. if I'm typing then that typing won't be shown for me but will be shown for everyone on that room. That event is handled on client side using function to display typing status.
