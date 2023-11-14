
# RTOS Framework Project. G11 

This project is designed to follow the Real-Time Operating System (RTOS) framework. It consists of three main tasks, each implemented as a class. An object of each task is declared and added to the scheduler.

## Project Overview


1. **Task 1: Classify weather through image by AI**
   - Train an AI model for image classification (e.g., sunny, cloudy, rainy). Provide suggestions based on weather conditions. Voice output for increased accessibility.
   
3. **Task 2: Predict weather using historical weather with Machine Learning**
   - This task utilizes machine learning algorithms to analyze historical weather patterns. Train the model to predict future weather.

4. **Task 3: Clone Climate Info from OpenWeatherMap**
   - This task is responsible for fetching climate information from the OpenWeatherMap API. It demonstrates how to use an API to collect weather data and showcases the multitasking capabilities of the RTOS.
   - Dashboard: https://io.adafruit.com/hej_manh/dashboards/introcs

### Getting Started

To get a local copy up and running, follow these simple steps:

1. Clone the repo
  
   git clone https://github.com/nima321123/G11_Intro2CS_Project.git
  

2. Install the required packages
- **Task 1:**
  - **Libraries**:
    - Install with: `pip install tkinter, `pip install Pillow`, `pip install keras`, `pip install numpy`, `pip install pyttsx3`
- **Task 2:**
   - **Libraries**:
    - Install with: `pip install pandas`,`pip install matplotlib`,`pip install scikit-learn`
- **Task 3:**
  - **Requests**:
    - Install with: `pip install requests`
  - **Adafruit-IO**
    - Install with: `pip install adafruit-io`

3. Run the main file
   ```sh
   python main.py
   ```


#### Contact

Contributing members:

- Nhi Mai Thi Yen - 10422061@student.vgu.edu.vn
- Anh Nguyen Ngoc Minh - 10422009@student.vgu.edu.vn
- Vy Nguyen Thao - 10421067@student.vgu.edu.vn

Project Link: [https://github.com/nima321123/G11_Intro2CS_Project](https://github.com/nima321123/G11_Intro2CS_Project)

