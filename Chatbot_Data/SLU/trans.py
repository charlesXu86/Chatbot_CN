

def transform(source_dir, file_path):
	text_path = source_dir + "/seq.in"
	slot_path = source_dir + "/seq.out"
	label_path = source_dir + "/label"

	with open(text_path, 'r') as fr:
		text_lines = fr.readlines()
	with open(slot_path, 'r') as fr:
		slot_lines = fr.readlines()
	with open(label_path, 'r') as fr:
		label_lines = fr.readlines()

	with open(file_path, 'w') as fr:	
		for text, slots, label in zip(text_lines, slot_lines, label_lines):
			word_list = text.strip().split()
			slot_list = slots.strip().split()
			intent = label.strip()

			for word, slot in zip(word_list, slot_list):
				fr.write(word + ' ' + slot + '\n')
			fr.write(intent + '\n')

			fr.write('\n')


if __name__ == "__main__":
	transform('./atis/train', './formal_atis/train.txt')
	transform('./atis/valid', './formal_atis/dev.txt')
	transform('./atis/test', './formal_atis/test.txt')

	transform('./snips/train', './formal_snips/train.txt')
	transform('./snips/valid', './formal_snips/dev.txt')
	transform('./snips/test', './formal_snips/test.txt')
