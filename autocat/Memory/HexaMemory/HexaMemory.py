import sys
import os
# sys.path.insert(1, os.path.join(sys.path[0], '..'))
from ast import match_case
import math
from . HexaGrid import HexaGrid


class HexaMemory(HexaGrid):
    """Hexa memory is an allocentric memory, made with an hexagonal grid.
    You can find informations on the hexagonal grid coordinates system in the docs
    folder.
    """

    def __init__(self, width, height, cell_radius=50, robot_width=200):
        """Construct the HexaMemory of the robot, child class of HexaGrid
        with the addition of the robot at the center of the grid and a link between the
        software and the real word, cell_radius representing the radius of a cell in the real world (in millimeters)
        """
        super().__init__(width, height)
        self.cell_radius = cell_radius
        self.robot_cell_x = self.width // 2
        self.robot_cell_y = self.height // 2
        self.robot_pos_x = 0
        self.robot_pos_y = 0
        self.robot_width = robot_width
        self.grid[self.robot_cell_x][self.robot_cell_y].occupy()
        self.robot_angle = 90
        self.orientation = 0
        self.update_orientation()
        self.azimuth = 0
        self.cells_changed_recently = []

    def reset(self):
        """Reset the hexamemory"""
        super().__init__(self.width, self.height)
        self.robot_cell_x = self.width // 2
        self.robot_cell_y = self.height // 2
        self.robot_pos_x = 0
        self.robot_pos_y = 0
        self.grid[self.robot_cell_x][self.robot_cell_y].occupy()
        self.robot_angle = 90
        self.orientation = 0
        self.azimuth = 0
        self.update_orientation()
        self.cells_changed_recently = []

    def update_orientation(self):
        "update the orientation of the robot based on its angle"
        angle = self.robot_angle
        if angle <= 60:
            self.orientation = 1
            return
        if angle <= 120:
            self.orientation = 0
            return
        if angle <= 180:
            self.orientation = 5
            return
        if angle <= 240:
            self.orientation = 4
            return
        if angle <= 300:
            self.orientation = 3
            return
        self.orientation = 2

    def convert_pos_in_cell(self,pos_x, pos_y):
        """Convert an allocentric position to cell coordinates."""
        radius = self.cell_radius
        mini_radius = math.sqrt(radius**2 - (radius/2)**2)
        tmp_cell_x = self.width // 2
        tmp_cell_y = self.height // 2
        tmp_cell_x_center = 0
        tmp_cell_y_center = 0
        # Do the regular part of translation :
        # to go to the next cell on the right/left you move by 3*radius on the x axis.
        x_sign = 1
        if pos_x < 0 :
            x_sign = -1
        y_sign = 1
        if pos_y < 0 :
            y_sign = -1
        while abs(pos_x) >= abs(3*radius) :
            tmp_cell_x += x_sign
            pos_x -= (3*radius) * x_sign
            tmp_cell_x_center += (3*radius) * x_sign
        #To move to the cell on the top/bottom you move by 2*mini_radius on the y axis. 
        while abs(pos_y) >= abs(2*mini_radius) :
            tmp_cell_y += 2*y_sign
            pos_y -= 2*mini_radius*y_sign
            tmp_cell_y_center += 2*mini_radius*y_sign
        # Elimination pour trouver dans quel voisin de la cellule courante on est
        distance = math.sqrt(pos_x**2 + pos_y**2)
        if(distance <= mini_radius): # On est forcement dans la bonne pos
            return tmp_cell_x, tmp_cell_y
        if distance <= radius :
            "determiner la ligne qui risque d'etre traversée, et si on a passé la ligne ou non"
        if abs(pos_x) >= 2.5 * radius:
            "on est forcément dans g hgg bgg ou d hdd bdd"
            if abs(pos_y) >= mini_radius :
                "on est forcement dans hgg bgg hdd bdd"
                return tmp_cell_x+ x_sign, tmp_cell_y + 2*y_sign
            else :
                "on est dans g ou d"
                return tmp_cell_x + x_sign, tmp_cell_y

        if abs(pos_x) >= 2 * radius :
            "on est dans hgg g bgg hg bg / hdd d bdd hd bd "
            if abs(pos_y) >= mini_radius :
                "on est dans hgg-hg  bgg-bg  hdd-hd bd-bdd"
                # On trouve l'équation de la ligne de démarcation
                x_depart = 2.5 * radius
                y_depart = mini_radius

                x_fin = 2* radius
                y_fin = 2*mini_radius

                slope = (y_fin - y_depart) / (x_fin - x_depart)
                offset = y_depart - (slope * x_depart)

                y_ref = abs(pos_x) * slope + offset

                if abs(pos_y) <= abs(y_ref) :
                   "on est dans hg hd bg bd"
                   return self.find_coordinates_corner(tmp_cell_x,tmp_cell_y, x_sign,y_sign)
                else :
                   "on est dans hgg bgg hdd bdd"
                   return tmp_cell_x+ x_sign, tmp_cell_y + 2*y_sign
                # sauf erreur, si on met tout en valeur absolue on obtient toujours une pente descendante
                # il faut donc juste regarder si le y du point est inférieur ou supérieur au 
                # y correspondant au x sur l'equation de droite

            else : 
                "on est dans hd ou d (ou equivalent)"
                # On trouve l'équation de la ligne de démarcation
                x_depart = 2.5 * radius
                y_depart = mini_radius

                x_fin = 2* radius
                y_fin = 0

                slope = (y_fin - y_depart) / (x_fin - x_depart)
                offset = y_depart - (slope * x_depart)

                y_ref = abs(pos_x) * slope + offset

                # sauf erreur, si on met tout en valeur absolue on obtient toujours une pente ascendante
                # il faut donc juste regarder si le y du point est inférieur ou supérieur au 
                # y correspondant au x sur l'equation de droite
                if abs(pos_y) >= abs(y_ref) :
                   "on est dans hd"
                   return self.find_coordinates_corner(tmp_cell_x,tmp_cell_y, x_sign,y_sign)
                else :
                   "on est dans d"
                   return tmp_cell_x+ x_sign, tmp_cell_y
            
        if abs(pos_x)> radius and abs(pos_x)< 2*radius :
            "on est dans hd"
            return self.find_coordinates_corner(tmp_cell_x,tmp_cell_y, x_sign,y_sign)
        if abs(pos_x) > radius/2 and abs(pos_x)<= 2*radius:
            # on est dans c, h ou hd
            x1 = radius
            y1 = 0

            x2 = radius/2
            y2 = mini_radius

            x3 = radius
            y3= 2*mini_radius

            slope1 = (y1 - y2) / (x1 - x2)
            offset1 = y2 - (slope1 * x2)
            y_ref1 = slope1 * pos_x + offset1

            slope2 = (y3 - y2) / (x3 - x2)
            offset2 = y2 - (slope2 * x2)
            y_ref2 = slope2 * pos_x + offset2


            if abs(pos_y) >= y_ref1 and abs(pos_y) <= y_ref2:
                # on est dans hd
                return self.find_coordinates_corner(tmp_cell_x,tmp_cell_y, x_sign,y_sign)
        if abs(pos_y)>mini_radius :
            return tmp_cell_x, tmp_cell_y + y_sign*2
        else :
            return tmp_cell_x, tmp_cell_y




    def convert_cell_to_pos(self,cell_x, cell_y):
        """Return the allocentric position of the center of the given cell."""
        radius = self.cell_radius
        mini_radius = math.sqrt(radius**2 - (radius/2)**2)
        start_x = self.width //2
        change_x = cell_x - start_x
        start_y = self.height //2
        change_y = cell_y - start_y
        pos_x = 3 * radius * change_x
        pos_y = 0
        reste = 0
        if change_y % 2 == 0 :
            pos_y = mini_radius * change_y
        else :
            signe =  (change_y/abs(change_y))
            pos_y = mini_radius * (change_y - signe)
            reste = signe

        if reste != 0 :
            y_arrivee = (change_y - signe) + start_y
            signe_x = 1 if y_arrivee % 2 == 0 else -1
            pos_x += signe_x * (3/2)*radius
            pos_y += signe* mini_radius 

        return int(pos_x), int(pos_y)
    def find_coordinates_corner(self,cell_x,cell_y,x_sign,y_sign):
        """aaaaaaaaa"""
        f_x, f_y =0,0
        y_even =cell_y % 2 == 0
        if(y_even):
            if(x_sign > 0):
                f_x = cell_x
            else :
                f_x = cell_x - 1

        else :
            if(x_sign > 0):
                f_x = cell_x+1
            else :
                f_x = cell_x

        if(y_sign > 0):
            f_y = cell_y +1 
        else :
            f_y = cell_y - 1

        return f_x,f_y
        


    def move(self, rotation, move_x, move_y,is_egocentric_translation= True):
        """Handle movement of the robot in the hexamemory"""
        self.rotate_robot(rotation)
        rota_radian = math.radians(self.robot_angle)
        x_prime = 0
        y_prime = 0
        if(is_egocentric_translation):
            x_prime = int(move_x * math.cos(rota_radian) - move_y * math.sin(rota_radian))  # OG 27/08/2022
            y_prime = int(move_x * math.sin(rota_radian) + move_y * math.cos(rota_radian))
        else :
            x_prime = move_x
            y_prime = move_y
        x_prime += self.robot_pos_x
        y_prime += self.robot_pos_y
        try :
            self.apply_changes(self.robot_pos_x, self.robot_pos_y, x_prime, y_prime)
            self.robot_pos_x = x_prime
            self.robot_pos_y = y_prime          
        except IndexError:
            print("IndexError")
            self.robot_cell_x = self.width // 2
            self.robot_cell_y = self.height // 2
            self.robot_pos_x = 0
            self.robot_pos_y = 0
        if self.grid[self.robot_cell_x][self.robot_cell_y] != 'Frontier':
            self.grid[self.robot_cell_x][self.robot_cell_y].set_to('Free')
        self.grid[self.robot_cell_x][self.robot_cell_y].leave()
        self.cells_changed_recently.append((self.robot_cell_x, self.robot_cell_y))
        self.robot_cell_x, self.robot_cell_y = self.convert_pos_in_cell(
            self.robot_pos_x, self.robot_pos_y)
        self.grid[self.robot_cell_x][self.robot_cell_y].occupy()
        self.cells_changed_recently.append((self.robot_cell_x, self.robot_cell_y))
        return x_prime, y_prime

    def apply_phenomenon(self, phenomenon, pos_x, pos_y):
        """Apply a phenomenon to the grid
        Args :
            phenomenon : type of phenomenon (TODO: but should be things like "line", "unmovable object", "movable object", etc.)
            pos_x, pos_y : position of the phenomenon (relative to the robot's position)
        """

    def rotate_robot(self, rotation):
        """Rotate the representation of the robot by the given angle.

        :Parameters:
            `rotation` : int, degrees of rotation
        """
        self.robot_angle = (self.robot_angle + rotation)
        while self.robot_angle < 0:
            self.robot_angle = 360 + self.robot_angle
        self.robot_angle = self.robot_angle % 360
        if(360-(self.robot_angle-90)  < self.azimuth -10 or 360-(self.robot_angle-90) > self.azimuth+10):
            self.robot_angle = 360 - self.azimuth +90
        self.update_orientation()

    def get_robot_pos(self):
        """Return the position of the robot. (cell coordinates)"""
        return self.robot_cell_x, self.robot_cell_y


    def apply_changes(self, start_x, start_y, end_x, end_y, status="Free"):
        """Apply the given status (Free by default) to every cell between coordinates start_x,start_y and end_x,end_y"""

        distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        if distance == 0:
            return
        nb_step = int(distance / (self.cell_radius))
        if nb_step == 0:
            return
        step_x = int((end_x - start_x)/nb_step)
        step_y = int((end_y - start_y)/nb_step)
        current_pos_x = start_x
        current_pos_y = start_y
        for _ in range(nb_step):
            cell_x, cell_y = self.convert_pos_in_cell(
                current_pos_x, current_pos_y)
            # if(self.grid[cell_x][cell_y].status == "Unknown"):
            if self.grid[cell_x][cell_y].status != "Frontier":
                self.grid[cell_x][cell_y].status = status
            self.grid[cell_x][cell_y].leave()
            self.cells_changed_recently.append((cell_x, cell_y))
            current_pos_x += step_x
            current_pos_y += step_y


    def change_cell(self, cell_x, cell_y,status):
        """Change the status of the cell at the given coordinates"""
        self.grid[cell_x][cell_y].status = status
        self.cells_changed_recently.append((cell_x,cell_y))

    def convert_egocentric_translation_to_allocentric(self,translation_x,translation_y):
        """Convert the given translation from egocentric to allocentric coordinates"""
        rota_radian = math.radians(self.robot_angle)
        x_prime = int(translation_x * math.cos(rota_radian) - translation_y * math.sin(rota_radian))
        y_prime = int(translation_x * math.sin(rota_radian) + translation_y * math.cos(rota_radian))
        return x_prime,y_prime

    def convert_allocentric_position_to_egocentric_translation(self,position_x,position_y):
        """Use the give position to compute an allocentric translation from the robot position, then convert This
        allocentric translation to an egocentric translation"""
        #Compute the allocentric translation
        translation_x = position_x - self.robot_pos_x
        translation_y = position_y - self.robot_pos_y
        #Convert the allocentric translation to an egocentric translation
        rota_radian = -math.radians(self.robot_angle)
        x_prime = int(translation_x * math.cos(rota_radian) - translation_y * math.sin(rota_radian))
        y_prime = int(translation_x * math.sin(rota_radian) + translation_y * math.cos(rota_radian))
        return x_prime,y_prime
        
    def convert_egocentric_position_to_allocentric(self,position_x,position_y):
        """Convert the given position from egocentric to allocentric coordinates"""
        translation_x,translation_y = self.convert_egocentric_translation_to_allocentric(position_x,position_y)
        return self.robot_pos_x + translation_x, self.robot_pos_y + translation_y

    def apply_translation_to_robot_pos(self,translation_x,translation_y):
        """Apply the given translation to the robot's position"""
        self.move(0,translation_x,translation_y,is_egocentric_translation = False)

    def apply_status_to_cell(self,cell_x, cell_y,status):
        self.grid[cell_x][cell_y].status = status
        self.cells_changed_recently.append((cell_x,cell_y))


    def apply_status_to_rectangle(self, center_x,center_y,width,height, status):
        """Apply the given status to every cell in the rectangle defined by the given center and width/height"""
        max_x = center_x + width/2 if center_x + width / 2 < self.width/2 * self.cell_radius * 2 else self.width * self.cell_radius
        max_y = center_y + height/2 if center_y + height / 2 < self.height/2 * self.cell_radius * 1.7 else self.height * self.cell_radius
        min_x = center_x - width/2 if center_x - width / 2 > 0 - self.width/2 * self.cell_radius * 2  else 0 - self.width/2 * self.cell_radius * 2
        min_y = center_y - height/2 if center_y - height / 2 > 0 - self.height/2 * self.cell_radius * 1.7 else 0 - self.height/2 * self.cell_radius * 1.7
        for x in range(int(min_x), int(max_x), self.cell_radius):
            for y in range(int(min_y), int(max_y), self.cell_radius):
                cell_x, cell_y = self.convert_pos_in_cell(x, y)
                self.apply_status_to_cell(cell_x, cell_y, status)

