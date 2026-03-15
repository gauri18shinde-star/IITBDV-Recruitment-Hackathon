
'''
PPC Hackathon — Participant Boilerplate
You must implement two functions: plan() and control()
'''

# ─── TYPES (for reference) ────────────────────────────────────────────────────

# Path: list of waypoints [{"x": float, "y": float}, ...]
# State: {"x", "y", "yaw", "vx", "vy", "yaw_rate"} 
# CmdFeedback: {"throttle", "steer"}         

# ─── CONTROLLER ───────────────────────────────────────────────────────────────
import numpy as np



def steering(path: list[dict], state: dict):

    length_of_car = 2.6
    # Calculate steering angle based on path and vehicle state

    ##################################################
    #Changes
    ##################################################
    
    #lookahead = 4.0
    speed = np.hypot(state["vx"], state["vy"])
    lookahead = 2.0 + 0.8 * speed
    #lookahead = 4.0 + 0.04 * speed*speed
    
    
    x = state["x"]
    y = state["y"]
    yaw = state["yaw"]

    # find closest waypoint
    closest = 0
    min_dist = 1e9

    for i, p in enumerate(path):
        dx = p["x"] - x
        dy = p["y"] - y
        d = np.hypot(dx, dy)

        if d < min_dist:
            min_dist = d
            closest = i

    # find lookahead point
    target = path[min(closest + 1, len(path)-1)]
    #vs changes
    #target = path[min(closest + int(2 + speed), len(path)-1)]
     #vs changes
    dx = target["x"] - x
    dy = target["y"] - y

    # transform to vehicle coordinates
   # local_x = np.cos(yaw)*dx + np.sin(yaw)*dy
    local_y = np.sin(-yaw)*dx + np.cos(yaw)*dy

    if local_y == 0:
        return 0

    curvature = 2 * local_y / (lookahead**2)

    steer = np.arctan(length_of_car * curvature)

    ##################################################

    if(steer<0):
        steer = -0.5#min(-0.5, steer)

    ##################################################
    # steer = 0.0 # Default steer value
    # 0.5 in the max steering angle in radians (about 28.6 degrees)
    ##################################################
    return np.clip(steer, -0.5, 0.5)


def throttle_algorithm(target_speed, current_speed, dt):

    ##################################################
    #Changes
    ##################################################
    kp = 0.6

    error = target_speed - current_speed

    throttle = kp * error

    if throttle < 0:
        brake = -throttle
        throttle = 0
    else:
        brake = 0


    # generate the output for throttle command
    ##################################################
    #throttle = 0
    #brake = 0.0
    ##################################################

    # clip throttle and brake to [0, 1]
    # ##################################################
    # throttle = min(1, throttle)
    # brake = min(1, brake)
    ##################################################
    return np.clip(throttle, 0.0, 1.0), np.clip(brake, 0.0, 1.0)

def control(
    path: list[dict],
    state: dict,
    cmd_feedback: dict,
    step: int,
) -> tuple[float, float, float]:
    """
    Generate throttle, steer, brake for the current timestep.
    Called every 50ms during simulation.

    Args:
        path:         Your planned path (waypoints)
        state:        Noisy vehicle state observation
                        x, y        : position (m)
                        yaw         : heading (rad)
                        vx, vy      : velocity in body frame (m/s)
                        yaw_rate    : (rad/s)
        cmd_feedback: Last applied command with noise
                        throttle, steer, brake
        step:         Current simulation timestep index

    Returns:
        throttle  : float in [0.0, 1.0]   — 0=none, 1=full
        steer     : float in [-0.5, 0.5]  — rad, neg=left
        brake     : float in [0.0, 1.0]   — 0=none, 1=full
    
    Note: throttle and brake cannot both be > 0 simultaneously.
    """
    throttle = 0.0
    steer    = 0.0
    brake = 0.0
   
    # TODO: implement your controller here
    steer = steering(path, state)
  #  target_speed = 9.0  # m/s, adjust as needed

    #speed = np.hypot(state["vx"], state["vy"])

    if abs(steer) < 0.1:
        target_speed = 10.0
    elif abs(steer) < 0.25:
        target_speed = 8.75
    else:
        target_speed = 9.5

    global integral
    throttle, brake = throttle_algorithm(target_speed, state["vx"], 0.05)

    return throttle, steer, brake
