# Game Jam 0H 2025

Jam: https://itch.io/jam/zero-hour-game-jam-2025  
Submission: https://eloistree.itch.io/pico-w-ovni  
Fail: https://itch.io/jam/zero-hour-game-jam-2025/topic/5461595/post-your-missed-submissions-here  
Post-Mortem: https://youtu.be/rNvknFmVE0s   

[<img width="1067" height="596" alt="image" src="https://github.com/user-attachments/assets/376d988d-42d7-4949-b760-24f83ccaf93b" />](https://youtu.be/rNvknFmVE0s)  
https://youtu.be/rNvknFmVE0s


> I want to make the 0H game jam but some spec of the concept I want to try need UDP and MicroPython

So I will prepare the network part:
- https://circuitpython.org/board/raspberry_pi_pico2_w/


```
sudo apt update && sudo apt upgrade -y 
sudo apt install -y mosquitto mosquitto-clients
```


```
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
sudo systemctl status mosquitto
```

```

sudo apt install ufw
sudo ufw enable
sudo ufw reload
sudo ufw allow 1883/tcp
sudo ufw allow 1883/udp
sudo ufw allow 7000/udp
sudo ufw allow 3615/udp
sudo ufw reload
sudo ufw status

```


```
sudo systemctl edit mosquitto

[Service]
Restart=always
RestartSec=5

sudo systemctl daemon-reload
sudo systemctl restart mosquitto
systemctl cat mosquitto

```


