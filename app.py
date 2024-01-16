##################################################################
# Brian Lesko 
# 12/2/2023
# Robotics Studies, control a virtual robot in C-space using a PS5 controller

import streamlit as st
import numpy as np
import modern_robotics as mr
import matplotlib.pyplot as plt
import time
import math

import dualsense # DualSense controller communication
import customize_gui # streamlit GUI modifications
import robot
DualSense = dualsense.DualSense
gui = customize_gui.gui()
my_robot = robot.two2_robot()

def main():
    # Set up the app UI
    gui.clean_format(wide=True)
    gui.about(text = "This code implements the configuration space of a 2R robot as a 2D plot.")
    Title, subTitle, Sidebar, image_spot = st.empty(), st.empty(), st.sidebar.empty(), st.columns([1,5,1])[1].empty()
    
    # Setting up the dualsense controller connection
    vendorID, productID = int("0x054C", 16), int("0x0CE6", 16)
    ds = DualSense(vendorID, productID)
    try: ds.connect()
    except Exception as e: st.error("Error occurred while connecting to Dualsense controller. Make sure the controller is wired up and the vendor and product ID's are correctly set in the python script.")
    
    # Initialize loop variables
    step = .001
    thetas = [0,0]
    fig, ax = my_robot.get_colored_plt('#F6F6F3','#335095','#D6D6D6')

    # Control Loop
    while True:
        ds.receive()
        ds.updateTriggers()
        ds.updateThumbsticks()

        # Thumbstick control
        ds.updateThumbsticks()
        if abs(ds.LX) > 4:
            thetas[0] = thetas[0] + (ds.LX)/128
        if abs(ds.LY) > 4:
            thetas[1] = thetas[1] - (ds.LY)/128

        # Determine which joint is selected
        joints_label = "<span style='font-size:30px;'>Joints:</span>"
        j1 = "<span style='font-size:30px;'>J1</span>" if abs(ds.LX) > 30 else "<span style='font-size:20px;'>J1</span>"
        j2 = "<span style='font-size:30px;'>J2</span>" if abs(ds.LY) > 30 else "<span style='font-size:20px;'>J2</span>"
        with Title: st.markdown(f" {joints_label} &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;{j1} &nbsp; | &nbsp; {j2} &nbsp; ", unsafe_allow_html=True)
            
        # make sure th1 and th2 are between -2pi and 2pi 
        thetas[0] = (thetas[0] + 2*np.pi) % (4*np.pi) - 2*np.pi
        thetas[1] = (thetas[1] + 2*np.pi) % (4*np.pi) - 2*np.pi
            
        # Show the C-Space map 
        ax.clear()
        ax.xaxis.label.set_color('#D6D6D6')
        ax.yaxis.label.set_color('#D6D6D6')
        fig = my_robot.get_c_space_figure(fig, ax, thetas[0], thetas[1])
        with image_spot: st.pyplot(fig)

        time.sleep(.02)

main()