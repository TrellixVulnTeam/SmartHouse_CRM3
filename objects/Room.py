import pygame
import os
class Room:
    def __init__(self,name):
        self.images = {}
        self.name = name
        self.cold_transparency = 0
        self.hot_transparency = 0
        self.light_transparency = 100
        self.job= {}
        self.temperature = 0
        self.text_pos = []
        for e in ["light","cold","hot"]:
            self.images[e] = pygame.image.load(os.path.join(os.getcwd(), "resources", "images", self.name+"-"+e+".png"))

    def blit_alpha(self,target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)
    def update(self,tick):
        if self.job:
            if self.job["type"] == "light":
                self.light_transparency += (self.job["transparency_set_to"]-self.job["transparency_was"])/self.job["total_time"]*tick
            elif self.job["type"] == "hot":
                self.hot_transparency += (self.job["transparency_set_to"]-self.job["transparency_was"])/self.job["total_time"]*tick
            elif self.job["type"] == "cold":
                self.cold_transparency += (self.job["transparency_set_to"]-self.job["transparency_was"])/self.job["total_time"]*tick
            elif self.job["type"] == "temperature":
                self.temperature += (self.job["transparency_set_to"] - self.job["transparency_was"]) / self.job["total_time"]*tick
                if self.temperature<22:
                    self.cold_transparency = abs((22-self.temperature)*5)
                    self.hot_transparency = 0
                else:
                    self.hot_transparency = (self.temperature-22)*5
                    self.cold_transparency = 0

            self.job["time"] -= tick
            print(self.job["time"]<=0)
            if self.job["time"] <=0: self.job = None

    def set_transparency(self,type,set_to,time=0):
        self.job = {"time": time, "type": type, "transparency_set_to": set_to, "transparency_was": 0,"total_time": time}
        if type == "light": self.job["transparency_was"] = self.light_transparency
        elif type == "hot": self.job["transparency_was"] = self.hot_transparency
        elif type == "cold":self.job["transparency_was"] = self.cold_transparency
        elif type == "temperature": self.job["transparency_was"] = self.temperature
    def draw(self,surface,tick):
        self.update(tick)
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(str(int(self.temperature))+"°", False, pygame.Color("red") if self.temperature<22 else pygame.Color("blue"))
        res = surface.copy()
        self.blit_alpha(res, self.images["light"], (0, 0), self.light_transparency)
        self.blit_alpha(res, self.images["hot"], (0, 0), self.hot_transparency)
        self.blit_alpha(res, self.images["cold"], (0, 0), self.cold_transparency)
        res.blit(textsurface,self.text_pos)
        return res
