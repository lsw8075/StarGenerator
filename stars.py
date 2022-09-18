from random import uniform
from math import sqrt, log10, acos, atan2, pi
import numpy as np
import matplotlib.pyplot as plt
import csv

class StarList:
    def __init__(self, starlist):
        self.slist = starlist

    def get(self):
        return self.slist

    def save(self, filename='stars.csv'):
        with open(filename, 'w', newline='') as csvfile:
            w = csv.writer(csvfile, delimiter=',')
            for star in self.slist:
                w.writerow(star)

    def load(filename='stars.csv'):
        with open(filename, newline='') as csvfile:
            rows = csv.reader(csvfile, delimiter=',')
            slist = []
            for row in rows:
                slist.append([
                    int(row[0]),
                    float(row[1]),
                    float(row[2]),
                    float(row[3]),
                    float(row[4]),
                    float(row[5]),
                    float(row[6]),
                    float(row[7]),
                    float(row[8]),
                    ])
            return StarList(slist)

    def draw(self, filename='stars.png'):
        # prepare data
        # change this expr to change draw setting
        calsize = (lambda m: ((6 - m) ** 4) * 0.03)
        data = np.array(self.slist).T
        mag = np.array(data[1])
        lati = np.array(data[7])
        longi = np.array(data[8])
        size = np.array([calsize(mag[i]) for i in range(len(mag))])
        # draw
        fig, ax = plt.subplots()
        ax.scatter(longi, lati, s=size, c='white')
        ax.set_facecolor('black')
        ax.set_xlim(-180, 180)
        ax.set_ylim(-90, 90)
        ax.set_xticks([i for i in range(-180, 180, 30)])
        ax.set_yticks([i for i in range(-90, 90, 30)])
        ax.grid(axis='x', color='white', linewidth=1, which='major')
        ax.grid(axis='y', color='white', linewidth=1, which='major')
        ax.set_xticks([i for i in range(-180, 180, 5)], minor=True)
        ax.set_yticks([i for i in range(-90, 90, 5)], minor=True)
        ax.grid(axis='x', color='white', linewidth=0.3, which='minor')
        ax.grid(axis='y', color='white', linewidth=0.3, which='minor')
        ax.tick_params(labelsize=20)
        fig.set_size_inches(100, 50)
        plt.tight_layout()
        fig.savefig('stars.png', dpi=100)

# constants
PARSEC = 500    # generating parsec
LY = 3.26156    # LY/pc
DEG = 180 / pi  # rad to deg

class StarGen:
    def __init__(self, density=1):
        # density : star density compared to near earth
        # starnum : count of stars generated
        # star statistics: abs.mag -7 ~ 9
        # from G. Ledrew, <The Real Starry Sky>
        stat = [1, 10, 60, 290, 1300, 5000, 25000,
            100000, 300000, 500000, 1200000, 1700000,
            2900000, 3000000, 3200000, 3300000, 4200000]
        self.starnum = [round(x*density) for x in stat]

    # calculate apparent magnitude 
    def calcapp(absol, radius):
        diff = 5 * (log10(radius) - 1)
        return absol + diff

    # generate random star position
    def genpos():
        x = uniform(-PARSEC, PARSEC)
        y = uniform(-PARSEC, PARSEC)
        z = uniform(-PARSEC, PARSEC)
        r = sqrt(x*x+y*y+z*z)
        return (r, x, y, z,
                (pi/2 - acos(z/r)) * DEG,
                atan2(y, x) * DEG)

    # generate stars
    def generate(self, maxmag=6, rnd=2):
        # maxmag : max apparent magnitude
        starlist = []
        for absol, num in enumerate(self.starnum, start=-7):
            for star in range(num):
                # gen rand star pos
                s = StarGen.genpos()
                # add variance on absolute magnitude
                vabm = absol + uniform(-0.5, 0.5)
                app = StarGen.calcapp(vabm, s[0])
                if app <= maxmag:
                    starlist.append([0,
                        round(app, rnd),
                        round(vabm, rnd),
                        round(s[0] * LY, rnd),
                        round(s[1] * LY, rnd),
                        round(s[2] * LY, rnd),
                        round(s[3] * LY, rnd),
                        round(s[4], rnd),
                        round(s[5], rnd)
                        ])
        slist = sorted(starlist, key=lambda x: x[1])
        for i in range(len(slist)):
            slist[i][0] = i + 1
        return StarList(slist)


#StarGen(5).generate().save()
#StarList.load().draw()
