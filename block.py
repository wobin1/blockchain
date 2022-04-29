import json
import os
import hashlib



blockchain_dir = 'blockchain/'
block_count = len(os.listdir(blockchain_dir))

def get_hash(prev_block):
	with open( blockchain_dir + prev_block, 'rb') as f:
		content = f.read()

	return hashlib.md5(content).hexdigest()


def check_integrity():
	files = sorted(os.listdir(blockchain_dir), key= lambda x: int(x))

	result = []
	
	for file in files[1:]:
		with open(blockchain_dir + file ) as f:
			block = json.load(f)

		prev_hash = block.get('prev_block').get('hash')
		prev_filename = block.get('prev_block').get('filename')

		actual_hash = get_hash(prev_filename)

		if prev_hash == actual_hash:
			res = "is Ok"
		else:
			res = "was changed"

		print(f'Block {prev_filename}: {res}')

		result.append({'block': prev_filename, 'result': res})
	return result


def write_block(borower, lender, amount):
	prev_block = str(block_count)
	data = {
		"borower":borower,
		"lender": lender,
		"amount": amount,
		"prev_block": {
			"hash": get_hash(prev_block),
			"filename": prev_block
		}
	}

	current_block = str( block_count + 1)
	with open(blockchain_dir + current_block, 'w') as f:
		json.dump(data, f, indent=4, ensure_ascii=False)
		f.write('\n')

def main():
	write_block("hello", 1, 0)


if __name__== '__main__':
	main()