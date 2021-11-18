import const
import csv

FINISH_EPISODE = const.FINISH_EPISODE

class Log:    
    
    def __init__(self):
        pass
    
    def q_logger_step_episode(self,f): 
                
        data = [str(const.EPISODE_Agent1),str(const.Step_Agent1)]              
        writer=csv.writer(f,lineterminator='\n')
        writer.writerow(data)
        if const.EPISODE_Agent1== FINISH_EPISODE:
            f.close()
    
    
    def q_logger_q_table(self,qtable,row,col,action_count,q):
        
        for x in range(1,row):
            for y in range(1,col):
                for action in range(action_count):
 
                    data=[x,y,action,qtable[x][y][action]]
            
                    writer=csv.writer(q,lineterminator='\n')
                    writer.writerow(data)
        print('log OK!')
        q.close()
        
                    