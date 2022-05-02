from .. stage_titouan import *
import json
from ..stage_titouan.Misc.RobotDefine import *
import threading

class CtrlRobot():
    """Blabla"""

    def __init__(self,model,robot_ip):
        self.model = model

        self.wifiInterface = WifiInterface(robot_ip)
        self.points_of_interest = []
        self.action = ""
        self.enact_step = 0
        self.outcome_bytes = b'{"status":"T"}'  # Default status T timeout
        self.robot_has_finished_acting = True

    def main(self,dt):
        """Blabla"""
        if self.robot_has_finished_acting:
            self.robot_has_finished_acting = False
            robot_data = self.translate_robot_data(b'{"status":"T"}')
            
            


    def translate_robot_data(self,data): #PAS FINITO ?
        """Translate data from the robot to data usable
        by the model
        """
        angle = 0
        outcome_for_agent = 0
        phenom_info = (0,0,0,0,None,None)
        translation = [0,0]
        rotation = 0
        obstacle = 0
        floor = 0
        shock = 0
        blocked = 0
        x = None
        y = None
        json_outcome = json.loads(self.outcome_bytes)
        echo_array = []

        # Updating the model from the latest received outcome
        outcome = json.loads(data)
        floor = 0
        if 'floor' in outcome:
            floor = outcome['floor']
            outcome_for_agent = json_outcome['floor']
        shock = 0
        if 'shock' in outcome and self.action == '8' and floor == 0:
            shock = outcome['shock']  # Yellow star
            outcome_for_agent = json_outcome['shock']
        blocked = 0
        if 'blocked' in outcome and self.action == '8' and floor == 0:
            blocked = outcome['blocked'] # Red star
            outcome_for_agent = json_outcome['shock'] #OULAH

        # floor_outcome = outcome['outcome']  # Agent5 uses floor_outcome

        if outcome['status'] == "T":  # If timeout no ego memory update
            print("No ego memory update")
        else:
            # Presupposed displacement of the robot relative to the environment
            translation = [0, 0]
            rotation = 0
            if self.action == "1":
                rotation = 45
            if self.action == "2":
                translation[0] = -STEP_FORWARD_DISTANCE
            if self.action == "3":
                rotation = -45
            if self.action == "4":
                translation[1] = SHIFT_DISTANCE
            if self.action == "6":
                translation[1] = -SHIFT_DISTANCE
            if self.action == "8":
                if not blocked:
                    translation[0] = STEP_FORWARD_DISTANCE * outcome['duration'] / 1000

            # Actual measured displacement if any
            if 'yaw' in outcome:
                rotation = outcome['yaw']

            # Estimate displacement due to floor change retreat
            if floor > 0:  # Black line detected
                # Update the translation
                forward_duration = outcome['duration'] - 300  # Subtract retreat duration
                if self.action == "8":  # TODO Other actions
                    translation[0] = STEP_FORWARD_DISTANCE * forward_duration/1000 - RETREAT_DISTANCE
                    if (translation[0] < 0 ) :
                            print("translation negative")
                    if floor == 0b01:  # Black line on the right
                        translation[0] -= 0
                        translation[1] = RETREAT_DISTANCE_Y
                    if floor == 0b10:  # Black line on the left
                        translation[0] -= 0
                        translation[1] = -RETREAT_DISTANCE_Y
                if self.action == "4":
                    translation[0] = -RETREAT_DISTANCE
                    translation[1] = SHIFT_DISTANCE * forward_duration/1000
                if self.action == "6":
                    translation[0] = -RETREAT_DISTANCE
                    translation[1] = -SHIFT_DISTANCE * forward_duration/1000

                



            angle = rotation

            # Update head angle
            if 'head_angle' in outcome:
                head_angle = outcome['head_angle']
                if self.action == "-" or self.action == "*" or self.action == "+":
                    print("Create a new echo interaction")
                    echo_distance = outcome['echo_distance']
                    if echo_distance > 0:  # echo measure 0 is false measure
                        obstacle = 1

            for i in range(100,-99,-10):
                    edstr = "ed"+str(i)

                    if edstr in outcome:
                        ha =i
                        ed = outcome[edstr]
                        tmp_x = ROBOT_HEAD_X + math.cos(math.radians(ha)) * ed
                        tmp_y = math.sin(math.radians(ha)) * ed
                        echo_array.append((tmp_x, tmp_y))
                        #print("ha :",ha,"ed :",ed, "tmp_x :",tmp_x,"tmp_y :",tmp_y)

            phenom_info = (floor,shock,blocked,obstacle,x,y)

        # Update the azimuth
        if 'azimuth' in outcome:
            self.azimuth = outcome['azimuth']
            #print("self az : ", self.azimuth)
        else:
            self.azimuth -= rotation

        angle = rotation

        outcome = dict()
        outcome['translation'] = translation
        outcome['rotation'] = rotation
        outcome['angle'] = angle
        outcome['floor'] = floor
        outcome['shock'] = shock
        outcome['blocked'] = blocked
        outcome['obstacle'] = obstacle,x,y
        return  outcome





    def command_robot(self, action):
        """ Creating an asynchronous thread to send the action to the robot and to wait for outcome """
        self.outcome_bytes = "Waiting"

        def enact_thread():
            """ Sending the action to the robot and waiting for outcome """
            action_string = json.dumps({'action': self.action, 'angle': self.action_angle})
            print("Sending: " + action_string)
            self.outcome_bytes = self.wifiInterface.enact(action_string)
            print("Receive ", end="")
            print(self.outcome_bytes)
            self.enact_step = 2

        self.action = action
        self.enact_step = 1
        thread = threading.Thread(target=enact_thread)
        thread.start()

        # Cas d'actions particulières :
        if action == "r":
            self.action_reset()