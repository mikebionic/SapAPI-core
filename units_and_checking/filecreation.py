

# import os
# if not os.path.exists('work/'):
# 	try:
# 		os.makedirs('work/')
# 	except:
# 		print("error creating directory")


def saveImageQuality(size):
	output_sizes = {
		"xdpi":(150,150),
		"xxdpi":(300,300),
		"xxxdpi":(1280,1280)
	}
	print (output_sizes[size])

saveImageQuality("xdpi")