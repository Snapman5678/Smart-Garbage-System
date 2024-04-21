# Smart Waste Management System

This project implements a smart waste management system that utilizes Arduino and Python to monitor waste bins and optimize waste collection routes.

## Description

The system consists of two main components:

1. **Arduino-based Waste Bin Monitoring System**: The Arduino microcontroller is equipped with various sensors including an ultrasonic sensor (HC-SR04) to measure the distance of waste in the bin, a temperature and humidity sensor (DHT11) to measure environmental conditions, and a gas sensor (MQ-4) to detect gas concentration. Based on these sensor readings, the Arduino determines whether the waste in the bin is wet or dry. If the bin is filled and the waste is detected, the Arduino sends a signal to the connected computer (Raspberry Pi or PC) via serial communication.

2. **Python-based Waste Route Optimization**: The Python program running on the connected computer receives signals from the Arduino indicating the type of waste detected. It then updates the waste bin locations on a graphical user interface (GUI) and calculates the shortest route to collect the waste bins based on their locations. The route optimization is performed using dynamic programming to solve the Travelling Salesman Problem (TSP). The optimized route is displayed on the GUI, helping waste collection personnel efficiently collect waste from the bins.

## Installation

### Arduino Setup

1. Connect the HC-SR04, DHT11, and MQ-4 sensors to the Arduino board as per the connections specified in the code.
2. Upload the provided Arduino sketch (`main.cpp`) to the Arduino board.

### Python Setup

1. Install Python (3.x recommended) on your computer.
2. Install the required Python libraries using pip:
3. '''bash
   pip install pygame pyserial
   '''


5. Download or clone the repository to your local machine.
6. Run the Python script `main.py` to start the waste route optimization program.

## Usage

1. Start the Python program (`waste_route_optimization.py`) to initialize the waste route optimization system.
2. The program will randomly generate 5 waste bins on the GUI.
3. Connect the Arduino to the computer via USB.
4. Once the Arduino detects waste in a bin, it will send a signal indicating the waste type (wet or dry) to the computer.
5. The Python program will update the GUI to reflect the new waste bin status and optimize the waste collection route.
6. Click the "Show Route" button on the GUI to display the optimized waste collection route.
7. Waste collection personnel can follow the displayed route to efficiently collect waste from the bins.

## Contributors

- [Aamir Mohammed](https://github.com/Snapman5678)
- [Akhmal Mohammed](https://github.com/contributor2)
- [Adhvaith Rajesh](https://github.com/contributor3)

## License

This project is licensed under the [MIT License](LICENSE).


