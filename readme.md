# VATSIM mach

#Update
This reposito

## Introduction
This repository has existed for many years but it has been privte for a long time. My vACC has used it as their foundation for their own Euroscope plugin, which has a feature that makes a rough calculation for VATSIM aircraft' mach number and indicated airspeed.

It works by extracting weather data from all layers of airspace for a very limited set of locations within and in close proximity to our FIR. The only data we use are: wind speed and heading as well as temperature. 

## Calculations
Mach numbers are calculated as follows: **TAS/LSS**

Indicated air speed is calculated as: **TAS/(1 + (AFL/ 10) *0.0175)**, [which simply reduces the TAS by 1.75% per 1000ft of altitude](https://skybrary.aero/articles/true-airspeed#:~:text=A%20very%20simple%20rule%20of,every%201000%20ft%20of%20altitude) ( suggest 2% but limited testing has showed 1.75 had greater accuracy.)

TAS = GS + (cos(Δheading(aircraft and wind)) * wind speed)

LSS = 643.855*((kelvin/273.15)**0.5)    [(knots)](https://www.weather.gov/media/epz/wxcalc/speedOfSound.pdf)

## Our implementation
_Step one: locations_

[We have one point for each of the entry points of our AOR.](https://webtools.kusternet.ch/geo/coordinatesconverter) Then, there are a few points scattered around the busiest parts of the airspace. **Keep the number of locatons to the bare minimum!** Our data comes from a reliable source, we don't want to bring our project to their attention.
![image](https://user-images.githubusercontent.com/51272243/186398340-4fdaa9d9-ca1f-426e-9515-83dab72e739a.png)

_Step two: API_

We have a server that executes the scripts and uplaods a weather file for the plugin to use. 

_Step three: plugin_

Write a plugin that, for each aircraft, find the closest available data point. Then, find the nearest altitude for which you have data and perform your calcualtions as provided below. In our implementation, we only show the mach number for aircraft above FL245 (early enough to have conversion mach number) while IAS is always shown. 

![image](https://user-images.githubusercontent.com/51272243/186400200-e80c135c-f723-46b1-8465-b836c5224516.png)
![image](https://user-images.githubusercontent.com/51272243/186400664-4844bacd-099b-41b9-9704-9059b0872849.png)




## Limitations
Different weather enginers for different simulators will inevitably result in different speeds, even if the only reason is the so called "resolution" of their data. Therefore, it's ONLY meant to be as a reference tool, not the hard truth. I will literally die inside if I hear someone tell a pilot he is doing 5 KT over the assigned speed. 

I would say the margin of error here is roughly about 10KT or M0.02. Keep this in mind at all times. 

Oh, and Euroscopes ground speed is sometimes very cluncy, we prefer the Topsky one but we don't have the data it has (iirc it's the average from the last x-positions). So if your speed jumps all around, blame Euroscope.

## Hopes for the network
With the new CoC now requiring pilots to use real world weather* it was time for me to realease this publicly. I hope someone will pick up on this, improve it and provide a plugin for all users to enjoy. 

[Data sourcing comes from there.](https://github.com/Louis-He/windyLib/blob/master/windyLib.py)
