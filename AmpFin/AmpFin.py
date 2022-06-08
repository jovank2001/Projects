#!/usr/bin/env python3

#A Script to find the Amplicon and its length, as well as the distance of each primer from the target (UpperCase) base, and GC content
#Written by Jovan Koledin on 5/20/2022
#Input sequence and associated primers should be in seq.txt. The reverse primer is expected to be the conjugate
#Input format should be: sequence
#                        forward primer
#                        reverse primer
#

#Variables
seq = "a"
fp = "b"
rp = "c"
target = 0
amp = ""
ampLength = 0
fdist = 0
rdist = 0
INPUTS_PER_SET = 3



#Unconjugate reverse primer
def unconjugate(rp):
	
    rp = rp[::-1]
    #Invert bases (G->C), (A->T), etc..
    rp_unconjugated = []
    for i in range(0, len(rp)):
        if (rp[i] == 'a' or rp[i] == 'A'):
            rp_unconjugated.append('t')
        if (rp[i] == 't' or rp[i] == 'T'):
            rp_unconjugated.append('a')
        if (rp[i] == 'g' or rp[i] == 'G'):
            rp_unconjugated.append('c')
        if (rp[i] == 'c' or rp[i] == 'C'):
            rp_unconjugated.append('g')
        
        
        rp_new = "".join(rp_unconjugated)
            
    return rp_new

#Get target position in seq 
def getTarget(seq):
    for i in range(0, len(seq)):
        if seq[i].isupper():
            target = i
            
    if target == 0:
	    print("Could not find target")
	    
    return target
            
#Get distance of each primer from target
def getPrimerDistance(fp, rp, target, seq):
    fp = fp.lower()
    rp = rp.lower()
    fdist = target - seq.find(fp) - len(fp)
    rdist = seq.find(rp) - target
    if fdist == (target + 1) or rdist == (-1 - target):
        print("Couldnt find primer matches.")
    return fdist, rdist

#Find GC content of amplicon  
def G_C(amp):
    GC = 0
    for base in amp:
        if base == 'g' or base == 'c':
            GC += 1
    return (100*GC)/len(amp)
            
#Big run file
def main():
    global rp, inFile, amp, ampLength, inputs_per_set
    inFile = open("seq.txt", "r")
    outFile = open("ampInfo.p3", "w")
    text_samp = inFile.readlines()
    #Convert text to 2d array for each DNA set
    seq_2D = [text_samp[i:i+INPUTS_PER_SET] for i in range(0, len(text_samp), INPUTS_PER_SET)]
    for set in seq_2D:
        rp = set[2]
        rp = rp.strip()
        fp = set[1]
        fp = fp.strip()
        seq = set[0]
        seq = seq.strip()
        rp = unconjugate(rp)
        target = getTarget(seq)
        seq = seq.lower()
        fdist, rdist = getPrimerDistance(fp, rp, target, seq)
        amp = seq[int(target-fdist-len(fp)):int(rdist+target+len(rp))]
        GC = G_C(amp)
        
        #Write to outfile
        ampLength = len(amp)
        outFile.write("Amplicon: " + amp + "\n")
        outFile.write("Amplicon Length: " + str(ampLength) + "\n")
        outFile.write("Forward Primer Distance: " + str(fdist) + "\n")
        outFile.write("Reverse Primer Distance: " + str(rdist) + "\n")
        outFile.write("GC Content (%): " + str(GC) + "\n")
    
    inFile.close()
    outFile.close()
    
    
#Call main
if __name__ == "__main__":
    main()
    

            
    
