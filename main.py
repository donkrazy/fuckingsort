import csv
from operator import itemgetter


def get_rank(revenue):
    seq = my_sort(revenue)
    rank_list = [seq.index(v) + 1 for v in revenue]
    return rank_list


# TODO: mysort
def my_sort(revenue):
    return sorted(revenue)  # use default sort


def get_diff(rank1, rank2):
    diff_list = []
    for r1, r2 in zip(rank1, rank2):
        diff = r1 - r2
        if diff > 0:
            diff_list.append('+{}'.format(diff))
        elif diff < 0:
            diff_list.append(str(diff))
        elif diff == 0:
            diff_list.append('-')
    return diff_list


if __name__ == '__main__':
    # Read csv -> table
    table = []
    with open('2017_be_sheet.csv') as input_csv:
        reader = csv.reader(input_csv, delimiter='|')
        next(reader)  # Skip first row
        reven_0910 = []  # Revenue
        reven_1011 = []
        for row in reader:
            name = row[0]
            price, price_original, q_0910, q_1011 = (int(i) for i in row[1:])  # q is Quantity
            discount = int(100 * (price_original - price) / price_original)
            reven_0910.append(q_0910 * price)
            reven_1011.append(q_1011 * price)
            table.append([name, price_original, price, discount])

    # Get rank info
    rank_0910 = get_rank(reven_0910)
    rank_1011 = get_rank(reven_1011)
    rank_diff = get_diff(rank_0910, rank_1011)

    # Update rank, rankdiff to table(make new column)
    new_table = []
    for rank, diff, row in zip(rank_1011, rank_diff, table):
        name = row[0]
        price = "{:,}원".format(row[1])
        price_original = "{:,}원".format(row[2])
        discount = '{}%'.format(row[3])
        new_table.append([rank, diff, name, price_original, price, discount])

    # Sort new table by rank
    new_table.sort(key=itemgetter(0))

    # Print new table as output.csv
    with open('output.csv', 'w') as output:
        writer = csv.writer(output, delimiter='|')
        writer.writerow(['현재순위', '순위변동', '상품명', '정상가', '판매가', '할인율'])

        for row in new_table:
            writer.writerow(row)
