from datetime import datetime
import matplotlib.pyplot as plt


def main():
	f = open("../apache_push.log", 'r')
	lines = f.readlines()

	#for i in range(3):
	#	print(lines[i])

	time_li = []

	for line in lines:
		time_and_after = line.split('[')[1]
		time_and_0700 = time_and_after.split(']')[0]
		time = time_and_0700.split()[0]
		time_li.append(time)

	#print(time_li[:5])

	datetime_li = [datetime.strptime(x, "%d/%b/%Y:%H:%M:%S") for x in time_li]
	#print(datetime_li[0])

	base = datetime_li[0]
	offset_li = [(x - base) for x in datetime_li]
	#print(offset_li[0].total_seconds())

	offset_sec_li = [x.total_seconds() for x in offset_li]
	#print(offset_sec_li[:10])


	plt.hist(offset_sec_li, bins=150, alpha=0.75)
	plt.xlabel('Time')
	plt.ylabel('Bandwidth')
	plt.title('Log traffic under push mode')
	plt.show()



if __name__ == '__main__':
	main()



