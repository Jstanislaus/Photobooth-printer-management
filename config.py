def config():
    config = open("photobooth_config.txt",'r')
    config_array = config.readlines()
    Venue= config_array[6].split(' ')[-2].upper().strip("\n")
    portrait = config_array[7].split(' ')[-1].lower().strip("\n")
    img_red1 = config_array[8].split(' ')[-1].lower().strip("\n")
    img_red2 = config_array[9].split(' ')[-1].lower().strip("\n")
    photos_per_cart = config_array[10].split(' ')[-1].lower().strip("\n")
    button_pin = config_array[11].split(' ')[-1].lower().strip("\n")
    img_w = config_array[12].split(' ')[-1].lower().strip("\n")
    img_h = config_array[13].split(' ')[-1].lower().strip("\n")
    VERBOSE = config_array[14].split(' ')[-1].lower().strip("\n")
    portrait = portrait == "True"
    VERBOSE = VERBOSE == "True"
    return Venue,portrait,int(img_red1),int(img_red2),int(photos_per_cart),button_pin,img_w,img_h,VERBOSE
