import time

from torch import split

def drive(speed: int):
    print("Driving fast af at", speed, "km/h")

def rotate(deg: int):
    print("Rotating", deg, "degrees")

def vroom(speed: int):
    print(speed, "vroom")

def aktiver(param: str):
    print("Kjørte aktiver med param", param)

def aktiver_algoritme(role: str):
    print("Activating algorithm for", role)
    if(role == "ingeniør"):
        print("ing")
    if(role == "marsgeolog"):
        print("geo")
    if(role == "fysiker"):
        print("fys")
    if(role == "telemetri"):
        print("tele")
    if(role == "koordinator"):
        print("koord")
        
# Fysiker tools: hazcam, supercam, mastcam-z, optisk, ir, 
# format(zoom, panorama, selfie, standard)
# Ingeniør tools: solcellepanel
# Geolog tools: rimfax, spektrometer
# Satelitt: Azimuth, elevation, signalstyrke
# lagre(disk), minne

def forsinkelse(delay: str):
    try:
        time.sleep(float(delay))
    
    except ValueError:
        print(f"Forsinkelse tar bare tall, f.eks. på formen: \"1\" eller \"1.92\". Brukeren ga: {delay}")
    

class Code_parts:
    def __init__(self):
        self.coordinator_lines = [],
        self.telemetry_lines = [],
        self.physics_lines = [],
        self.engineer_lines = [],
        self.geologist_lines = []

    def add_lines(self, filename: str):
        file = open(filename, "r", encoding="utf-8")
        lines = file.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].replace('æ', 'ae').replace('ø', 'o').replace('å', 'a')
        
        print(lines)
        coord_start = lines.index("pseudokode for koordinator\n")
        tel_start = lines.index("pseudokode for telemetri\n")
        phy_start = lines.index("pseudokode for fysiker\n")
        eng_start = lines.index("pseudokode for ingenior\n")
        geo_start = lines.index("pseudokode for marsgeolog\n")

        self.coordinator_lines = lines[coord_start + 2 : tel_start - 1]
        self.telemetry_lines = lines[tel_start + 2 : phy_start - 1]
        self.physics_lines = lines[phy_start + 2 : eng_start - 1]
        self.engineer_lines = lines[eng_start + 2 : geo_start - 1]
        self.geologist_lines = lines[geo_start + 2 :]

    def print_lines(self):
        print("Coordinator:", self.coordinator_lines, "\nTelemetry:", self.telemetry_lines, "\nPhysics:", self.physics_lines, "\nEngineer:", self.engineer_lines, "\nGeologist:", self.geologist_lines)


eit_code = Code_parts()

