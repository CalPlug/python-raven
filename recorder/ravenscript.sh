#! /bin/bash


while true
do
    curl https://www.google.com >/dev/null 2>&1

    if [[ $? -eq 0 ]]; then
        echo "Connected to Internet. Starting Python script!";
        sleep 1;

        tmux new-session -s "smartmeter2" -n script -d
        tmux send-keys -t "smartmeter2" "python3 /home/calplug/smartmeter/serverMqttR.py" C-m 

        echo "Successfully started Python script under tmux session 'smartmeter2'";
        break
    else 
        echo "Not connected to the internet. Retrying in 5 seconds...";
        sleep 5;
    fi

done