def leer_opta_f27(xml_file):
    ''''
    Function to read F27 Opta Pass Matrix file

    Input:
    OPTA F27 xml file


    '''

    import xml.etree.ElementTree as ET
    import pandas as pd

    file = ET.parse(xml_file)

    namelist= []
    xlist =[]
    ylist = []
    passer = []
    receiver = []
    passeslist = []
    poslist = []
    pass_lost_list = []

    for node in file.getroot():
        for players in node:
            name = node.attrib.get("player_name")
            x = float(node.attrib.get("x"))
            y = float(node.attrib.get("y"))
            pos = node.attrib.get("position")
            pass_lost = int(node.attrib.get("pass_lost"))
            namelist.append(name)
            xlist.append(x)
            ylist.append(y)
            poslist.append(pos)
            pass_lost_list.append(pass_lost)


            passes = players.text
            name = players.attrib.get("player_name")
            passer.append(node.attrib.get("player_name"))
            receiver.append(name)
            passeslist.append(passes)

    
    df=pd.DataFrame(data = list(zip(passer,xlist,ylist,poslist,receiver, passeslist)),
                    columns = ["Passer","x","y","Position_Passer","Receiver","PassSuccess"])
    
    return df.sort_values(by=["Position_Passer",'Passer']).reset_index(drop=True)