import re

global remaining


class FetchFrame:
    def __init__(self):

        f = open('hands_long.txt', 'r')
        self.file_content = f.read()
        # print(file_content)
        # data = file_content.split(',')

        # file_content = "Cats are smarter than dogs"
        self.pattern_list = [' Right hand, id 117, position: ', 'Thumb finger,', 'Index finger,', 'Middle finger,', 'Ring finger,',
                        'Pinky finger,']
        # matchObj = re.match(r'(.*?) Right hand, id 117, position: (.*?)    ', file_content, re.M|re.I)

    def parse_arm(self):
        matchObj = re.match(r'(.*?) Right hand, id 117, position: (.*?)wrist position: (.*?), elbow position: (.*?)  (.*)',
                                self.file_content, re.M | re.I)
        if matchObj:
            start = self.str2coordinates(matchObj.group(3))
            end = self.str2coordinates(matchObj.group(4))
            return start, end
        else:
            return None

    def parse_finger(self, finger_name):
        # print(finger_name)

        matchObj = re.match(r'(.*?)' + finger_name + '(.*?)      (.*?)      (.*?)      (.*?)     (.*?)   (.*)',
                                self.file_content, re.M | re.I)
        if matchObj:
            # print "matchObj.group() : ", matchObj.group()
            # print "matchObj.group(1) : ", matchObj.group(1)
            # print "matchObj.group(2) : ", matchObj.group(2)
            # print "matchObj.group(3) : ", matchObj.group(3)
            # print "matchObj.group(4) : ", matchObj.group(4)
            # print "matchObj.group(5) : ", matchObj.group(5)
            # print "matchObj.group(6) : ", matchObj.group(6)
            metacarpal = matchObj.group(3)
            startm, endm = self.get_joints(metacarpal)
            proximal = matchObj.group(4)
            startp, endp = self.get_joints(proximal)
            intermediate = matchObj.group(5)
            starti, endi = self.get_joints(intermediate)
            distal = matchObj.group(6)
            startd, endd = self.get_joints(distal)
            global remaining
            remaining = matchObj.group(7)
            return [startm, startp, starti, startd, endd]
        else:
            print
            "No match!!"

    # print(start, end)

    def get_joints(self, bone):
        # print(bone)
        matchObj = re.match(r'(.*?)start: (.*?), end: (.*?), direction', bone, re.M | re.I)
        # print(matchObj.group(2))
        # print(matchObj.group(3))
        start = self.str2coordinates(matchObj.group(2))
        end = self.str2coordinates(matchObj.group(3))
        return start, end

    def str2coordinates(self, input):
        matchObj = re.match(r'\((.*?), (.*?), (.*?)\)', input, re.M | re.I)
        if matchObj:
            # print(matchObj.group(1))
            # print(matchObj.group(2))
            # print(matchObj.group(3))
            return (float(matchObj.group(1)), float(matchObj.group(2)), float(matchObj.group(3)))

        else:
            print('no match')
    def __iter__(self):
        return  self
    def __next__(self):
        try:
            start, end = self.parse_arm()
            joints = [self.parse_finger(self.pattern_list[i])[:] for i in range(1, 6)]
            joints.append(start)
            joints.append(end)
        # # joints = parse_finger(pattern_list[5])
        # print(joints)
            self.file_content = remaining
            return joints
        except:
            return None

# print('remaining:', remaining)
# matchObj = re.match(r'(.*?)'+pattern_list[2]+'(.*?)      (.*?)      (.*?)      (.*?)     (.*?)   (.*?)', file_content, re.M|re.I)

# if matchObj:
#    print "matchObj.group() : ", matchObj.group()
#    print "matchObj.group(1) : ", matchObj.group(1)
#    print "matchObj.group(2) : ", matchObj.group(2)
#    print "matchObj.group(3) : ", matchObj.group(3)
#    print "matchObj.group(4) : ", matchObj.group(4)
#    print "matchObj.group(5) : ", matchObj.group(5)
#    print "matchObj.group(6) : ", matchObj.group(6)


# else:
#    print "No match!!"
# [print(data_1) for data_1 in data]

# frame = FetchFrame()
# i = iter(frame)
# print(next(i))
# next(i)