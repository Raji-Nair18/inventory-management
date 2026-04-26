import sys
import os
# Ensure we can import from Backend/services
sys.path.append(os.path.join(os.getcwd(), 'Backend'))

from services.matching_service import names_match

def test(n1, n2, expected=True):
    res = names_match(n1, n2)
    status = "PASS" if res == expected else "FAIL"
    print(f"[{status}] names_match('{n1}', '{n2}') -> {res} (Expected: {expected})")

print("--- Basic Matching ---")
test("Milk", "milk")
test("milk", "Milk")
test("MILK", "milk")

print("\n--- Plurals and Measurement Units ---")
test("Milks", "milk")
test("Milk 1L", "milk")
test("Milk 500ml", "Milk")
test("Biscuits", "Biscuit")
test("Oil 1 Litre", "Oil")

print("\n--- Substrings and Generic Terms ---")
test("Sunflower Oil", "Oil")
test("Fresh Milk", "Milk")
test("Premium Bread", "Bread")
test("Milk Product", "Milk")

print("\n--- Synonym Groups ---")
test("fuel", "diesel")
test("kerosene", "fuel")
test("diesel", "kerosene")
test("sunflower oil", "oil")
test("vegetable oil", "oil")
test("cooking oil", "sunflower oil")

print("\n--- Non-Matches ---")
test("Milk", "Bread", False)
test("Fuel", "Milk", False)
test("Oil", "Soda", False)
test("abc", "xyz", False)
