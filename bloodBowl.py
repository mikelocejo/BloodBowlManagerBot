def Get_Race(race_id):
        
      #This dict should be in static file
    races_dict = {1:':bbhuman:',2:':bbdwarf:',3:':bbskaven:',4:':bborc:',7:':bbwoodElf:',9:':bbdarkElfs:',12:':bbnorses:',13:':bbamazon:',15:':bbhighElf:',16:':bbkhemri:',17:':bbnecromantic:',20:':bbvampire:',21:':bbchaosDwarf:',24:':bbbretonnia:'}
        
      #If race_id exists in dict return race otherwise return Unknown 
    race = races_dict.get(race_id)
    if race: return race    
    else: return 'Unknown'
