from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import numpy as np
from get_coordinates import FetchFrame
from PIL import Image
import io
# -----------
# VARIABLES
# -----------

g_fViewDistance = 9.
g_Width = 600
g_Height = 600

g_nearPlane = 1.
g_farPlane = 1000.

action = ""
xStart = yStart = 0.
zoom = 90.

xRotate = 685.0
yRotate = -75.0
zRotate = 0.

xTrans = 0.
yTrans = 0.


# -------------------
# SCENE CONSTRUCTOR
# -------------------

frame = FetchFrame()
tframe = iter(frame)
count = 0
def scenemodel():
    glRotate(90, 0., 0., 1.)
    arm_end = [107.598, 126.048, 59.1634]
    arm_start = [142.045, 23.9809, 299.209]
    # global joints
    # points = joints[0]
    # points = [list(data) for data in points]
    # cylinder_2p(np.array(points[1]), np.array(points[2]),50,[255,0,0,255])
    # cylinder_2p(np.array(points[2]), np.array(points[3]),50,[255,0,0,255])
    # cylinder_2p(np.array(arm_end), np.array(arm_start),200,[255,0,0,0.5])
    joints = next(tframe)
    if joints != None:
        for points in joints[:-2]:
            points = [list(data) for data in points]
            for i in range(len(points)-1):
                cylinder_2p(np.array(points[i]), np.array(points[i+1]), 50, [200, 0, 0, 0.5])
    cylinder_2p(np.array(joints[-1]), np.array(joints[-2]), 200, [200, 0, 0, 0.5])

    # glutSolidTeapot(1.)


def cylinder_2p(v1, v2, dim, color):
    # glMaterialfv(GL_FRONT, GL_DIFFUSE, [color[0], color[1], color[2], color[3]])

    v2r = v2 - v1
    z = np.array([0.0, 0.0, 1.0])
    # the rotation axis is the cross product between Z and v2r
    ax = np.cross(z, v2r)
    l = np.sqrt(np.dot(v2r, v2r))
    # get the angle using a dot product
    angle = 180.0 / 3.14 * math.acos(np.dot(z, v2r) / l)

    glPushMatrix()
    glTranslatef(v1[0], v1[1], v1[2])

    # print "The cylinder between %s and %s has angle %f and axis %s\n" % (v1, v2, angle, ax)
    glRotatef(angle, ax[0], ax[1], ax[2])
    glutSolidCylinder(dim / 10.0, l, 20, 20)
    glPopMatrix()

# --------
# VIEWER
# --------

def printHelp():
    print(
    """\n\n    
         -------------------------------------------------------------------\n
         Left Mousebutton       - move eye position (+ Shift for third axis)\n
         Middle Mousebutton     - translate the scene\n
         Right Mousebutton      - move up / down to zoom in / out\n
          Key                - reset viewpoint\n
          Key                - exit the program\n
         -------------------------------------------------------------------\n
         \n""")


def init():
    glEnable(GL_NORMALIZE)
    glLightfv(GL_LIGHT0, GL_POSITION, [.0, 200.0, 200., 0.])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [.0, .0, .0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0]);
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glShadeModel(GL_SMOOTH)
    resetView()


def resetView():
    global zoom, xRotate, yRotate, zRotate, xTrans, yTrans
    zoom = 90.
    xRotate = 685.0
    yRotate = -75.0
    zRotate = 0.
    xTrans = 0.
    yTrans = 0.
    glutPostRedisplay()


def display():
    global count
    # Clear frame buffer and depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Set up viewing transformation, looking down -Z axis
    glLoadIdentity()
    g_fViewDistance = 9
    # zoom = 70.0
    g_Width = 600
    g_Height = 600
    g_nearPlane = 1.0
    g_farPlane = 1000.0
    gluLookAt(0, 0, -g_fViewDistance, 0, 0, 0, -.1, 0, 0)  # -.1,0,0
    # print(-g_fViewDistance,zoom,g_Width,g_Height,g_nearPlane,g_farPlane)
    # Set perspective (also zoom)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(zoom, float(g_Width) / float(g_Height), g_nearPlane, g_farPlane)
    glMatrixMode(GL_MODELVIEW)
    # Render the scene
    polarView()
    scenemodel()
    # Make sure changes appear onscreen
    glutSwapBuffers()
    glReadBuffer(GL_FRONT)
    data = glReadPixels(0, 0, 600, 600, GL_RGBA, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGBA", (600, 600), data, 'raw')
    image.save('save_vid/file_'+str(count).zfill(4), 'png')
    count += 1


def reshape(width, height):
    global g_Width, g_Height
    g_Width = width
    g_Height = height
    glViewport(0, 0, g_Width, g_Height)


def polarView():
    # print(yTrans,xTrans,zRotate,xRotate,yRotate)
    glTranslatef(yTrans / 100., 0.0, 0.0)
    glTranslatef(0.0, -xTrans / 100., 0.0)
    glRotatef(-zRotate, 0.0, 0.0, 1.0)
    glRotatef(-xRotate, 1.0, 0.0, 0.0)
    glRotatef(-yRotate, .0, 1.0, 0.0)


def keyboard(key, x, y):
    global zTr, yTr, xTr
    if (key == 'r'): resetView()
    if (key == 'q'): exit(0)
    glutPostRedisplay()


def mouse(button, state, x, y):
    global action, xStart, yStart
    if (button == GLUT_LEFT_BUTTON):
        if (glutGetModifiers() == GLUT_ACTIVE_SHIFT):
            action = "MOVE_EYE_2"
        else:
            action = "MOVE_EYE"
    elif (button == GLUT_MIDDLE_BUTTON):
        action = "TRANS"
    elif (button == GLUT_RIGHT_BUTTON):
        action = "ZOOM"
    xStart = x
    yStart = y

def idle():
    glutPostRedisplay()


def motion(x, y):
    global zoom, xStart, yStart, xRotate, yRotate, zRotate, xTrans, yTrans
    if (action == "MOVE_EYE"):
        xRotate += x - xStart
        yRotate -= y - yStart
    elif (action == "MOVE_EYE_2"):
        zRotate += y - yStart
    elif (action == "TRANS"):
        xTrans += x - xStart
        yTrans += y - yStart
    elif (action == "ZOOM"):
        zoom -= y - yStart
        if zoom > 150.:
            zoom = 150.
        elif zoom < 1.1:
            zoom = 1.1
    else:
        print("unknown action\n", action)
    xStart = x
    yStart = y
    glutPostRedisplay()


# ------
# MAIN
# ------
if __name__ == "__main__":
    # GLUT Window Initialization
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # zBuffer
    glutInitWindowSize(g_Width, g_Height)
    glutInitWindowPosition(0 + 4, int(g_Height / 4))
    glutCreateWindow("Hands-up")
    # Initialize OpenGL graphics state
    init()
    # Register callbacks
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)
    printHelp()
    # Turn the flow of control over to GLUT
    glutMainLoop()