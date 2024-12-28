import requests
from bs4 import BeautifulSoup

sources_reductions = {
    "Player's Handbook" : "PHB",
    "Xanathar's Guide to Everything" : "XGE",
    "Acquisitions Inc." : "A Inc.",
    "Unearthed Arcana 36 - Starter Spells" : "UA-36",
    "Xanathar's Guide to Everything/Elemental Evil Player's Companion" : "XGE/EEPC",
    "Strixhaven: A Curriculum of Chaos" : "S:ACC",
    "Fizban's Treasury of Dragons" : "FTD",
    "Unearthed Arcana 78 - Draconic Options" : "UA-78",
    "The Book of Many Things" : "TBMT",
    "Unearthed Arcana 85 - Wonders of the Multiverse" : "UA-85",
    "Tasha's Cauldron of Everything" : "TCE",
    "Unearthed Arcana 66 - Fighter, Rogue, and Wizard" : "UA-66",
    "Guildmaster's Guide to Ravnica" : "GGR",
    "Unearthed Arcana 7 - Modern Magic" : "UA-7"
}

WIKIDOT_URL = "https://dnd5e.wikidot.com"

class_name = str(input("Tell me the class you want the spells of: "))
class_spells_url = WIKIDOT_URL + "/spells:" + class_name

response = requests.get(class_spells_url)

if response.status_code == 200:

	soup = BeautifulSoup(response.text, 'html.parser')
	divs = soup.find_all('div', id=True)
	
	spell_list_file = open("spells_list.tex", "w")

	for div in divs:
		id_text = div['id']

		if "wiki-tab-0" in id_text:
		    print("== Downloading the table " + id_text[-1] + " ==")
		    
		    spell_list_file.write("\\newpage\n")
		    spell_list_file.write("\\fancyhead{}\n")
		    
		    if id_text[-1] == "0":
		        spell_list_file.write("\\fancyhead[RO, RE]{\\textbf{Cantrips}}\n")
		    else:
		        spell_list_file.write("\\fancyhead[RO, RE]{\\textbf{" + id_text[-1] + "-th level spells}}\n")
		    
		    spell_list_file.write("\\input{spells/" + id_text[-1] + "-th_spells}\n\n")
		    
		    spells_file = open("spells/" + id_text[-1] + "-th_spells.tex", "w")
		    
		    spells = div.find_all('a', href=True)
		    
		    for spell in spells:
		        spell_code = spell['href']
		        response = requests.get(WIKIDOT_URL + spell_code)
		        
		        if response.status_code == 200:
		            soup = BeautifulSoup(response.text, 'html.parser')
		            
		            spell_page_content = soup.find_all('div', {"class":True})
		            
		            for spell_div in spell_page_content:
		                spell_id_text = spell_div['class']
		                
		                if "page-header" in spell_id_text:
		                    spell_info = spell_div.find_all('span')
		                    
		                    for data in spell_info:
		                        spells_file.write("\\begin{spell}{")
		                        spells_file.write(data.text)
		                        spells_file.write("}")
		            
		            spell_page_content = soup.find_all('div', id=True)
		            
		            for spell_div in spell_page_content:
		                spell_id_text = spell_div['id']
		                
		                if spell_id_text == "page-content":
		                    spell_info = spell_div.find_all('p')
		                    
		                    spells_file.write("{" + sources_reductions[spell_info[0].text[8:len(spell_info[0].text)]] + "}")
		                    spells_file.write("{" + spell_info[1].text + "}\n")
		                    spells_file.write("{\n")
		                    
		                    spell_data = spell_info[2].text
		                    
		                    spells_file.write("\t\\spTime{")
		                    spells_file.write(spell_data[spell_data.find("Casting Time: ") + len("Casting Time: "): spell_data.find("Range: ") - 1] + "}\n")
		                    
		                    spells_file.write("\t\\spRange{")
		                    spells_file.write(spell_data[spell_data.find("Range: ") + len("Range: "): spell_data.find("Components: ") - 1] + "}\n")
		                    
		                    spells_file.write("\t\\spComponents{")
		                    spells_file.write(spell_data[spell_data.find("Components: ") + len("Components: "): spell_data.find("Duration: ") - 1] + "}\n")
		                    
		                    spells_file.write("\t\\spDuration{")
		                    spells_file.write(spell_data[spell_data.find("Duration: ") + len("Duration: "): len(spell_data)] + "}\n")
		                    
		                    spells_file.write("}\n")
		                    
		                    for i in range(3, len(spell_info)):
		                        if (not "At Higher Levels." in spell_info[i].text) or (not "Spell Lists." in spell_info[i].text):
		                            spells_file.write(spell_info[i].text + "\n")
		                    
		                    last_paragraph = spell_info[-2].text
		                    
		                    if "At Higher Levels" in last_paragraph:
		                        spells_file.write("\n\\note{At Higher Levels.}")
		                        spells_file.write(last_paragraph[len("At Higher Levels."): len(last_paragraph)] + "\n")
		                    
		                    spells_file.write("\\end{spell}\n\n")
		        else:
		            print("There was an error loading the spell page")
		            print(f"Error code: {response.status_code}")
		            
		    spells_file.close()
	spell_list_file.close()

else:
	print("There was an error loading the wikidot page")
	print(f"Error code: {response.status_code}")

