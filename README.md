# Game Jam 0H 2025

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
sudo ufw allow 1883/tcp
sudo ufw reload
sudo ufw status
```




