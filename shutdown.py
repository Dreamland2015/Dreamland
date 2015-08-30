from SetupDreamland import configs
if __name__ == "__main__":
    s = multiSSH.MultiDreamandPi(configs)
    s.shutdown()
    print('Finished setup run.')
