import argparse
import cv2
import numpy as np
import pickle


OBJCOLOR, BKGCOLOR = (0, 0, 255), (0, 255, 0)
OBJCODE, BKGCODE = 1, 2
SF = 10
OBJ, BKG = "OBJ", "BKG"


def plantSeed(image):

    def drawLines(x, y, pixelType):
        if pixelType == OBJ:
            color, code = OBJCOLOR, OBJCODE
        else:
            color, code = BKGCOLOR, BKGCODE
        cv2.circle(image, (x, y), radius, color, thickness)
        cv2.circle(seeds, (x , y), radius , code, thickness)

    def onMouse(event, x, y, flags, pixelType):
        global drawing
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            drawLines(x, y, pixelType)
        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            drawLines(x, y, pixelType)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False

    def paintSeeds(pixelType):
        print("Planting", pixelType, "seeds")
        global drawing
        drawing = False
        windowname = "Plant " + pixelType + " seeds"
        cv2.namedWindow(windowname, cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback(windowname, onMouse, pixelType)
        while (1):
            cv2.imshow(windowname, image)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        cv2.destroyAllWindows()


    seeds = np.zeros((image.shape[0],image.shape[1]))

    radius = 2
    thickness = -1 # fill the whole circle
    global drawing
    drawing = False


    paintSeeds(OBJ)
    paintSeeds(BKG)

    return seeds, image


def parseArgs():
    '''
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--srcpath','-sp', help = "image source file path", default = './img_test/man.jpg')
    parser.add_argument('--outpath','-op', help = "saved image file path", default = './seeded_imgs')
    parser.add_argument('--savimgname', '-savimg', help = 'saved image name', default = 'man')

    return parser.parse_args()


if __name__ == "__main__":

    args = parseArgs()
    image = cv2.imread(args.srcpath)
    seeds, seededImage = plantSeed(image)
    cv2.imwrite('./'+args.outpath+'/'+args.savimgname+'.jpg',seededImage)
    with open('./'+args.outpath+'/'+args.savimgname+'.pkl','wb') as f:
        pickle.dump(seeds, f)
