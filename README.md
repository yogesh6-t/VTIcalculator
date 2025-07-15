# VTIcalculator

# VTI Shot
VTIShot is a AI powered python utility which enables a user to calculate VTI in a single step.

Traditionally VTI calculations were made by the echo-cardiograph machine operator using
pointer(stylus) where they manually trace the frozen frame from the doppler plot and the machine
does the calculation based on the plot, which is a rare occurring, most of the time the operators
do a assumption, where they see the Vmax and give an assumption based on the time period of a
regular systolic waveform time-period.

VTI stands for : Velocity Time Integral. It’s a measurement used in echocardiography (ultrasound
of the heart) to quantify the distance that blood travels through a specific part of the heart
during one heartbeat.

 What VTI Measures:
VTI represents the area under the curve of a Doppler waveform. It essentially integrates (adds 
up) the blood velocity over time during one cardiac cycle.

VTI = ∫ Velocity(t) dt
This is computed by tracing the Doppler waveform (a curve showing blood velocity vs. time) during either systole (ejection) or diastole (filling). The area under the curve is measured in centimeters.

VTI is used to calculate:
Stroke Volume (SV): how much blood the heart pumps in one beat.
Cardiac Output (CO): how much blood the heart pumps per minute.
Formula:
Stroke Volume = VTI× (Cross-sectional area of the outflow tract)
 Common VTI Applications:
- Left Ventricular Outflow Tract (LVOT) VTI → assess left ventricular function.
- Aortic and Pulmonary valve evaluation.
- Monitoring heart function in critically ill patients.

![VTI graph.](/image/sample.webp "This is a sample image.")

Formula to Convert Pixels to Time
                    Time per pixel=1/(Sweep Speed × Pixels per mm)
                    Time per pixel= Sweep Speed×Pixels per mm

Total Time=Waveform Width in Pixels×Time per Pixel
