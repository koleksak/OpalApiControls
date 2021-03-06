import logging
logging.basicConfig(level=logging.INFO)
import os

from OpalApiControl.parser.device_vars import DeviceModels
from OpalApiControl.parser import psse
from OpalApiControl.parser.settings import Settings

if __name__ == '__main__':
    path = 'C:/RT-LABv11_Workspace_New/WECC181/models/phasor03_PSSE'
    rawfile = os.path.join(path, 'Curent02_final_ConstZ.raw')
    dyrfile = os.path.join(path, 'Curent02_final.dyr')
    Settings = psse.init_pf_to_stream(rawfile, dyrfile)
    fmu_path = os.path.join(path, 'FMU')
    devices = DeviceModels('WECC181', 'phasor03_PSSE', fmu_path, Settings)
    #opalfile = os.path.join(fmu_path,'GENCLS/win_.opal')
    devices.parse_opal_files(fmu_path)
    devices.find_devices_at_bus()
    devices.find_device_vars()
    devices.create_excel_file_pins_vars()
    print 'devices added'
