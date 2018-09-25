from collections import Counter

def transform(in_file, out_file):

	with open(in_file, 'r') as fr:
		lines = fr.readlines()

	with open(out_file, 'w') as fw:
		start = False
		count = Counter()

		true = 0.0
		total = 0.0

		for line in lines:

			if start:
				items = line.strip().split()

				if len(items) > 1:
					fw.write(line)
					count[items[-1]] += 1
				else:
					item = count.most_common(1)[0][0]
					fw.write(item + '\t' + items[0] + '\n')

					if (item == items[0]):
						true += 1.0
					total += 1.0

					count.clear()
					start = False
			else:
				fw.write(line)

				if len(line) > 2:
					start=True

	return true / total

if __name__ == "__main__":
	print transform('./error_samples_snips.txt', './test_result_snips.txt')
	print transform('./error_samples_atis.txt', './test_result_atis.txt')



