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
    
    # Total num of steps we want the car to finish the lap, it will vary depends on the track length
    TOTAL_NUM_STEPS = 300

    # Initialize the reward with typical value
    reward = 1.0

    # Give additional reward if the car pass every 100 steps faster than expected
    if (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100 :
        reward += 10.0

    # Calculate the distance from each border
    distance_from_border = 0.5 * track_width - distance_from_center

    # Reward higher if the car stays inside the track borders
    if distance_from_border >= 0.05:
        reward += 10.0
    else:
        reward -= 5 # Low reward if too close to the border or goes off the track

    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    
    # Convert to degree
    track_direction = math.degrees(track_direction)
    
    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5
    
    if(is_offtrack)
        reward *= 0.5
    
    point1 = waypoints[closest_waypoints[1]]
    point2 = waypoints[closest_waypoints[2]]
    point3 = waypoints[closest_waypoints[3]]
    
    slope1 = (point2.y-point1.y)(point3.x-point2.x)
    slope2 = (point3.y-point2.y)(point2.x-point1.x)
    
    if(slope1 == slope2 and speed >= 3.0) #Straight line
        reward *= 2


    return float(reward)