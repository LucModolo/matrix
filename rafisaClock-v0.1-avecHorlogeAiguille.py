# rafisaClock-v0.1.py
# -------------------
# horloge d'affichage pour la zone accueil de Rafisa
# Basée sur rpi-rgb-led-matrix/bindings/pythons/samples/runtext.py (GIT https://github.com/hzeller)
# -------------------
# v0.1 : 18.01.2020 / PAR : reprise du programme et intégration de l'heure digitale et l'image 

# Pour tester .
# cd rpi-rgb-led-matrix/bindings/python/samples/
# sudo python3 rafisaClock-v0.1.py --led-rows=64 --led-cols=64 --led-slowdown-gpio=4

#!/usr/bin/env python

# Librairies de base pour LED Matrix
from samplebase import SampleBase
from rgbmatrix import graphics

# Librairie pour affichage d'une image
from PIL import Image

# Librairie pour le temps et date/heure
import time, datetime, math


class RafisaClock(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RafisaClock, self).__init__(*args, **kwargs)
        #self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Rafisa Horloge v0.1")
        self.parser.add_argument("-i", "--image", help="The image to display", default="/home/pi/rpi-rgb-led-matrix/bindings/python/samples/logorafisa64.ppm")

    def run(self):
        if not 'image' in self.__dict__:
            self.image = Image.open(self.args.image).convert('RGB')
        
        self.image.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
        
        double_buffer = self.matrix.CreateFrameCanvas()
        img_width, img_height = self.image.size
        
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        
        fontHeure = graphics.Font()
        fontHeure.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/7x13.bdf")
        fontDate = graphics.Font()
        fontDate.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x9.bdf")
                
        textColor = graphics.Color(255, 255, 0)
        heureColor = graphics.Color(100,100,100)
        black = graphics.Color(0,0,0)
        
        typeClock = 1

        while True:
            
            #effacement de la zone de texte
            for i in range(19,64):
                graphics.DrawLine(offscreen_canvas, 0, i, 64, i, black)

            if typeClock == 1:
                my_textJourS = datetime.datetime.now().strftime("%A") 
                my_textDateJ = datetime.datetime.now().strftime("%d/%m/%Y")
                my_textHeure = datetime.datetime.now().strftime("%H:%M:%S")
                
                nbCar = len(my_textJourS)
                lenW = graphics.DrawText(offscreen_canvas, fontDate, (64-((nbCar*4)+(nbCar-1)*2))/2, (64+9)/2 - 10, textColor, my_textJourS)
                nbCar = len(my_textDateJ)
                lenD = graphics.DrawText(offscreen_canvas, fontDate, (64-((nbCar*4)+(nbCar-1)*2))/2, (64+9)/2, textColor, my_textDateJ)
                nbCar = len(my_textHeure)
                lenH = graphics.DrawText(offscreen_canvas, fontHeure, (64-((nbCar*6)+(nbCar-1)*1))/2, (64+9)/2+25, heureColor, my_textHeure)
            
            if typeClock == 2:
                # voir http://pedagogie.cegepoutaouais.qc.ca/fsthilaire/leve_topo_II/5_ressources/revision_station_totale/5_calcul_main/default.aspx
                stationX = 32
                stationY = 42

                # aiguille longueurs
                secondesLong = 20   
                minutesLong = 22    
                heuresLong = 18      

                graphics.DrawLine(offscreen_canvas, stationX-1, stationY-1, stationX+1, stationY-1, textColor)
                graphics.DrawLine(offscreen_canvas, stationX+1, stationY-1, stationX+1, stationY+1, textColor)
                graphics.DrawLine(offscreen_canvas, stationX-1, stationY+1, stationX+1, stationY+1, textColor)
                graphics.DrawLine(offscreen_canvas, stationX-1, stationY-1, stationX-1, stationY+1, textColor)
                

                
                # aiguille couleurs
                secondesCol = graphics.Color(80,20,20)
                minutesCol = graphics.Color(255,255,255)
                heuresCol = graphics.Color(0,100,100)

                # recup valeurs
                my_secondes = datetime.datetime.now().second
                my_minutes = datetime.datetime.now().minute
                my_heures = datetime.datetime.now().hour
                if my_heures > 12:
                    my_heures = my_heures -12
                print(str(my_heures) + ":" + str(my_minutes) + ":" + str(my_secondes))

                # facteurs de correction
                secondesCorrection = 10
                minutesCorrection = 0
                heuresCorrection = 0
                
                # angle entre point 0 degrés et les valeurs
                secondesDeg = (360/60) * my_secondes + 180 + secondesCorrection
                minutesDeg  = (360/60) * my_minutes + 180 + minutesCorrection
                heuresDeg   = (360/12) * my_heures + 180 + heuresCorrection
                
                secondesRad = math.radians(secondesDeg)
                minutesRad = math.radians(minutesDeg)
                heuresRad = math.radians(heuresDeg)
                
                secondesRad = -secondesRad         # inversion de l'angle pour que les aiguilles tournent dans le bon sens
                minutesRad = -minutesRad
                heuresRad = -heuresRad
                
                # calcul coordonnées des aiguilles et affichage
                pointsY = stationY + math.cos(secondesRad) * secondesLong
                pointsX = stationX + math.sin(secondesRad) * secondesLong
                pointmY = stationY + math.cos(minutesRad) * minutesLong
                pointmX = stationX + math.sin(minutesRad) * minutesLong
                pointhY = stationY + math.cos(heuresRad) * heuresLong
                pointhX = stationX + math.sin(heuresRad) * heuresLong
                graphics.DrawLine(offscreen_canvas, stationX, stationY, pointsX, pointsY, secondesCol)
                graphics.DrawLine(offscreen_canvas, stationX, stationY, pointmX, pointmY, minutesCol)
                graphics.DrawLine(offscreen_canvas, stationX, stationY, pointhX, pointhY, heuresCol)
                
            double_buffer.SetImage(self.image, 1)
            double_buffer = self.matrix.SwapOnVSync(double_buffer)

            time.sleep(1.0)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    rafisa_clock = RafisaClock()
    if (not rafisa_clock.process()):
        rafisa_clock.print_help()
