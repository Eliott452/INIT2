# By Olivier GEORGEON 15 March 2022

import sys
from stage_titouan import *
from stage_titouan.Agent.Agent5 import Agent5

CONTROL_MODE_MANUAL = 0
CONTROL_MODE_AUTOMATIC = 1
control_mode = CONTROL_MODE_MANUAL
print("Control mode: MANUAL")


# Testing ControllerNew by remote controlling the robot from the EgoMemoryWindowNew
# py -m tests.test_EgomemoryWindowNew <ROBOT_IP>
if __name__ == "__main__":
    ip = "192.168.1.11"
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    else:
        print("Please provide your robot's IP address")
    print("Sending to: " + ip)

    workspace = Workspace()
    robot_controller = CtrlRobot(workspace, ip)

    ego_controller = CtrlView(workspace)
    ego_view = ego_controller.view
    agent = Agent5()

    ctrl_hexaview = CtrlHexaview(workspace)
    ctrl_synthe = CtrlSynthe(workspace)

    # synthesizer = CtrlSynthe(workspace)
    # controller = CtrlRobot(agent, memory, ip, view=ego_view, synthesizer = synthesizer, hexa_memory = hexa_memory, hexaview = hexaview)
    # controller.hexaview.extract_and_convert_interactions(controller.hexa_memory)

    @ego_view.event
    def on_text(text):
        global control_mode
        if text.upper() == "A":
            control_mode = CONTROL_MODE_AUTOMATIC
            print("Control mode: AUTOMATIC")
        elif text.upper() == "M":
            control_mode = CONTROL_MODE_MANUAL
            print("Control mode: MANUAL")

        if control_mode == CONTROL_MODE_MANUAL:
            if robot_controller.enact_step == 0:
                intended_interaction = {'action': text, 'angle': ego_controller.mouse_press_angle}
                # workspace.intended_interaction = intended_interaction
                robot_controller.command_robot(intended_interaction)
            else:
                print("Waiting for previous outcome before sending new action")

    def main_loop(dt):
        """ Watch for the end of the previous interaction and choose the next """
        if robot_controller.enact_step == 2:
            # Update the egocentric memory window
            enacted_interaction = robot_controller.translate_robot_data()
            if enacted_interaction["status"] != "T":
                ego_controller.update_model(enacted_interaction)
            robot_controller.enact_step = 0

        if control_mode == CONTROL_MODE_AUTOMATIC:
            if robot_controller.enact_step == 0:
                # Construct the outcome expected by Agent5
                enacted_interaction = robot_controller.translate_robot_data()
                outcome = 0
                if 'floor' in enacted_interaction:
                    outcome = int(enacted_interaction['floor'])
                if 'shock' in enacted_interaction:
                    if enacted_interaction['shock'] > 0:
                        outcome = enacted_interaction['shock']

                # Choose the next action
                action = agent.action(outcome)
                intended_interaction = {'action': ['8', '1', '3'][action]}
                robot_controller.command_robot(intended_interaction)

    # Schedule the main loop that updates the agent
    pyglet.clock.schedule_interval(main_loop, 0.1)

    # Run all the windows
    pyglet.app.run()
