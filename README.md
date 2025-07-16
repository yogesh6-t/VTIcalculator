# VTIcalculator

# VTI Shot
VTIShot is a AI powered python utility which enables a user to calculate VTI in a single step.

VTI stands for : Velocity Time Integral. It’s a measurement used in echocardiography (ultrasound
of the heart) to quantify the distance that blood travels through a specific part of the heart
during one heartbeat.

 What VTI Measures:
VTI represents the area under the curve of a Doppler waveform. It essentially integrates (adds 
up) the blood velocity over time during one cardiac cycle.

VTI = ∫ Velocity(t) dt
This is computed by tracing the Doppler waveform (a curve showing blood velocity vs. time) during
either systole (ejection) or diastole (filling). The area under the curve is measured in centimeters.

VTI is used to calculate:
Stroke Volume (SV): how much blood the heart pumps in one beat.
Cardiac Output (CO): how much blood the heart pumps per minute.
Formula:
Stroke Volume = VTI× (Cross-sectional area of the outflow tract)
 Common VTI Applications:
- Left Ventricular Outflow Tract (LVOT) VTI → assess left ventricular function.
- Aortic and Pulmonary valve evaluation.
- Monitoring heart function in critically ill patients.

Traditionally VTI calculations were made by the echo-cardiograph machine operator using
pointer(stylus) where they manually trace the frozen frame from the doppler plot and the machine
does the calculation based on the plot, this feature is only present in the high-end, state of
the art echocardiograph machines. Most of the time the operators make a assumption/guess, where
Vmax and based on the time period of a regular systolic waveform time-period, approximately
0.3 secs VTI is vaguely rounded off to  ~(60-65)% of Vmax*time period.

<img src="/imgs/images.jpg" alt="VTI graph" title="This is a regular VTI image/plot." width="900">

Formula to Convert Pixels to Time

                    Time per pixel=1/(Sweep Speed × Pixels per mm)

*Sweep Speed on an echocardiograph (or echocardiogram machine) refers to the rate at
which the ultrasound images or waveforms (especially M-mode and Doppler) are displayed across the screen.
Time axis is scaled and time is calculater based on sweep speed, width in pixels and screen resolution. 

####                Total Time=Waveform Width in Pixels×Time per Pixel

# Flow
<div style="text-align: center;">
 <img width="400" height="496" alt="image" src="https://github.com/user-attachments/assets/e86a0a9e-323c-4d8d-9ba4-b51d9f75fcc0" />
</div>


VTI Shot uses a pipeline, with 3 blocks, at the head of which in the first block is a fine-tuned YOLOv5,
which is specifically trained to detect the plots in a given input image. Once the model generates the
expected information i.e. confidence, class:in this case just a single class `vti` and coordinates of
the detected plots.

In the second block, which involves image processing handling and refining the output from block 1. The
block goes on selecting only the plot(s) with most confidence, grabs the plots, isolates them from the
zero line. Using image processing techniques more specifically using morphological operations, the contours
are grabbed. Further they are processed using steps like erosion, dilation, opening and closing to get a
better and thorough plots, with definite width(time) and height(Vmax).

In the third block, contours from block 2 are scaled to realistically represents the machine output before
making the final calculations about the time period (t) of the heart cycle (VTI plot) and the amplitude
of the plot (Vmax). Scaling the plot on y-axis is straight-forward using the markers and written scale values.
Scaling y-axis gives us the cm(or m)/pixel, scaled to contour height gives us Vmax. Scaling x-axis gives us
the sec(or msec)/pixel, scaled to contour width gives us time, which can be used to calculate systolic
cycle time. Dividing contour area with x and y scales gives us the realistic and accurate VTI values.
contour area (pixel) x Vmax (cm/sec) x t (sec) : area (cm).

# Results

![VTI graph.](/imgs/test1.jpg "Test VTI image/plot.")

![VTI graph.](/imgs/test1_result.jpg "Test VTI image/plot.")

![VTI graph.](/imgs/test1_avg.jpg "Test VTI image/plot (avg).")

![VTI graph.](/imgs/test3.jpg "Test VTI image/plot.")

![VTI graph.](/imgs/test3_result.jpg "Test VTI image/plot.")

![VTI graph.](/imgs/test3_avg.jpg "Test VTI image/plot (avg).")
