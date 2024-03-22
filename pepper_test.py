import time
import numpy as np
import naoqi as n
import pepper_kinematics as pk
import qi
import sys

IP = "128.237.247.249"
port = 9559
host = "nao.local"

tts = n.ALProxy("ALTextToSpeech", IP, port)
m = n.ALProxy("ALMotion", host, port)

m.setAngles(pk.left_arm_tags, pk.left_arm_work_pose, 1.0)

time.sleep(1.0)

current_angles = m.getAngles(pk.left_arm_tags)
current_position, current_orientation = pk.left_arm_get_position(current_angles)

target_position = current_position
target_position[1] = target_position[1] + 0.10 # 10 cm toward left
target_position[0] += 0.10
target_orientation = current_orientation # This is not supported yet

target_angles = pk.left_arm_set_position(current_angles, target_position, target_orientation)
if target_angles:
    tts.say("I am moving my left arm")
    m.setAngles(pk.left_arm_tags, target_angles, 1.0)
