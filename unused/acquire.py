# ***************************************************************************************
# Description
#
# Connect to a running or paused model. If the model is not running, it will be executed.
# Model must be compiled and assigned prior to connecting.
# ***************************************************************************************


# ***************************************************************************************
# Modules
import OpalApiPy
import RtlabApi
import os
from time import sleep
import logging

# ***************************************************************************************
# Globals
# ***************************************************************************************
# list of returned model state
modelStateList = ["not connected", "not loadable", "compiling", "loadable", "loading", \
                  "resetting", "loaded", "paused", "running", "disconnected"]

realTimeModeList = {'Hardware Sync':0, 'Simulation':1, 'Software Sync':2, 'Not Used':3, 'Low Priority Sim':4}
# ***************************************************************************************
# Main
# ***************************************************************************************

def connectToModel(project,model):
    """Takes the name of the project and model to connect to(string) and connectsif model is compiled"""

    # project = 'ephasorex1'
    # model = 'phasor01_IEEE39'
    # connect to the local project

    projectPath = 'C:/RT-LABv11_Workspace_New/'
    projectName = os.path.join(projectPath, str(project) + '/' + str(project) + '.llp')
    modelPath = os.path.join(projectPath, str(project) + '/simulink/')
    modelName = str(model) + '.mdl'

    # Connects to Project
    try:
        RtlabApi.OpenProject(projectName)
        # modelState,realTimeMode = OpalApiPy.GetModelState()
    except:
        logging.error("<Missed Connection>")
        return False
    return True


