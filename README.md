# Smart Waste Management System

This project implements a smart waste management system that utilizes Arduino and Python to monitor waste bins and optimize waste collection routes.

## Description

The system consists of two main components:

1. **Arduino-based Waste Bin Monitoring System**: The Arduino microcontroller is equipped with various sensors including an ultrasonic sensor (HC-SR04) to measure the distance of waste in the bin, a temperature and humidity sensor (DHT11) to measure environmental conditions, and a gas sensor (MQ-4) to detect gas concentration. Based on these sensor readings, the Arduino determines whether the waste in the bin is wet or dry. If the bin is filled and the waste is detected, the Arduino sends a signal to the connected computer (Raspberry Pi or PC) via serial communication.

2. **Python-based Waste Route Optimization**: The Python program running on the connected computer receives signals from the Arduino indicating the type of waste detected. It then updates the waste bin locations on a graphical user interface (GUI) and calculates the shortest route to collect the waste bins based on their locations. The route optimization is performed using dynamic programming to solve the Travelling Salesman Problem (TSP). The optimized route is displayed on the GUI, helping waste collection personnel efficiently collect waste from the bins.

## Installation

### Arduino Setup

1. Connect the HC-SR04, DHT11, and MQ-4 sensors to the Arduino board as per the connections specified in the code.
2. Upload the provided Arduino sketch (`waste_bin_monitoring.ino`) to the Arduino board.

### Python Setup

1. Install Python (3.x recommended) on your computer.
2. Install the required Python libraries using pip:

