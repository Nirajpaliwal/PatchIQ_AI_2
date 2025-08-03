def add(data):
    num1 = data.get('num1')
    num2 = data.get('num2')

    result = int(num1) + int(num2)
  
    return {
        'result': result,
        'num1': num1,
        'num2': num2
    }

data = {
    'num1': '5',
    'num2': 10
}   

added_result = add(data)
print("Added Result:", added_result)
