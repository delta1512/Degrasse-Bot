from math import floor
from PIL import Image
from os import popen
from time import sleep
import random
import sys
import PIL

class Destroyer:
    final_image = []
    neighbours = ((1, 1), (-1, 1), (1, -1), (-1, -1),
                    (0, 1), (-1, 0), (1, 0), (0, -1))

    def __init__(self, imageurl):
        self.pixels = None
        self.final_image = []
        self.w, self.h = 0, 0
        try:
            outfile = '/tmp/tmp.png'
            popen('echo "False" > /tmp/done && wget -O ' + outfile + ' ' + imageurl + '&& echo "True " > /tmp/done')
            image_downloaded = False
            while not image_downloaded:
                sleep(1)
                with open('/tmp/done', 'r') as status:
                    if 'True' in status.read(5):
                        image_downloaded = True
            image = Image.open(outfile)
            self.pixels = image.load()
            self.w, self.h = image.size[0], image.size[1]
        except Exception as e:
            print('[ERROR] Error caught in ImageDestroyer __init__()')
            print(e)

    #Demonstration of performing an average
    def average(self, pixel):
        Sum = 0
        for pix in pixel:
            Sum += pix
        avg = int(round(Sum / len(pixel)))
        return avg

    #Sequence generator for pixel data
    def seq_image(self):
        for x in range(self.h):
            for y in range(self.w):
                yield self.pixels[y, x]

    #Function for enabling the reuse of the output of another function
    def prepare_reiterate(self):
        if len(self.final_image) > 0:
            tmp = Image.new('RGB', (self.w, self.h))
            tmp.putdata(self.final_image)
            self.pixels = tmp.load()
            self.final_image = []

    def check_thresh(self, thresh):
        thresh = abs(thresh)
        if thresh >= 1:
            thresh = thresh - ((thresh // 100) * 100)
            return thresh / 100
        else:
            return thresh

    def greyscale(self):
        for x in range(self.h):
            for y in range(self.w):
                pixel = self.pixels[y, x]
                avg = self.average(pixel)
                self.final_image.append((avg, avg, avg))

    def edge_jumbler(self):
        ratio = (self.w * self.h) / 256
        self.final_image = list(self.seq_image())
        for i, pix in enumerate(self.seq_image()):
            swp_target = int(floor(self.average(pix) * ratio))
            tmp = self.final_image[i]
            self.final_image[i] = self.final_image[swp_target]

    def incremental_brightness(self):
        bright = 0
        for x in range(self.h):
            for y in range(self.w):
                pixel = list(self.pixels[y, x])
                bright += 1
                if bright > 255:
                    bright -= 255
                for i in range(3):
                    pixel[i] += pixel[i] + bright
                    if pixel[i] > 255:
                        pixel[i] -= 256
                self.final_image.append(tuple(pixel))

    def random_brightness(self):
        for x in range(self.h):
            for y in range(self.w):
                pixel = list(self.pixels[y, x])
                bright = random.uniform(0, 1)
                for i in range(3):
                    pixel[i] += int(pixel[i] * bright)
                    if pixel[i] > 255:
                        pixel[i] -= 256
                self.final_image.append(tuple(pixel))

    def random_displacer(self, thresh):
        thresh = self.check_thresh(thresh)
        for x in range(self.h):
            for y in range(self.w):
                pixel = self.pixels[y, x]
                for neighbour in self.neighbours:
                    if random.uniform(0, 1) < thresh:
                        tmp = pixel
                        try:
                            self.pixels[y, x] = self.pixels[y + neighbour[0], x + neighbour[1]]
                            self.pixels[y + neighbour[0], x + neighbour[1]] = tmp
                        except:
                            pass
                        break
                self.final_image.append(pixel)

    def scratches(self, thresh, prop_length):
        thresh = self.check_thresh(thresh)
        propagation = 0
        prev = None
        for x in range(self.h):
            for y in range(self.w):
                pixel = self.pixels[y, x]
                if propagation > 0:
                    pixel = prev
                    propagation -= 1
                elif random.uniform(0, 1) < thresh:
                    prev = pixel
                    propagation = random.randint(0, prop_length)
                self.final_image.append(pixel)

    def worms(self, amount, minP, thresh):
        thresh = self.check_thresh(thresh)
        for spawn in range(amount):
            y, x = random.randint(0, self.w-1), random.randint(0, self.h-1)
            init = minP
            original = self.pixels[y, x]
            cutneighbours = self.neighbours[4:]
            choice = random.randint(1, 4)
            if choice == 1:
                chosen_neighbours = cutneighbours[0:3]
            elif choice == 2:
                chosen_neighbours = cutneighbours[1:4]
            elif choice == 3:
                chosen_neighbours = [cutneighbours[0], cutneighbours[2], cutneighbours[3]]
            else:
                chosen_neighbours = [cutneighbours[0], cutneighbours[1], cutneighbours[3]]
            while (random.uniform(0, 1) < thresh) or (init > 0):
                newy, newx = -1, -1
                while not ((0 <= newy < self.w) and (0 <= newx < self.h)):
                    nextpix = chosen_neighbours[random.randint(0, 2)]
                    newy, newx = y + nextpix[0], x + nextpix[1]
                y, x = newy, newx
                self.pixels[y, x] = original
                init -= 1
        for x in range(self.h):
            for y in range(self.w):
                self.final_image.append(self.pixels[y, x])

    def save(self, filename):
        self.final_image = [pix for pix in self.seq_image()]
        outimage = Image.new('RGB', (self.w, self.h))
        outimage.putdata(self.final_image)
        outimage.save('/tmp/' + filename + '.png')
