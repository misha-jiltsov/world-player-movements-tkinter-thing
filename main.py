import random
import tkinter as tk
import random as rd


class Game:
    def __init__(self, master):
        pos = ["up", "down", "left", "right"]
        self.sprites = {
            "green": "ground",
            "grey": "rock",
            "dark green": "tree",
            "brown": "stick",
        }
        self.playerinv = {
            "sticks": 0,
            "rocks": 0
        }
        self.sprinting = False
        self.energy = 10
        self.move_dist = 1
        self.playerposinworld = [15, 10]
        self.button_frame = tk.Frame(master, padx=30, pady=150)
        self.button_frame.grid(column=0, row=0)
        self.control_buttons = [
            tk.Button(self.button_frame, text=pos[i], width=10, height=4, command=lambda i=pos[i]: self.on_clicked(i))
            for i in range(4)]
        self.world = [[None for i in range(100)] for i in range(100)]
        self.create_world()


        self.display_frame = tk.Frame(master, borderwidth=3, relief="solid")
        self.display_frame.grid(column=1, row=0)
        self.display_tiles = [[tk.Label(self.display_frame, width=2, bg="white") for i in range(31)] for i in range(21)]

        for i, row in enumerate(self.display_tiles):
            for j, pixel in enumerate(row):
                pixel.grid(column=j, row=i)

        self.control_buttons[0].grid(column=0, row=1)
        self.control_buttons[1].grid(column=1, row=1)
        self.control_buttons[2].grid(column=0, row=2)
        self.control_buttons[3].grid(column=1, row=2)

        self.update_screen()

        self.inf_frame = tk.Frame()
        self.inf_frame.grid(row=0, column=2)
        self.inv_label = tk.Label(self.inf_frame,
                                  text=f"sticks: {self.playerinv['sticks']} \n rocks: {self.playerinv['rocks']}")
        self.inv_label.grid(column=0, row=2)

        self.sprint_toggle = tk.Button(self.inf_frame, width=15, text=f"Sprinting: {self.sprinting}", command = lambda : self.SprintToggle())
        self.sprint_toggle.grid(column=0, row=0)

        self.energy_label = tk.Label(self.inf_frame, text=f"energy left: {self.energy}")
        self.energy_label.grid(column=1, row=0)

    def update_screen(self):

        ## displays the world surroundings

        world_loc_start = [self.playerposinworld[0] - 15, self.playerposinworld[1] - 10]

        for row_num in range(len(self.display_tiles)):
            for pixel_num in range(len(self.display_tiles[row_num])):
                if not ((world_loc_start[0] + pixel_num < 0) or world_loc_start[0] + pixel_num > (
                        len(self.world[0]) - 1) or (world_loc_start[1] + row_num < 0) or world_loc_start[
                            1] + row_num > (len(self.world) - 1)):
                    self.display_tiles[row_num][pixel_num]["bg"] = self.world[world_loc_start[1] + row_num][
                        world_loc_start[0] + pixel_num]
                else:
                    self.display_tiles[row_num][pixel_num]["bg"] = "white"
                self.display_tiles[row_num][pixel_num].update()

        ## display player pos

        self.display_tiles[10][15]["bg"] = "blue"
        self.display_tiles[10][15].update()

        ##### updates inventory display

    def SprintToggle(self):
        if self.sprinting:
            self.sprinting = False
            self.sprint_toggle["text"] = f"Sprinting: {self.sprinting}"
            self.sprint_toggle.update()
            self.move_dist = 1
        else:
            self.sprinting = True
            self.sprint_toggle["text"] = f"Sprinting: {self.sprinting}"
            self.sprint_toggle.update()
            self.move_dist = 2

    def on_clicked(self, command):
        tile_infrnt = self.check_item(command)
        print(tile_infrnt)
        if (self.sprinting and self.energy>0) or (not self.sprinting):
         if tile_infrnt == "ground" or tile_infrnt == "stick":
             if command == "up" and self.playerposinworld[1] != 0:
                 self.playerposinworld[1] -= self.move_dist
             elif command == "down" and self.playerposinworld[1] < (len(self.world) - self.move_dist):
                 self.playerposinworld[1] += self.move_dist
             elif command == "left" and self.playerposinworld[0] != 0:
                 self.playerposinworld[0] -= self.move_dist
             elif command == "right" and self.playerposinworld[0] < (len(self.world[0]) - self.move_dist):
                 self.playerposinworld[0] += self.move_dist

             if tile_infrnt == "stick":
                 self.playerinv["sticks"] += 1
                 self.inv_label["text"] = f"sticks: {self.playerinv['sticks']} \n rocks: {self.playerinv['rocks']}"
                 self.inf_frame.update()
                 self.world[self.playerposinworld[1]][self.playerposinworld[0]] = "green"

             if self.sprinting:
              self.energy-=1
              self.energy_label["text"] = f"energy left: {self.energy}"
             elif not self.sprinting and self.energy<11:
              self.energy+=1
              self.energy_label["text"] = f"energy left: {self.energy}"
             self.energy_label.update()



        self.update_screen()

    def check_item(self, command):
        if command == "up" and self.playerposinworld[1] != 0:
            return self.sprites[self.world[self.playerposinworld[1] - self.move_dist][self.playerposinworld[0]]]
        elif command == "down" and self.playerposinworld[1] < (len(self.world) - self.move_dist):
            return self.sprites[self.world[self.playerposinworld[1] + self.move_dist][self.playerposinworld[0]]]
        elif command == "left" and self.playerposinworld[0] != 0:
            return self.sprites[self.world[self.playerposinworld[1]][self.playerposinworld[0] - self.move_dist]]
        elif command == "right" and self.playerposinworld[0] < (len(self.world[0]) - self.move_dist):
            return self.sprites[self.world[self.playerposinworld[1]][self.playerposinworld[0] + self.move_dist]]

    def create_world(self):

        for rownum in range(len(self.world)):
            for tilenum in range(len(self.world[rownum])):
                rand = rd.randint(1, 100)
                if rand < 96:
                    self.world[rownum][tilenum] = "green"
                elif rand == 96:
                    self.world[rownum][tilenum] = "grey"
                elif rand == 97 or rand == 98:
                    self.world[rownum][tilenum] = "dark green"
                elif rand == 99 or rand == 100:
                    self.world[rownum][tilenum] = "brown"

        print(self.world)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1050x450")

    game = Game(root)
    root.mainloop()
