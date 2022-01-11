import math
def reward_function(params):

    # Read input variable
    steps = params['steps']
    progress = params['progress']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    speed = params['speed']
    abs_steering = abs(params['steering_angle']) # Only need the absolute steering angle
    currentposition = (params['x'],params['y'])
    is_offtrack = params['is_offtrack']
    all_wheels_on_track = params['all_wheels_on_track']
    speed_up = False
    straight = False
    
    # Total num of steps we want the car to finish the lap, it will vary depends on the track length
    TOTAL_NUM_STEPS = 700
    STEER_THRES = 10
    TURN_THRESHOLD_SPEED = 6
    TURN_THRESHOLD_STRAIGHT = 20
    FUTURE_STEP = 6
    FUTURE_STEP_STRAIGHT = 8
    
    # Identify next waypoint and a further waypoint
    point_prev = waypoints[closest_waypoints[0]]
    point_next = waypoints[closest_waypoints[1]]
    point_future = waypoints[min(len(waypoints) - 1,
                                 closest_waypoints[1] + FUTURE_STEP)]

    # Calculate headings to waypoints
    heading_current = math.degrees(math.atan2(point_prev[1]-point_next[1], 
                                           point_prev[0] - point_next[0]))
    heading_future = math.degrees(math.atan2(point_prev[1] - point_future[1], 
                                           point_prev[0] - point_future[0]))

    # Calculate the difference between the headings
    diff_heading = abs(heading_current - heading_future)

    # Check we didn't choose the reflex angle
    if diff_heading > 180:
        diff_heading = 360 - diff_heading

    if diff_heading < TURN_THRESHOLD_SPEED:
        # If there's no corner encourage going faster
        speed_up = True
    else:
        # If there is a corner encourage slowing down
        speed_up = False

    if diff_heading < TURN_THRESHOLD_STRAIGHT:
        # If there's no corner encourage going straighter
        straight = True
    else:
        # If there is a corner don't encourage going straighter
        straight = False

    # Initialize the reward with typical value
    reward = 1e-3

    if is_offtrack:
        return reward

    # Give higher reward if the car is closer to centre line and vice versa
    # 0 if you're on edge of track, 1 if you're centre of track
    reward = 1 - (distance_from_center/(track_width/2))**(1/4) 

    if (steps % 50) == 0 and progress/100 > (steps/TOTAL_NUM_STEPS):
        # reward += 2.22 for each second faster than 45s projected
        reward += progress - (steps/TOTAL_NUM_STEPS)*100

    if straight and abs_steering < STEER_THRES:
        reward += 0.3

    if speed_up and speed > 3 and abs_steering < STEER_THRES:
        reward += 2.0
    elif not speed_up and speed < 1:
        reward += 0.5
        
    if not all_wheels_on_track:
        reward -= 0.5
        
    reward = max(reward, 1e-3)
    return float(reward)