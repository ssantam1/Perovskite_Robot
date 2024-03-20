# ECD415 Robotic Arm Controlled Perovskite Synthesis

This repository contains the code and documentation for the ECD415 Robotic Arm Controlled Perovskite Synthesis project, which is an ECE Senior Capstone Project for the academic year 2023-2024 sponsored by the ECE Department at Binghamton University.

## Project Overview

In this project, we aim to develop an autonomous system for synthesizing perovskite samples on glass slides for analysis and testing. Currently, graduate students spend significant time and labor manually synthesizing these samples. Our goal is to automate this process to free up time for graduate students and to increase the speed and efficiency of sample production.

The project builds upon the work of the previous team, ECD317 Autonomous Perovskite Solar Cell Synthesis, which completed an initial design of the system. Our team is tasked with improving upon the initial designs and implementing the missing station from the previous year's project to achieve a fully autonomous run through of the complete synthesis process.

## System Components

Our system consists of the following main components:

- **Gantry**: The gantry, based on the design of an Ender 3 3D Printer with extended rails for y-direction movement, provides the necessary movement for the robotic head. It allows for a large work area and precise positioning of the robotic head.

- **Robotic Head**: The robotic head replaces the extruder of the 3D printer with a suction cup and pipette for moving the solution between the stations of the synthesis process.

- **Microcontroller**: The microcontroller serves as the central control unit of the system, coordinating the actions of the gantry, robotic head, and various stages of the synthesis process.

- **Stations**:
  - **Carousel Stage**: Allows for the selection of solutions and vials for mixing the stock solutions into an input solution.
  - **Spin Coater Stage**: Enables the uniform coating of the slide to prepare it for subsequent stages.
  - **Hot Plate Stage**: Anneals the solution to remove any precipitates and permits the usage of a spectrometer to test for photoluminescence.

## Acknowledgments

We would like to thank the ECE Department at Binghamton University for sponsoring this project and providing the necessary resources for its completion. Additionally, we are grateful to the Center for Autonomous Solar Power (CASP) Lab for their support and guidance throughout the development process.

## Contact Information

For inquiries about the project or collaboration opportunities, please contact:

- Project Lead: Pierce Alvir
- Email: palvir1@binghamton.edu

- Software Lead: Steven Santamorena
- Email: stevenasanta@gmail.com