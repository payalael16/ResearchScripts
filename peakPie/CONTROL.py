import makePeakInput
import subprocess

#makePeakInput.makePeakInputQ('ovarySmall.conf', 20)
#makePeakInput.mergeInputs('ovarySmall.conf', 20)

#makePeakInput.makePeakInputQ('ovaryDeg.conf', 3)
#makePeakInput.mergeInputs('ovaryDeg.conf', 3)

#makePeakInput.makePeakInputQ('kidneySmall.conf', 20)
#makePeakInput.mergeInputs('kidneySmall.conf', 20)

#makePeakInput.makePeakInputQ('kidneyDeg.conf', 2)
#makePeakInput.mergeInputs('kidneyDeg.conf', 3)

#makePeakInput.makePeakInputQ('siPeaks.conf', 20)
#makePeakInput.mergeInputs('siPeaks.conf', 20)

#makePeakInput.makePeakInputQ('siDegradome.conf', 4)
#makePeakInput.mergeInputs('siDegradome.conf', 4)

#tcc = 'chr1:1:1102538:1103319'
#subprocess.Popen(['qsub', '-V', '-cwd', '-e', 'test', '-o', 'test', 'q.sh', '%s' % tcc, 'agoProfile.conf', '200']).wait()
#qsub -V -cwd -o test -e test q.sh chr1:1:1102538:1103319 agoProfile.conf 20

import sys

(sName, confBaseName, makeChoice, lowestE) = sys.argv

if makeChoice == '1':
        makePeakInput.makePeakInputQ(confBaseName, int(lowestE))
else:
        makePeakInput.mergeInputs(confBaseName, int(lowestE))
