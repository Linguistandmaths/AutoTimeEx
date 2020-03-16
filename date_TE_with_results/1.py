import dateparser
import csv
with open('result_dateparser.csv', 'w') as csvfile:
    fieldnames = ['pattern', 'result']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    with open('test_ex.txt', encoding='utf-8', newline='') as f:
        test_strs = f.read().split('\n')
        for s in test_strs:
            writer.writerow({'pattern': s, 'result': dateparser.parse(s)})
