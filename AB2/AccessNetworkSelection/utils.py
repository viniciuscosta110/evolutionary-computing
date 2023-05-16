def GetUserVoices(voices):
  totalVoices = sum(voices)

  return 1 - (totalVoices / 275)

def GetUserData(data):
  totalData = sum(data)
  
  return 1 - (totalData / 110)

def GetGSMCost(voice, data):
  return abs(- 30 + data + 6/25*voice)

def GetWCDMACost(voice, data):
  return abs(-80 + data + 8/15*voice)

def GetCost(userVoice, userData, costGSM, costWCDMA):
  return (pow(costGSM, 2) + pow(costWCDMA, 2)) * userVoice * userData