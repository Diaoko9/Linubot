# Linubot

**Linubot** is a containerized ROS 2 (Jazzy) differential drive robotics project designed for the Raspberry Pi. It provides real-time motor control via a Bluetooth PS4 controller, interfacing with an L293D motor driver.

To ensure robust deployment on edge devices, the entire ROS 2 workspace, including `joy_node` dependencies and Python hardware libraries, is packaged as a strict-confined Linux Snap.

## 🚀 Features

* **ROS 2 Jazzy Integration:** Utilizes standard `sensor_msgs/Joy` topics for teleoperation.
* **Snapcraft Deployment:** Fully containerized environment ensuring dependency isolation (including SDL/PulseAudio fixes for headless joystick support).
* **Differential Drive Mixing:** Custom Python logic converting raw X/Y joystick axes into normalized left/right PWM motor speeds.
* **Background Daemon:** Configured to automatically launch as a system daemon on boot.

## 🛠️ Hardware Requirements

* **Compute:** Raspberry Pi 4 (or similar SBC running Ubuntu/Debian)
* **Motor Driver:** L293D Dual H-Bridge IC
* **Actuators:** 2x DC Motors (Left and Right)
* **Input:** PlayStation 4 DualShock Controller (Bluetooth)
* **Power:** Independent external battery pack for motor power (VCC2)

### GPIO Pinout (BCM)

| Component | Function | Raspberry Pi GPIO | L293D Pin |
| --- | --- | --- | --- |
| **Left Motor (A)** | Forward (IN1) | GPIO 5 | Pin 2 |
|  | Backward (IN2) | GPIO 6 | Pin 7 |
|  | Enable PWM (ENA) | GPIO 12 | Pin 1 |
| **Right Motor (B)** | Forward (IN3) | GPIO 23 | Pin 10 |
|  | Backward (IN4) | GPIO 24 | Pin 15 |
|  | Enable PWM (ENB) | GPIO 13 | Pin 9 |

*Note: The L293D ground pins must share a common ground with the Raspberry Pi.*

## 📦 Installation & Building

Since Linubot is packaged as a Snap, you do not need to install ROS 2 natively on your host machine. All dependencies are handled by Snapcraft.

1. **Clone the repository:**
```bash
git clone https://github.com/Diaoko9/Linubot.git
cd Linubot

```


2. **Build the Snap:**
```bash
snapcraft pack

```


3. **Install the built Snap:**
```bash
sudo snap install ./linubot_1.0_arm64.snap --dangerous --devmode

```



## 🎮 Usage

1. **Connect the PS4 Controller:**
Ensure your controller is paired via Bluetooth and registered to the OS at `/dev/input/js0`.
2. **Run the Robot:**
Upon installation, the snap runs automatically as a background daemon. To take manual control or view logs, stop the daemon and run it interactively:
```bash
sudo snap stop linubot
sudo snap run linubot

```


3. **Controls:**
* **Left Joystick (Vertical):** Forward / Backward Throttle
* **Left Joystick (Horizontal):** Left / Right Steering Mixing



## 🛑 Troubleshooting

* **`GPIO busy` Error:** If running manually, ensure the background daemon is stopped (`sudo snap stop linubot`) so it releases the hardware pins.
* **Controller not detected:** If `joy_node` fails to initialize, verify the PS4 controller hasn't gone to sleep and is still mapped to `js0`. You can restart the Bluetooth service via `sudo systemctl restart bluetooth`.

---

Now that the software and code are safely backed up and documented on GitHub, we can dive back into diagnosing the physical hardware. Do you want to start tracing the power lines to the L293D chip, or test the DC motors directly against the battery?
