#!/usr/bin/env python
import roslib; roslib.load_manifest('attentionwhore')
import rospy
import tf
import math
import geometry_msgs.msg
import kinematics_msgs.srv
import kinematics_msgs.msg
import sensor_msgs.msg
import arm_navigation_msgs.msg
import arm_navigation_msgs.srv
import brics_actuator.msg
from attentionwhore.msg import Trajectory


class SimpleIkSolver:

	def __init__(self):
		self.joint_names = ["arm_joint_1", "arm_joint_2", "arm_joint_3", "arm_joint_4", "arm_joint_5"]
		self.configuration = [0, 0, 0, 0, 0]
		self.received_state = False
		
		rospy.Subscriber('/joint_states', sensor_msgs.msg.JointState, self.joint_states_callback)
		
		rospy.loginfo("Waiting for 'get_constraint_aware_ik' service")
		rospy.wait_for_service('/youbot_arm_kinematics/get_constraint_aware_ik')
		self.ciks = rospy.ServiceProxy('/youbot_arm_kinematics/get_constraint_aware_ik', kinematics_msgs.srv.GetConstraintAwarePositionIK)
		rospy.loginfo("Service 'get_constraint_aware_ik' is ready")
		
		rospy.loginfo("Waiting for 'set_planning_scene_diff' service")
		rospy.wait_for_service('/environment_server/set_planning_scene_diff')
		self.planning_scene = rospy.ServiceProxy('/environment_server/set_planning_scene_diff', arm_navigation_msgs.srv.SetPlanningSceneDiff)
		rospy.loginfo("Service 'set_planning_scene_diff'")
		
		# a planning scene must be set before using the constraint-aware ik!
		self.send_planning_scene()


    #callback function: when a joint_states message arrives, save the values
	def joint_states_callback(self, msg):
		for k in range(5):
			for i in range(len(msg.name)):
				joint_name = "arm_joint_" + str(k + 1)
				if(msg.name[i] == joint_name):
					self.configuration[k] = msg.position[i]
		self.received_state = True


	def send_planning_scene(self):
		rospy.loginfo("Sending planning scene")
		
		req = arm_navigation_msgs.srv.SetPlanningSceneDiffRequest()
		res = self.planning_scene.call(req)


	def call_constraint_aware_ik_solver(self, goal_pose):
		while (not self.received_state):
			rospy.sleep(0.1)
		req = kinematics_msgs.srv.GetConstraintAwarePositionIKRequest()
		req.timeout = rospy.Duration(0.5)
		req.ik_request.ik_link_name = "arm_link_5"
		req.ik_request.ik_seed_state.joint_state.name = self.joint_names
		req.ik_request.ik_seed_state.joint_state.position = self.configuration
		req.ik_request.pose_stamped = goal_pose
		try:
			resp = self.ciks(req)
		except rospy.ServiceException, e:
			rospy.logerr("Service did not process request: %s", str(e))
		
		if (resp.error_code.val == arm_navigation_msgs.msg.ArmNavigationErrorCodes.SUCCESS):
			return resp.solution.joint_state.position
		else:
			return None


	def create_pose(self, x, y, z, roll, pitch, yaw):
		pose = geometry_msgs.msg.PoseStamped()
		pose.pose.position.x = x
		pose.pose.position.y = y
		pose.pose.position.z = z
		quat = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
		pose.pose.orientation.x = quat[0]
		pose.pose.orientation.y = quat[1]
		pose.pose.orientation.z = quat[2]
		pose.pose.orientation.w = quat[3]
		pose.header.frame_id = "/arm_link_0"
		pose.header.stamp = rospy.Time.now()
		
		return pose

def transmove(x, y, z, roll, pitch, yaw):
	#iks = SimpleIkSolver()
	pose = iks.create_pose(x, y, z, roll, pitch, yaw)
	
	print x, y, z, roll, pitch, yaw
	
	conf = iks.call_constraint_aware_ik_solver(pose)
	if (conf):
		# publish solution directly as joint positions
		print conf
		jp = brics_actuator.msg.JointPositions()

		for i in range(5):
			jv = brics_actuator.msg.JointValue()
			jv.joint_uri = iks.joint_names[i]
			jv.value = conf[i]
			jv.unit = "rad"
			jp.positions.append(jv)

		rospy.sleep(0.1)
		print "publishing cmd"
		armpub.publish(jp)
	else:
		print("IK solver didn't find a solution")


def callback(data):
	roll = 0.0#-math.pi / 2.0 #0.0
	pitch = math.pi / 2.0
	yaw = -math.pi / 2.0 #0.0
	z = 0.122#0.122
	#rospy.loginfo(data.data)
	#rospy.loginfo(data.trajectory)
	xCorrection = -0.09
	yCorrection = -0.499
	#xLimit = 0#0.22
	yLimit = 0.177
	zHigh = 0.14
	zTmp = zHigh
	#transmove((xLimit - data.trajectory[0].x) + xCorrection, (yLimit - data.trajectory[0].y) + yCorrection, zForNewPath, roll, pitch, yaw)
	while zTmp > z:
		zTmp -= 1.0 / 4000
		print zTmp
		transmove(data.trajectory[0].x + xCorrection, (yLimit - data.trajectory[0].y) + yCorrection, zTmp, roll, pitch, yaw)
		print "Down"
		#rospy.sleep(0.5)
	for i in range(len(data.trajectory)):
		x = data.trajectory[i].x + xCorrection
		#x = (xLimit - data.trajectory[i].x) + xCorrection
		y = (yLimit - data.trajectory[i].y) + yCorrection
		#print "(" + str(x) +", " + str(y) + "), ",
		transmove(x, y, z, roll, pitch, yaw)
		#rospy.sleep(0.1)
	#transmove((xLimit - data.trajectory[len(data.trajectory)-1].x) + xCorrection, (yLimit - data.trajectory[len(data.trajectory)-1].y) + yCorrection, zForNewPath, roll, pitch, yaw)
	while zTmp < zHigh:
		zTmp += 1.0 / 4000
		transmove(data.trajectory[len(data.trajectory)-1].x + xCorrection, (yLimit - data.trajectory[len(data.trajectory)-1].y) + yCorrection, zTmp, roll, pitch, yaw)
		#rospy.sleep(0.5)
	

