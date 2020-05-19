import matplotlib.pyplot as plt


def graphplt(reward_X,reward_O,label_main,labelX,labelY) :
      plt.figure(figsize=[8, 6])
      plt.plot(reward_X,color='olive',label = "X Agent")
      plt.plot(reward_O, color='red', label="O Agent")
      plt.xlabel(labelX, fontsize=14)
      plt.ylabel(labelY, fontsize=14)
      plt.legend()
      plt.savefig(label_main+".png")
