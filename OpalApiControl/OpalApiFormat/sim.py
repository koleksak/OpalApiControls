"""Streaming data thread for ePhasorsim using OpalApi Interface"""

from OpalApiControl.OpalApiFormat import stream
from OpalApiControl.OpalApiFormat import psse32
import threading
from time import sleep
import OpalApiPy
from system import acquire

#if __name__ == "__main__":
#def simulate():
class Simulate(threading.Thread):
    def __init__(self, Control):
        threading.Thread.__init__(self)
        #self.SimNum = SimNum
        self._Control = Control
        sim_stop = threading.Event()
        #Control for pausing model
        self.sim_stop = sim_stop
        SysParam, Varheader, Idxvgs, project, model = psse32.init_pf_to_stream()
        self.SysParam = SysParam
        self.Varheader = Varheader
        self.Idxvgs = Idxvgs
        self.project = project
        self.model = model
        #acq_wait = threading.Event()
        #self.acq_wait = acq_wait


    def run(self):
        self.sim_stop.set()
        #self.acq_wait.set()

        #st = threading.Thread(target=stream.ltb_stream_sim, args=(SysParam, Idxvgs, Varheader,
        #                                                          project, model))
        #st.start()
        stream.ltb_stream_sim(self.SysParam, self.Idxvgs, self.Varheader, self.project,
                              self.model, self.sim_stop)


if __name__ == "__main__":
    simu = Simulate(True)
    simu.start()