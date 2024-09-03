# FYP-Full-Stack-PyroInsight
A full-stack web application has been in development to display data retrieved from system called a fire control panel in an organized and visually appealing manner on a dashboard app.

Data from the fire control panel is continuously collected via a COM port utilizing the MX Speak Protocol, a communication protocol commonly used by these panels. Within this protocol, a specific packet contains vital information regarding the connected devices to the panel, including attributes such as cleanliness and heat values.

The challenge at hand lies in the underutilization of this valuable data, presenting a potential business opportunity. The data can be harnessed in various ways, such as for preventive maintenance and false alarm detection.

To address this, a Raspberry Pi 4 is employed to run a service application developed in C++. This application interfaces with the fire control panel using the MX Protocol to retrieve and store data in a logfile. After completing my internship at Johnson Controls, I no longer have access to panels. Consequently, I have decided to create a Python script that simulates the data being produced.

There is another script that is used to upload the formatted data into a PostgresSQL database. A backend has been crafted to retrieve this data from the database, delivering it in JSON format using FastAPI. Additionally, a user-friendly front-end dashboard web application has been created to visualize the data through graphs, charts, and statistics using Dash. 

Machine learning algorithms such as Linear Regression and Random Forest has been untilised for predicting future values for temperature, carbon monoxide, obscuration and dirtiness using Scikit-Learn.

So in total there are 4 parts in this project:
- Simulator
- Data uploader
- Frontend
- Backend
