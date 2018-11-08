#! /bin/bash


while true
do
    curl https://www.google.com >/dev/null 2>&1

    if [[ $? -eq 0 ]]; then
        echo "Connected to Internet. Starting Python script!";
        sleep 1;

        tmux new-session -s "ravensession" -n script -d
        tmux send-keys -t "ravensession" "cd ~/python-raven/reporter" C-m 
        tmux send-keys -t "ravensession" "python3 direct_mqtt_run.py -usemac" C-m 

        echo "Successfully started Python script under tmux session 'ravensession'";
        break
    else 
        echo "Not connected to the internet. Retrying in 5 seconds...";
        sleep 5;
    fi

done