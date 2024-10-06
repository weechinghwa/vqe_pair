import subprocess


## O22
base_command = "python compute.py -i 2121_O22_herm_5_val -o SPSA -e no -n Hlp -esti esti0"
params1 = [ # alpha, target_magnitude, A, gamma, c 
        "-lrp [0.602,0.10,0.00,0.101,0.1]", "-lrp [0.602,0.10,0.00,0.101,0.1]", "-lrp [0.602,0.10,0.00,0.101,0.1]",
        "-lrp [0.602,0.10,10.0,0.101,0.1]", "-lrp [0.602,0.10,10.0,0.101,0.1]", "-lrp [0.602,0.10,10.0,0.101,0.1]",
        "-lrp [0.602,0.10,20.0,0.101,0.1]", "-lrp [0.602,0.10,20.0,0.101,0.1]", "-lrp [0.602,0.10,20.0,0.101,0.1]",
]    

commands = [f"{base_command} {param}" for param in params1]

for cmd in commands:
    process = subprocess.run(cmd, shell=True, check=True)



## O20
base_command = "python compute.py -i 2121_O20_herm_5_val -o SPSA -e no -n Hlp -esti esti0"
params1 = [ # alpha, target_magnitude, A, gamma, c 
        "-lrp [0.602,0.10,0.00,0.101,0.1]", "-lrp [0.602,0.10,0.00,0.101,0.1]", "-lrp [0.602,0.10,0.00,0.101,0.1]",
        "-lrp [0.602,0.10,10.0,0.101,0.1]", "-lrp [0.602,0.10,10.0,0.101,0.1]", "-lrp [0.602,0.10,10.0,0.101,0.1]",
        "-lrp [0.602,0.10,20.0,0.101,0.1]", "-lrp [0.602,0.10,20.0,0.101,0.1]", "-lrp [0.602,0.10,20.0,0.101,0.1]",

]    

commands = [f"{base_command} {param}" for param in params1]

for cmd in commands:
    process = subprocess.run(cmd, shell=True, check=True)


## O18
base_command = "python compute.py -i 2121_O18_herm_5_val -o SPSA -e no -n Hlp -esti esti0"
params2 = [ # alpha, target_magnitude, A, gamma, c 
        "-lrp [0.602,0.10,0.00,0.101,0.1]", "-lrp [0.602,0.10,0.00,0.101,0.1]", "-lrp [0.602,0.10,0.00,0.101,0.1]",
        "-lrp [0.602,0.10,10.0,0.101,0.1]", "-lrp [0.602,0.10,10.0,0.101,0.1]", "-lrp [0.602,0.10,10.0,0.101,0.1]",
        "-lrp [0.602,0.10,20.0,0.101,0.1]", "-lrp [0.602,0.10,20.0,0.101,0.1]", "-lrp [0.602,0.10,20.0,0.101,0.1]",

]

commands = [f"{base_command} {param}" for param in params2]

for cmd in commands:
    process = subprocess.run(cmd, shell=True, check=True)

## He6
base_command = "python compute.py -i 2121_He6_herm_1 -o SPSA -e no -n Hlp -esti esti0"
params3 = [ # alpha, target_magnitude, A, gamma, c 
        "-lrp [0.602,0.10,0.00,0.101,0.1]", "-lrp [0.602,0.10,0.00,0.101,0.1]", "-lrp [0.602,0.10,0.00,0.101,0.1]",
        "-lrp [0.602,0.10,10.0,0.101,0.1]", "-lrp [0.602,0.10,10.0,0.101,0.1]", "-lrp [0.602,0.10,10.0,0.101,0.1]",
        "-lrp [0.602,0.10,20.0,0.101,0.1]", "-lrp [0.602,0.10,20.0,0.101,0.1]", "-lrp [0.602,0.10,20.0,0.101,0.1]",

]    

commands = [f"{base_command} {param}" for param in params3]

for cmd in commands:
    process = subprocess.run(cmd, shell=True, check=True)