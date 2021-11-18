
class Sensor_agent:

    def __init__(self):
        self.sensor2_rightup1=0
        self.sensor2_leftup1=0
        self.sensor2_rightdown1=0
        self.sensor2_leftdown1=0

        self.sensor2_up1=0
        self.sensor2_up2=0
        self.sensor2_right1=0
        self.sensor2_right2=0
        self.sensor2_left1=0
        self.sensor2_left2=0
        self.sensor2_down1=0
        self.sensor2_down2=0

        self.FoundBy1=0

    def Agent_hunter_sensor(self,agent):

        self.sensor2_rightup1 = self.field[self.agent.y-1][self.agent.x+1]
        self.sensor2_right1  =  self.field[self.agent.y][self.agent.x+1]
        self.sensor2_right2  =  self.field[self.agent.y][self.agent.x+2]

        self.sensor2_up1     =  self.field[self.agent.y-1][self.agent.x]
        self.sensor2_up2     =  self.field[self.agent.y-2][self.agent.x]

        self.sensor2_leftup1 =  self.field[self.agent.y-1][self.agent.x-1]
        self.sensor2_left1   =  self.field[self.agent.y][self.agent.x-1]
        self.sensor2_left2   =  self.field[self.agent.y][self.agent.x-2]

        self.sensor2_rightdown1=self.field[self.agent.y+1][self.agent.x+1]
        self.sensor2_down1   =  self.field[self.agent.y+1][self.agent.x]
        self.sensor2_down2   =  self.field[self.agent.y+2][self.agent.x]

        self.sensor2_leftdown1 =self.field[self.agent.y+1][self.agent.x-1]



        '''
        if self.field_now2 == self.sensor2_leftdown1:
            print("1!")
        if self.field_now2 == self.sensor2_up1:
            print("2!")
        if self.field_now2 == self.sensor2_up2:
            print("3!")

        if self.field_now2 == self.sensor2_rightup1:
            print("4!")
        if self.field_now2 == self.sensor2_right1:
            print("5!")
        if self.field_now2 == self.sensor2_right2:
            print("6!")

        if self.field_now2 == self.sensor2_leftup1:
            print("7!")
        if self.field_now2 == self.sensor2_left1:
            print("8!")
        if self.field_now2 == self.sensor2_left2:
            print("9!")

        if self.field_now2 == self.sensor2_rightdown1:
            print("10!")
        if self.field_now2 == self.sensor2_down1:
            print("11!")
        if self.field_now2 == self.sensor2_down2:
            print("12!")
        '''



    
        

    