def tester():
	test = ((0.0475, 0.0125), (0.05, 0.0125), (0.0525, 0.0125), (0.055, 0.0125), (0.0575, 0.0125), (0.06, 0.0125), (0.0625, 0.0125), (0.065, 0.0125), (0.0675, 0.0125), (0.07, 0.0125), (0.0725, 0.015), (0.075, 0.015), (0.0775, 0.015), (0.08, 0.015), (0.0825, 0.0175), (0.085, 0.0175), (0.0875, 0.02), (0.09, 0.02), (0.0925, 0.0225), (0.095, 0.025), (0.0975, 0.0275), (0.1, 0.03), (0.1025, 0.0325), (0.1025, 0.035), (0.105, 0.0375), (0.1075, 0.04), (0.1075, 0.0425), (0.11, 0.045), (0.11, 0.0475), (0.11, 0.05), (0.1125, 0.0525), (0.1125, 0.055), (0.1125, 0.0575), (0.1125, 0.06), (0.115, 0.0625), (0.115, 0.065), (0.115, 0.0675), (0.115, 0.07), (0.115, 0.0725), (0.115, 0.075), (0.115, 0.0775), (0.115, 0.08), (0.115, 0.0825), (0.115, 0.085), (0.115, 0.0875), (0.115, 0.09), (0.1125, 0.0925), (0.1125, 0.095), (0.1125, 0.0975), (0.1125, 0.1), (0.11, 0.1025), (0.11, 0.105), (0.11, 0.1075), (0.1075, 0.11), (0.1075, 0.1125), (0.105, 0.115), (0.1025, 0.1175), (0.1025, 0.12), (0.1, 0.1225), (0.0975, 0.125), (0.095, 0.1275), (0.0925, 0.13), (0.09, 0.1325), (0.0875, 0.1325), (0.085, 0.135), (0.0825, 0.135), (0.08, 0.1375), (0.0775, 0.1375), (0.075, 0.1375), (0.0725, 0.14), (0.07, 0.14), (0.0675, 0.14), (0.065, 0.14), (0.0625, 0.14), (0.06, 0.14), (0.0575, 0.14), (0.055, 0.14), (0.0525, 0.14), (0.05, 0.14), (0.0475, 0.14), (0.045, 0.1375), (0.0425, 0.1375), (0.04, 0.1375), (0.0375, 0.135), (0.035, 0.135), (0.0325, 0.1325), (0.03, 0.1325), (0.0275, 0.13), (0.025, 0.1275), (0.0225, 0.125), (0.02, 0.1225), (0.0175, 0.12), (0.0175, 0.1175), (0.015, 0.115), (0.0125, 0.1125), (0.0125, 0.11), (0.01, 0.1075), (0.01, 0.105), (0.01, 0.1025), (0.0075, 0.1), (0.0075, 0.0975), (0.0075, 0.095), (0.0075, 0.0925), (0.005, 0.09), (0.005, 0.0875), (0.005, 0.085), (0.005, 0.0825), (0.005, 0.08), (0.005, 0.0775), (0.005, 0.075), (0.005, 0.0725), (0.005, 0.07), (0.005, 0.0675), (0.005, 0.065), (0.005, 0.0625), (0.0075, 0.06), (0.0075, 0.0575), (0.0075, 0.055), (0.0075, 0.0525), (0.01, 0.05), (0.01, 0.0475), (0.01, 0.045), (0.0125, 0.0425), (0.0125, 0.04), (0.015, 0.0375), (0.0175, 0.035), (0.0175, 0.0325), (0.02, 0.03), (0.0225, 0.0275), (0.025, 0.025), (0.0275, 0.0225), (0.03, 0.02), (0.0325, 0.02), (0.035, 0.0175), (0.0375, 0.0175), (0.04, 0.015), (0.0425, 0.015), (0.045, 0.015))
	roll = 0.0#-math.pi / 2.0 #0.0
	pitch = math.pi / 2.0
	yaw = -math.pi / 2.0 #0.0
	z = 0.122
	x = 0.0
	y = -0.4
	#for i in range(100):
		#x += 1.0/5000
		#transmove(x, y, z, roll, pitch, yaw)
	for i in range(len(test)):
		x = test[i][0] - 0.09
		#x = (0.22 - test[i][0]) - 0.09
		y = test[i][1] - 0.504
		transmove(x, y, z, roll, pitch, yaw)

def listener():
	rospy.Subscriber("/trajectory", Trajectory, callback)
	rospy.spin()


if __name__ == '__main__':
	rospy.init_node('ik_solver_listener', anonymous=True)
	rospy.sleep(0.5)
	armpub = rospy.Publisher("/arm_1/arm_controller/position_command", brics_actuator.msg.JointPositions)
	iks = SimpleIkSolver()
	rospy.sleep(1)
	transmove(-0.09, -0.322, 0.17, 0.0, math.pi / 2.0, -math.pi / 2.0)
	rospy.sleep(1)
	#tester()
	listener()