def connectToModelTest(project, model):
    """Takes the name of the model to connect to(string) and connects based on current model state"""

    # project = 'Connect1'
    # model = 'rtdemo1'
    # connect to the local project
    try:
        modelState, realTimeMode = OpalApiPy.GetModelState()

    except:
        projectPath = 'C:/RT-LABv11_Workspace_New/'
        projectName = os.path.join(projectPath, str(project)+'/'+str(project) +'.llp')
        modelPath = os.path.join(projectPath, 'Simulink/')
        modelName = str(model) + '.mdl'

        #Connects to Project
        RtlabApi.OpenProject(projectName)
        print "Now connected to '%s' project." % projectName

        #Connects to model
        #filename = os.path.join(modelPath,modelName)
        # OpalApiPy.SetCurrentModel(filename)
        modelState, realTimeMode = OpalApiPy.GetModelState()
        # print "Model State Connected is %s." %modelStateList[modelState]
        print "Now connected to %s model." %modelName
        #print "Model state 1 is %s" %modelStateList[modelState]

        # OpalApiPy.StartCompile2((("",31),))
        # print"compiling"
        # OpalApiPy.RegisterDisplay(OpalApiPy.DISPLAY_REGISTER_ALL)
        # OpalApiPy.DisplayInformation(0)

        try:
            # Acquire Model State, Get system control
            modelState, realTimeMode = OpalApiPy.GetModelState()
            print "Model state is %s'." %modelStateList[modelState]

            # Model Connection Parameters
            systemControl = 0
            # modelName  = ''
            modelPath  = ''
            exactMatch = 0
            returnOnAmbiquity  = 0

            # Connect API to model if already running
            if modelState == OpalApiPy.MODEL_RUNNING:
                instanceId = OpalApiPy.ConnectByName(str(model))
                print "Now connected to running model %s.\n" %model
                # print ("instanceId is: ", str(instanceId))

            elif (modelState == OpalApiPy.MODEL_LOADABLE):


                # If model is not loaded,load and ask to execute

                realTimeMode = realTimeModeList['Software Sync']
                timeFactor = 1
                OpalApiPy.Load(realTimeMode, timeFactor)
                print "RT Project %s is Loading." %project
                OpalApiPy.LoadConsole()
                print "Model %s console is loading" % model


                chooseExecute = raw_input("Loading Complete.Would you like to execute model now?  y/n ")
                chooseExecute = 'y'
                if chooseExecute == 'y':
                    try:
                        print "Now Executing Model"
                        systemControl = 1
                        OpalApiPy.GetSystemControl(systemControl)
                        print "System Control Granted"

                        # OpalApiPy.LoadConsole()
                        # print "Model %s console is loading" % model

                        OpalApiPy.ExecuteConsole()
                        print "Model %s console is executed" %model

                        OpalApiPy.Execute(1)

                        #sleep(10)
                        modelState,realTimeMode = OpalApiPy.GetModelState()
                        print"Model State is %s" %modelStateList[modelState]
                        if((modelState == OpalApiPy.MODEL_RUNNING) | (modelState == OpalApiPy.MODEL_LOADED)):
                            print"Model Running"

                        else:

                            modelState, realTimeMode = OpalApiPy.GetModelState()
                            print"Model State is %s" % modelStateList[modelState]
                            print"Model Not executed"
                            transitionToPause()

                            # systemControl = 1
                            # OpalApiPy.GetSystemControl(systemControl)
                            # OpalApiPy.ResetConsole()
                            # print "System Control Granted"
                            # print "Console is now reset"
                            # # resets the model after loading
                            # OpalApiPy.Pause()
                            # print "Model %s is now paused" % model
                            # # OpalApiPy.Reset()
                            # # print "Model %s is now reset." %model
                            #
                            # systemControl = 0
                            # OpalApiPy.GetSystemControl(systemControl)
                            # print "System Control is released"
                            # # OpalApiPy.Disconnect()
                            # # print "Disconnected from %s model" % modelName

                    except:

                        modelState, realTimeMode = OpalApiPy.GetModelState()
                        print"Model State is %s" % modelStateList[modelState]
                        print"Model Not executed"
                        transitionToPause()

                        # print "Module execution unsuccessful"
                        # systemControl = 1
                        # OpalApiPy.GetSystemControl(systemControl)
                        # OpalApiPy.ResetConsole()
                        # print "System Control Granted"
                        # print "Console is now reset"
                        # # resets the model after loading
                        # OpalApiPy.Pause()
                        # print "Model %s is now paused" % model
                        # # OpalApiPy.Reset()
                        # # print "Model %s is now reset." %model
                        #
                        # systemControl = 0
                        # OpalApiPy.GetSystemControl(systemControl)
                        # print "System Control is released"
                        # # OpalApiPy.Disconnect()
                        # # print "Disconnected from %s model" % modelName

                elif chooseExecute == 'n':

                    print "Model not executed"

                    # OpalApiPy.ExecuteConsole()
                    # OpalApiPy.PauseConsole()


            elif (modelState == OpalApiPy.MODEL_LOADED):
                # If model is loaded but not running, execute the model
                try:
                    print "Now Executing Model"
                    systemControl = 1
                    OpalApiPy.GetSystemControl(systemControl)
                    print "System Control Granted"

                    # Load Simulink and Matlab
                    OpalApiPy.LoadConsole()
                    print "Model %s console is loaded" % model
                    OpalApiPy.ExecuteConsole()
                    print "Model %s console is executed" % model
                    OpalApiPy.Execute(1)

                    modelState,realTimeMode = OpalApiPy.GetModelState()
                    print"Model State is %s" %modelStateList[modelState]
                    if((modelState == OpalApiPy.MODEL_RUNNING) | (modelState == OpalApiPy.MODEL_LOADED)):
                        print"Model is running"

                    else:

                        modelState, realTimeMode = OpalApiPy.GetModelState()
                        print"Model State is %s" % modelStateList[modelState]
                        print"Model Not executed"
                        transitionToPause()

                except:
                    modelState,realTimeMode = OpalApiPy.GetModelState()
                    print"Model State is %s" %modelStateList[modelState]
                    print"Model Not executed"
                    fullDisconnect()

            elif(modelState == OpalApiPy.MODEL_PAUSED):
                #try:
                    systemControl = 1
                    #OpalApiPy.GetSystemControl(0)
                    #OpalApiPy.Disconnect()
                    #OpalApiPy.ConnectByName(str(model))
                    OpalApiPy.GetSystemControl(systemControl)
                    OpalApiPy.LoadConsole()
                    print"Console loaded"
                    OpalApiPy.ExecuteConsole()
                    print "Model %s console is executed" % model
                    OpalApiPy.Execute(1)
                    print "Model %s is executed" % model
                    modelState, realTimeMode = OpalApiPy.GetModelState()
                    print"Model State is %s" % modelStateList[modelState]
                    if ((modelState == OpalApiPy.MODEL_RUNNING) | (modelState == OpalApiPy.MODEL_LOADED)):
                        print"Model is running"

                #except:
                 #   logging.error('<Model Control Released>')
                    #fullDisconnect()

            else:
                print "Compile and Assign Model before Loading or Running"

        finally:
            print "Complete Connection Successful"
            # Disconnect from Model after testing
            # OpalApiPy.Disconnect()
            # print "Disconnected from %s model" %modelName

    #MODEL IS ALREADY CONNECTED,
    else:
        print("MODEL ALREADY CONNECTED")
        #OpalApiPy.Disconnect()
        connectToModel('IEEE39Acq', 'phasor01_IEEE39')
        modelState, realTimeMode = OpalApiPy.GetModelState()
        print"Model State is %s" % modelStateList[modelState]
        systemControl = 1
        OpalApiPy.GetSystemControl(systemControl)
        print"System Control Granted"
        #systemControl = 1
        # OpalApiPy.GetSystemControl(0)
        # OpalApiPy.Disconnect()
        # OpalApiPy.ConnectByName(str(model))
        #OpalApiPy.GetSystemControl(systemControl)
        #OpalApiPy.LoadConsole()
        #print"Console loaded"
        #OpalApiPy.ExecuteConsole()
        #print "Model %s console is executed" % model
        OpalApiPy.Execute(1)
        print "Model %s is executed" % model
        modelState, realTimeMode = OpalApiPy.GetModelState()
        print"Model State is %s" % modelStateList[modelState]
        if ((modelState == OpalApiPy.MODEL_RUNNING) | (modelState == OpalApiPy.MODEL_LOADED)):
            print"Model is running"