def translate_to_python(lines: list, output_path: str):
    python_lines = []
    print("Length of lines:", len(lines), lines)
    for i, line in enumerate(lines):
        # Indices of elif, else and løkke. Ngl husker ikke hvordan det går med tab vs spaces og indeksering av stringen, men we hope its ok ( it is not)
        elseif_idx = line.find("else if (")
        else_idx = line.find("else {")
        loop_idx = line.find("lokke")

        # Add comment to lines that are useless. (Maybe we need to implement each of these as functions, but works for now)
        if(line.find("pseudokode for") == 0 or line.find("--------------------------------") == 0):
            # It's a filler line which defines that the following section is for a certain group
            python_lines.append("#" + line)

        elif(line.find("if (") != -1):
            # It's an if

            # TODO split the arguments of the if up such that we can handle e.g. if ( a==2 && b!=3 || c>4)
            # Low priority i think, there is a ton of mess here with extra parentheses in the case of e.g. if ( (a==2 && b!=3) || c>4)
            # And not even sure Andøya supports multiple logical evaluations in a single if

            # string_between_parentheses = line[line.find("(") + 1 : line.find(")")]
            # print(string_between_parentheses)
            # params = string_between_parentheses.split("&&", "||")
            # for i, param in params:
            
            # This is hacky at best, only works on ifs with the exact format: if(x == y), if(x >= y and a > b or c != d) etc..
            # And really it only works when there is a variable on the left side and a value on the right. E.g. if(a > 6 and b == "asd")
            
            start_parentheses_idx = line.find("(")
            end_parentheses_idx = line.find(")")
            # responstid på kommunikasjon og krav til ekstra arbeid ice
            
            if(start_parentheses_idx != -1 and end_parentheses_idx != -1):
                str_within_parentheses = line[start_parentheses_idx + 1 : end_parentheses_idx]
                split = str_within_parentheses.split(" ")
                reconstructed = ""
                for i in range(len(split)//3):
                    if(i == 0):
                        if(split[3*i+2].isdigit()):
                            reconstructed += split[3*i] + " " + split[3*i+1] + " " + split[3*i+2]
                        else:
                            reconstructed += split[3*i] + " " + split[3*i+1] + " \"" + split[3*i+2] + "\""
                    else:
                        if(split[3*i + i+1].isdigit()):
                            reconstructed += split[3*i + i-1] + " " + split[3*i + i] + " " + split[3*i + i+1] + " " + split[3*i + i+2]
                        else:
                            reconstructed += split[3*i + i-1] + " " + split[3*i + i] + " \"" + split[3*i + i+1] + "\" " + split[3*i + i+2]
                    
                python_lines.append(line[0:start_parentheses_idx+1] + reconstructed + line[end_parentheses_idx:].replace(" {", ":"))
            else:
                #fuckoff
                #python_lines.append(line.replace(" {", ":"))
                print("Just put parentheses in your if's for now")

        elif(elseif_idx != -1):
            # It's an else if
            python_lines.append("\t"*elseif_idx + "elif (" + line.strip().replace(" {", ":\n"))

        elif(else_idx != -1):
            # It's an else
            python_lines.append("\t"*else_idx + "else:\n")
        
        elif(loop_idx != -1):
            # It's a for loop
            loop_count = line.strip().translate({ord(i): None for i in '():{'}).split("==")[1]
            python_lines.append("\t"*loop_idx + "for i in range(" + loop_count + "):\n")
        
        elif(len(line.strip()) > 0 and line.strip()[0] == "}"):
            # It's a line with just '}'
            # Remove the } but keep the indent becuase python :^)
            python_lines.append(line[0:len(line)-len(line.lstrip())] + "\n")

        else:
            # It's a function call
            start_parentheses_idx = line.find("(")
            end_parentheses_idx = line.find(")")
            if(start_parentheses_idx != -1 and end_parentheses_idx != -1):
                # Example: "add(a=3, b=5)" -> "a=3, b=5"
                str_within_parentheses = line[start_parentheses_idx + 1 : end_parentheses_idx]
                # Example: "a=3, b=5" -> ["a=3", "b=5"]
                split_up_assignments = str_within_parentheses.split(",")

                temp_inside_parentheses = ""
                for el in split_up_assignments:
                    # Example: "a=3" -> a="3"
                    split_assignment = el.split("=")
                    if(len(split_assignment) > 1):
                        temp_inside_parentheses += split_assignment[0] + "=\"" + split_assignment[1] + "\","
                    else:
                        temp_inside_parentheses +=  "\"" + split_assignment[0] + "\","
                # Smash it all together and remove the trailing comma from up here ------------------ ^
                python_lines.append(line[0:start_parentheses_idx + 1] + temp_inside_parentheses[0:-1] + line[end_parentheses_idx : -1] + "\n")
            else:
                # Only blank lines and other weird stuff like classes should come through here
                # Strip the white chars before the start of the text with lstrip()
                stripped = line.lstrip()
                non_white_char_idx = len(line) - len(stripped)
                if(non_white_char_idx > 0):
                    python_lines.append("\t"*non_white_char_idx +  stripped)
                else:
                    python_lines.append(line)


    output_file = open(output_path, "w", encoding="utf-8")
    output_file.writelines(python_lines)
    output_file.close()

    #content = open(output_path).read()
    #exec(content)

eit_code.add_lines("EiT_pseudokode.txt")
translate_to_python(eit_code.coordinator_lines, "translated_scripts/coordinator_code.py")
translate_to_python(eit_code.telemetry_lines, "translated_scripts/telemetry_code.py")
translate_to_python(eit_code.physics_lines, "translated_scripts/physics_code.py")
translate_to_python(eit_code.engineer_lines, "translated_scripts/engineer_code.py")
translate_to_python(eit_code.geologist_lines, "translated_scripts/geologist_code.py")




#inguna / eit
#rtsp://192.168.57.203:8080/ for livestream






'''
        # Remove prefix and suffix spaces
        stripped = line.strip()

        # Check if a loop starts in the line
        loop_idx = line.find("løkke")
        if(loop_idx != -1):
            # Split line into each side of ==, and get the number of loops
            loop_len = stripped.split("==")[1][1:-3]
            #print("loop len:", loop_len)
            loops_left = int(loop_len)
            current_loop_indent = loop_idx
            loop_start_line_idx = i
            continue

        # Check if there is an end bracket on the line and that its indent corresponds with the start of the loop.
        # If it does, add the content of the loop x times to the lines array
        end_bracket_idx = line.find("}")
        if(end_bracket_idx != -1):
            if(loops_left > 0 and end_bracket_idx == current_loop_indent):
                for j in range(loops_left):
                    #print("Adding lines:", lines[loop_start_line_idx + 1 : i], "to lines")
                    for k in range(len(lines[loop_start_line_idx + 1 : i])):
                        lines.insert(i + 1 + k, lines[loop_start_line_idx + 1 : i][k])
            #print("Done adding lines, lines arr now looks like: ", lines)
            continue
        
        if(stripped.find("if") == 0):
            print("found if in line", line)
            pure = stripped.translate({ord(i): None for i in '():{'}).split("if")[1].split("==")
            print("got pure", pure)
            if(eval(pure[0]) != eval(pure[1])):
                inside_false_if_block = True
                continue
        else:
            split_line = stripped.split("(")
            exec(split_line[0] + "(\"" + split_line[1][0:-1] + "\")")
        
        
        if(stripped.find("endif") != -1):
            inside_false_if_block = False
            print("found endif in line", line)
            continue

        if(inside_false_if_block):
            continue

        if(stripped.find("if") == 0):
            print("found if in line", line)
            pure = stripped.translate({ord(i): None for i in '():{'}).split("if")[1].split("==")
            print("got pure", pure)
            if(eval(pure[0]) != eval(pure[1])):
                inside_false_if_block = True
                continue
        else:
    '''




def execute_lines(lines: list):
    last_if_was_true = True
    inside_false_if_block = False
    current_if_indent = 0

    loops_left = 0
    current_loop_indent = 0
    loop_start_line_idx = 0
    print("Length of lines:", len(lines), lines)
    for i, line in enumerate(lines):
        
        # Check if line needs to be run at all, if not skip it
        if(line == "\n" or line == "" or line == "\t"):
            print("Skipping line", line, i)
            continue

        if(inside_false_if_block and line.strip().find("}") != 0):
            continue

        # Remove prefix and suffix spaces
        stripped = line.strip()

        # Check if a loop starts in the line
        loop_idx = line.find("løkke")
        if(loop_idx != -1):
            # Split line into each side of ==, and get the number of loops
            loop_len = stripped.split("==")[1][1:-3]
            #print("loop len:", loop_len)
            loops_left = int(loop_len)
            current_loop_indent = loop_idx
            loop_start_line_idx = i
            continue

        # Check if there is an end bracket on the line and that its indent corresponds with the start of the loop.
        # If it does, add the content of the loop x times to the lines array
        end_bracket_idx = line.find("}")
        if(end_bracket_idx != -1):
            if(loops_left > 0 and end_bracket_idx == current_loop_indent):
                for j in range(loops_left):
                    #print("Adding lines:", lines[loop_start_line_idx + 1 : i], "to lines")
                    for k in range(len(lines[loop_start_line_idx + 1 : i])):
                        lines.insert(i + 1 + k, lines[loop_start_line_idx + 1 : i][k])
            #print("Done adding lines, lines arr now looks like: ", lines)
            continue
        
        if(stripped.find("if") == 0):
            print("found if in line", line)
            pure = stripped.translate({ord(i): None for i in '():{'}).split("if")[1].split("==")
            print("got pure", pure)
            if(eval(pure[0]) != eval(pure[1])):
                inside_false_if_block = True
                continue
        else:
            split_line = stripped.split("(")
            exec(split_line[0] + "(\"" + split_line[1][0:-1] + "\")")
        
    '''
        if(stripped.find("endif") != -1):
            inside_false_if_block = False
            print("found endif in line", line)
            continue

        if(inside_false_if_block):
            continue

        if(stripped.find("if") == 0):
            print("found if in line", line)
            pure = stripped.translate({ord(i): None for i in '():{'}).split("if")[1].split("==")
            print("got pure", pure)
            if(eval(pure[0]) != eval(pure[1])):
                inside_false_if_block = True
                continue
        else:
            

add_lines("EiT_pseudokode.txt")
execute_lines(eit_code.coordinator_lines)
    '''

