

def function(file):
    lines = []
    for line in f:
        lines.append(line)
    return lines

with open('xc7z020clg484pkg.txt', 'r') as f: #open the file
    contents = function(f) #put the lines to a variable.
    n = len(contents)
    Pin2Name = []
    for i in range(3,n-2):
        line = contents[i].split()
        temp = [line[0], line[1]]
        Pin2Name.append(temp)

with open('PacManV5_Trenz_Signals_Flat.csv', 'r') as f: #open the file
    contents = function(f) #put the lines to a variable.
    ThreeCols = []
    for i in range(len(contents)-1):
        line = contents[i+1].strip("\n")
        splitline = line.split(",")
        if len(splitline) >= 3:
            ThreeCols.append([splitline[0], splitline[2], splitline[1]])
    for entry in ThreeCols:
        print(entry)

FourCols = []
NewThreeCols = []
for i in range(len(ThreeCols)):
    name = ThreeCols[i][2]
    if name[0] != 'B':
        NewThreeCols.append(ThreeCols[i])
        continue
    name = name[1:]
    #print(name)
    splitname = name.split("_")
    #print(splitname)
    for j in range(len(Pin2Name)):
        #print(Pin2Name[j])
        bool1 = "_"+splitname[0] in Pin2Name[j][1]
        if len(splitname) == 3:
            bool2 = splitname[1]+splitname[2] in Pin2Name[j][1]
        else:
            bool2 = False
        if bool1 and bool2:
            FourCols.append([ThreeCols[i][0],ThreeCols[i][1],ThreeCols[i][2], Pin2Name[j][1], Pin2Name[j][0]])

for entry in FourCols:
    print(entry)            

            
Constraints = []
sum = 0
NAMES = []
for i in range(len(FourCols)):
    PinNumber = FourCols[i][4]
    TempName = FourCols[i][1]
    if "PISO" in TempName:
        number = TempName[4:6]
        if number[1] != '0':
            number = int(number[0])-1
        else:
            number = 9
        PSNumber = number * 4 + int(TempName[-1])
        Name = 'PISO[' + str(PSNumber) + ']'
    elif "POSI" in TempName:
        number = TempName[4:6]
        if number[1] != '0':
            number = int(number[0])-1
        else:
            number = 9
        PSNumber = number * 4 + int(TempName[-1])
        Name = 'POSI[' + str(PSNumber) + ']'
    elif "_SYNC" in TempName:
        number = int(TempName[4:-5]) - 1
        Name = "SYNC[" + str(number) + ']'
    elif "ENABLE" in TempName:
        number = int(TempName[4:-7])-1
        Name = "TILE_EN[" + str(number) + ']'
    elif "_TRIG" in TempName:
        number = int(TempName[4:-5]) - 1
        Name = "TRIG[" + str(number) + ']'
    elif "ADC_D" in TempName:
        number = int(TempName[-1])
        nstr = TempName[-2:];
        if nstr.isdigit():
            number = int(nstr)
        Name = "ADC_D["+str(number)+']'
    elif "TEST" in TempName:
        number = int(TempName[-1])-1
        Name = "TEST_OUT["+str(number)+']'
    elif "(not used)" == TempName:
        continue
    else:
        Name = TempName
    NAMES.append([Name, PinNumber])

Names = sorted(NAMES)


for i in range(len(Names)):
    MAIN = f"set_property PACKAGE_PIN {Names[i][1]} [get_ports {Names[i][0]}]\n"
    Constraints.append(MAIN)



string1 = ''.join(Constraints)
text_file = open("Output2.txt", "w")
text_file.write(string1)
text_file.close()





