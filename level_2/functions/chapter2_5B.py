import itertools

# Your task: Create a memory-efficient solution to
# 1 . Read the stock data file.
# 2. Find all days where the price was greater than $150.
# 3. Extract just the date and price for those days.
# 4. Count how many high-price days there are.

def find_high_price_days(filename,threshold=150):
    # Your generator expression pipeline goes here!
    #
    with open(filename,"r", encoding="utf8") as file:
        next(file)
        for stock in file:
            stock=stock.split(",")
            if (float(stock[1]))> threshold:
                yield stock[0],float(stock[1])

high_price_gen=find_high_price_days('stock_data.csv')

print(f"Found {sum(1 for _ in high_price_gen)} days with price > $150")

# When you're done, you should be able to run this:
# high_price_gen=find_high_price_days('stock_data.csv')
# print(f"Found {sum(1 for in high_price_gen)} days with price > $150")

# Pipeline Versión
def find_high_price_days_pipeline(filename,threshold=150):

    with open(filename) as f:
        # Skip the header row
        next(f)

        # 1. Create a base generador to strip whitespace from each line
        lines=(line.strip() for line in f)

        # 2. Chain another to split each line by the comma
        parsed=(line.split(',') for line in lines)

        # 3. Chain another to filter for rows where the price is high
        high_price=(row for row in parsed if float(row[1])> threshold)

        # 4. Chain a final one to extract just the date and price
        date_price=((row[0],float(row[1]))for row in high_price)

        yield from date_price

# This is an efficient way to count items in an iterator without building a list
# We have to re-create the generator since sum() will consume it.
count=sum(1 for _ in find_high_price_days_pipeline('stock_data.csv'))
print(f"Days with price > 150 : {count}")

print()
# Now let's get the first 5 results to see them
print("First 5 high-price days: ")
results=list(itertools.islice(find_high_price_days_pipeline('stock_data.csv'),5))
for date, price in results:
    print(f"{date}: ${price:.2f}")


