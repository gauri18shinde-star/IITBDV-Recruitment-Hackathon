import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/gauri/racing/IITBDV-Recruitment-Hackathon/Simulation-Development/workspace/install/robot_sim'
