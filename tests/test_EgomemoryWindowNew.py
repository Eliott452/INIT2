# By Olivier GEORGEON 15 March 2022

import sys
import json
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

    # ego_view = EgocentricView()
    ego_controller = CtrlView(workspace)
    ego_view = ego_controller.view

    # memory = MemoryV1()
    #hexa_memory = HexaMemory(width=40, height=80, cell_radius=50)
    agent_act = Agent5()
    #agent = Agent6(memory, hexa_memory)
    #hexaview = HexaView(cell_radius=hexa_memory.cell_radius)

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
                workspace.intended_interaction = intended_interaction
                # workspace.agent_action = text
                # workspace.action_angle = ego_controller.mouse_press_angle
                # robot_controller.action_angle = ego_controller.mouse_press_angle
                robot_controller.command_robot(intended_interaction)
            else:
                print("Waiting for previous outcome before sending new action")

    def main_loop(dt):
        """ Watch for the end of the previous interaction and choose the next """
        if robot_controller.enact_step == 2:
            # Update the egocentric memory window
            # phenom_info, angle, translation, controller.outcome, echo_array, head_angle, azimuth, status = robot_controller.translate_robot_data()
            robot_controller.robot_data = robot_controller.translate_robot_data()
            enacted_interaction = robot_controller.robot_data
            status = enacted_interaction["status"]
            if status != "T":
                robot_controller.send_position_change_to_memory()
                robot_controller.send_phenom_info_to_memory()
                ego_controller.update_model(enacted_interaction)
                # controller.memory.tick()
                # ego_controller.extract_and_convert_interactions(memory)
                # controller.hexaview.extract_and_convert_interactions(controller.hexa_memory)
                # controller.azimuth = azimuth
                # controller.send_position_change_to_hexa_memory(angle, translation)
                # controller.ask_synthetizer_to_act()

                # Displace the points of interest
                # ego_controller.displace(displacement_matrix)
                # ego_controller.add_point_of_interest(0, 0, POINT_PLACE)
                # ego_controller.rotate_head(head_angle)

                # ego_controller.extract_and_convert_interactions(memory)
                # ego_view.azimuth = azimuth  # TODO Use the EgoController
                # controller.main_refresh()
            robot_controller.enact_step = 0

        if control_mode == CONTROL_MODE_AUTOMATIC:
            if robot_controller.enact_step == 0:
                # Retrieve the previous outcome
                outcome = 0
                json_outcome = json.loads(robot_controller.outcome_bytes)
                if 'floor' in json_outcome:
                    outcome = json_outcome['floor']
                if 'shock' in json_outcome:
                    if json_outcome['shock'] > 0:
                        outcome = json_outcome['shock']

                # Choose the next action
                action = agent_act.action(outcome)
                robot_controller.command_robot(['8', '1', '3'][action])

    # Schedule the main loop that updates the agent
    pyglet.clock.schedule_interval(main_loop, 0.1)

    # Run all the windows
    pyglet.app.run()
