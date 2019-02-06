import visa
import time
import datetime

print("Connecting to resources....")
rm = visa.ResourceManager('@py')
address = "ASRL/dev/ttyUSB0::INSTR"
inst = rm.open_resource(address)
inst.SendEndEnabled = True
inst.TerminationCharacter = 10
inst.TerminationCharacterEnabled = True
inst.Timeout = 10000

inst.write("*RST\n")
inst.write("*CLS\n")
print(inst.query("*IDN?\n"))
inst.write("SYST:REM\n")
inst.write("VOLT 24.0\n")
inst.write("CURR 1.0\n")
inst.write("SOUR:APPL CH2\n")
inst.write("VOLT 0.0\n")
inst.write("CURR 1.0\n")
inst.write("SOUR:APPL CH3\n")
inst.write("VOLT 0.0\n")
inst.write("CURR 1.0\n")
inst.write("SOUR:APPL CH1\n")
now = datetime.datetime.now()
#print("Starting seqence at ")
print(now.strftime("Starting sequence at %Y-%m-%d %H:%M"))
i = 0
while i < 1728:     # sets us up for about 12 days of cycling
    # heat up phase
    k = 0
    while k < 384:
        inst.write("OUTP ON\n")
        time.sleep(2.0)   # on time 4 min
    #print("Cycle {0} ended..\n".format(i+1))
        inst.write("OUTP OFF\n")
        time.sleep(1.0)   # off time 6 min==
        k += 1
    i += 1
    time.sleep(250.0)
    print("Cycle {0} ended..\n".format(i+1))
    now = datetime.datetime.now()
    #print("Starting next cycle... ")
    print(now.strftime("Starting next cycle: %Y-%m-%d %H:%M"))

inst.write("SYST:LOC\n")
print("Closing resources...")

inst.close()
rm.close()
