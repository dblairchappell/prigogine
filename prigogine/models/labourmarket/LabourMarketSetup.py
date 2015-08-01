import time
from prigogine.PrigogineCore import *

start = time.clock()
labourmarket = prigogine.loadmodel("LabourMarketModel.prm")

numHouseholds = 10000
labourmarket.households.create(numHouseholds)

labourmarket.households.states[0] = np.random.choice([1, 0], numHouseholds, [0.5,0.5])
labourmarket.households.reserveWages[0] = np.random.randint(100, size=numHouseholds)
labourmarket.households.weeksEmployed[0] = np.ones(numHouseholds)
labourmarket.households.minWages[0] = np.ones(numHouseholds) * 60

labourmarket.meanWeeksEmployed[0] = np.zeros(1)
labourmarket.meanReserveWages[0] = np.zeros(1)
labourmarket.meanMinWages[0] = np.zeros(1)

meanReserveWages = []
meanWeeksEmployed = []
meanMinWages = []

for i in range(100):
    labourmarket.runModel(1)
    meanWeeksEmployed.append(labourmarket.meanWeeksEmployed[labourmarket.readIndex][0])
    meanReserveWages.append(labourmarket.meanReserveWages[labourmarket.readIndex][0])
    meanMinWages.append(labourmarket.meanMinWages[labourmarket.readIndex][0])

end = time.clock()
print "\n\ntime elapsed: " + str(end - start) + "s"
plt.plot(meanReserveWages,'r-', meanWeeksEmployed, 'b-', meanMinWages, 'g-')
plt.show()