def fullDisconnect():
    """Basic disconnect steps to reset matlab/simulink console, then rtlab console, then disconnect from the model"""

    modelState, realTimeMode = OpalApiPy.GetModelState()
    print"Model State is %s" % modelStateList[modelState]
    systemControl = 1
    OpalApiPy.GetSystemControl(systemControl)
    print"System Control Granted"

    if(modelState == OpalApiPy.MODEL_RUNNING):
        OpalApiPy.PauseConsole()
        print"Console is now paused"
        OpalApiPy.Pause()
        print "Model is now paused"

    OpalApiPy.ResetConsole()
    print "System Control Granted"
    print "Console is now reset"

    OpalApiPy.Pause()
    print "Model %s is now paused"

    OpalApiPy.Reset()
    print "Model %s is now reset."
    print "System Control Released"

    systemControl = 0
    OpalApiPy.GetSystemControl(systemControl)
    print "System Control is released"
    OpalApiPy.Disconnect()
    print "Disconnected from %s model"

def transitionToPause():
    """Allows model to transition to pause state
    without resetting matlab/simulink console, or rtlab console"""
    connectToModel('IEEE39Acq', 'phasor01_IEEE39')
    modelState, realTimeMode = OpalApiPy.GetModelState()
    print"Model State is %s" % modelStateList[modelState]
    systemControl = 1
    OpalApiPy.GetSystemControl(systemControl)
    print"System Control Granted"
    # OpalApiPy.LoadConsole()
    # OpalApiPy.PauseConsole()
    # print"Console is now paused"
    OpalApiPy.Pause()
    print "Model is now paused"
    systemControl = 0
    OpalApiPy.GetSystemControl(systemControl)
    #OpalApiPy.Disconnect()
    print "System Control is released"


