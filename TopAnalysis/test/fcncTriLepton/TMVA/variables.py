from ROOT import *
import os

#order does matter (order must be same to the ntuple)
def input_TT_bdt(channel):
    if channel == "TTZct" or channel == "TTZut":
        # Define default variable first
        var_list = ['Z_mass', 'W_MT',]
        var_list.extend(['KinTopWb_mass', 'KinTopZq_mass',
                         'MVAinput_bJ_DeepJetB', 'MVAinput_qJ_DeepJetB', 'MVAinput_bJ_pt',
                         'MVAinput_bJqJ_dR', 'MVAinput_WLbJ_dPhi', 'MVAinput_WLqJ_dR', 'MVAinput_ZL1bJ_dR', 'MVAinput_ZL1qJ_dR',])

    return var_list

def input_ST_bdt(channel):
    if channel == "STZct" or channel == "STZut":
        # Define default variable first
        var_list = ['Z_mass', 'TriLepton_WleptonZdPhi', 'TriLepton_WleptonZdR', 'W_MT',]
        var_list.extend(['KinTopWb_pt', 'KinTopWb_phi',
                        'MVAinput_WLZL1_dPhi', 'MVAinput_WLZL1_dR', 'MVAinput_bJ_DeepJetB',
                        'MVAinput_WLbJ_dPhi', 'MVAinput_WLbJ_dR', 'MVAinput_ZL1bJ_dR',])

    return var_list
