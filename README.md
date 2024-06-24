# ReadMe File for US/PAT C-mode Measurement Script

## Overview

This Python script is designed to perform combined Ultrasound (US) and Photoacoustic Tomography (PAT) C-mode measurements in a clinical setting. The script interfaces with a Thorlabs stage and an Optical Parametric Oscillator (OPO) via a socket connection, manages the OPO flashlamp, and executes the measurements by moving the stage to specified locations and performing laser multishots. After completing the measurements, the stage returns to its initial position, and the OPO flashlamp is turned off. All the key parameters and timestamps are logged in a separate log file for reference.

## Script Execution Environment

- The script is intended to be executed within the Spyder console environment.
- It runs on an OCT PC used in clinical settings for combined US/PAT measurements.

## Main Functionalities

1. **Initialize and Connect to Devices:**
   - Connects to a Thorlabs stage.
   - Establishes a socket connection to the OPO.

2. **Set Measurement Parameters:**
   - Defines step size, number of steps, wavelengths, delay between steps, and direction of motion.

3. **Logging:**
   - Logs the start time, measurement parameters, and other significant events in a log file.

4. **Perform Measurements:**
   - Moves the stage to target positions.
   - Performs laser multishots at each position.
   - Uses multiple wavelengths if specified.

5. **Clean Up:**
   - Returns the stage to the initial position.
   - Turns off the OPO flashlamp.
   - Logs the end time of the measurements.

## Parameters and Variables

- **N (int)**: Number of steps the stage will move. Must be an even number. (Default: 30)
- **STEP_SIZE (int)**: Step size in micrometers for the stage movement. Within the current setup, range of more than 8 mm are avoided. (Default: 200)
- **WAVELENGTH (list of int)**: List of wavelengths in nanometers used for the measurements. The length of this list must match the number of photoacoustic frames in the Verasonics script. (Default: [430, 530, 630])
- **DELAY (float)**: Delay in seconds between each step of the stage movement. A useful range is 1.0 to 2.5 seconds. (Default: 1.2)
- **SIGN (int)**: Direction of stage movement. Use 1 for towards the fiber bundle and -1 for backwards. (Default: 1)
- **filename_today (str)**: Name of the log file based on the current date.
- **stage**: Thorlabs Kinesis Motor object representing the motorized stage.
- **units (str)**: Units of the stage position (e.g., mm or m).
- **pos (float)**: Current position of the stage.
- **IP (str)**: IP address of the OPO. (Default: "192.168.12.223")
- **PORT (int)**: Port number for the remote client connection to the OPO. (Default: 1025)
- **client**: Socket object for communication with the OPO.

## Usage Instructions

1. **Set Parameters:**
   - Adjust the parameters (N, STEP_SIZE, WAVELENGTH, DELAY, SIGN) as needed before running the script.

2. **Run Script:**
   - Execute the script in the Spyder console environment that controls the OPO and the motorizes stage.

3. **Monitor Execution:**
   - Observe the console output for the current stage position, wavelength settings, and other status messages.
   - Ensure the safety goggles are used if wavelengths above 532 nm are employed.

## Safety and Precautions

- Verify the correct safety goggles are used for the applied wavelengths.
- Ensure the stage is homed and the initial position is clear before starting the measurements.

---

This ReadMe file provides a concise summary of the script's functionality, parameters, and usage instructions for effective and safe operation during clinical measurements.
```