# VATSIM mach
This repository has existed for many years but it has been privte for a long time. My vACC has used it as their foundation for their own Euroscope plugin, which has a feature that makes a rough calculation for VATSIM aircraft' mach number and indicated airspeed.

It works by extracting weather data from all layers of airspace for a very limited set of locations within and in close proximity to our FIR. The only data we use are: wind speed and heading as well as temperature. 

# Calculations
Mach numbers are calculated as follows: TAS/LSS

Indicated air speed is calculated as: TAS/(1 + (AFL/ 10) *0.0175), [which simply reduces the TAS by 1.75% per 1000ft of altitude](https://skybrary.aero/articles/true-airspeed#:~:text=A%20very%20simple%20rule%20of,every%201000%20ft%20of%20altitude) ( suggest 2% but limited testing has showed 1.75 had greater accuracy.)

TAS = GS + (cos(Δheading(aircraft and wind)) * wind speed)

LSS = 643.855*((kelvin/273.15)**0.5)    [(knots)](https://www.weather.gov/media/epz/wxcalc/speedOfSound.pdf)
