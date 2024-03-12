Download Rasa

Open two terminals A and B

In terminal A 
run the command: rasa run --cors "*" --enable-api OR python -m rasa run --cors "*" --enable-api
It will say that the model is running or a similar message

In terminal B 
run the command: rasa run actions or python -m rasa run actions
this will show where the endpoints are.

In another terminal change the directory to RasaUI 'cd RasaUI'
run npm start

