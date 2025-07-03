import json
from tabulate import tabulate  # pip install tabulate

# NOT ALL (8080)
data1 = []
#ALL (8081)
data2 = []
# Output file paths
output_file = "result.txt"
summary_file = "summarize.txt"

# Check for list length mismatch
if len(data1) != len(data2):
    print(f"⚠️ Length mismatch: data1 has {len(data1)} items, data2 has {len(data2)} items")
    min_len = min(len(data1), len(data2))
else:
    min_len = len(data1)

all_comparisons = []
fields_only_in_HKT = set()
fields_only_in_all = set()
mismatched_fields = []
matched_field_count = 0
mismatched_field_count = 0
total_shared_fields = 0

for i in range(min_len):
    item1 = data1[i]
    item2 = data2[i]

    fields_HKT = set(item1.keys())
    fields_all = set(item2.keys())
    all_fields = fields_HKT | fields_all
    comparison_result = []

    for field in sorted(all_fields):
        HKT_value = item1.get(field, "Not have")
        all_value = item2.get(field, "Not have")

        if field in fields_HKT and field not in fields_all:
            status = "❌ Missing in ALL"
            fields_only_in_HKT.add(field)
        elif field in fields_all and field not in fields_HKT:
            status = "❌ Missing in HKT"
            fields_only_in_all.add(field)
        elif HKT_value == all_value:
            status = "✅ Match"
            matched_field_count += 1
            total_shared_fields += 1
        else:
            status = "❌ Mismatch"
            mismatched_field_count += 1
            total_shared_fields += 1
            mismatched_fields.append([i + 1, field, HKT_value, all_value])

        comparison_result.append([
            i + 1,
            field,
            HKT_value,
            all_value,
            status
        ])

    all_comparisons.append(comparison_result)

# --- Write result.txt ---
with open(output_file, "w", encoding="utf-8") as f:
    for comparison in all_comparisons:
        item_index = comparison[0][0]
        f.write(f"\n🔍 Item #{item_index} Comparison:\n")
        table_text = tabulate(comparison, headers=["Item #", "Field", "HKT Value", "ALL Value", "Status"], tablefmt="grid")
        f.write(table_text + "\n")

print(f"✅ Result written to '{output_file}'")

# --- Write summarize.txt ---
with open(summary_file, "w", encoding="utf-8") as f:

    if fields_only_in_HKT:
        f.write("\n❌ Fields in HKT but NOT in ALL\n")
        HKT_only_table = [[field, data1[0].get(field, ""), "Not have"] for field in sorted(fields_only_in_HKT)]
        f.write(tabulate(HKT_only_table, headers=["Field", "HKT Value", "ALL Value"], tablefmt="grid") + "\n")
    else:
        f.write("\n✅ NO Fields in HKT but NOT in ALL\n")

    if fields_only_in_all:
        f.write("\n❌ Fields in ALL but NOT in HKT\n")
        all_only_table = [[field, "Not have", data2[0].get(field, "")] for field in sorted(fields_only_in_all)]
        f.write(tabulate(all_only_table, headers=["Field", "HKT Value", "ALL Value"], tablefmt="grid") + "\n")
    else:
        f.write("\n✅ NO Fields in ALL but NOT in HKT\n")

    if mismatched_fields:
        f.write("\n❌ Fields with Mismatched Values\n")
        f.write(tabulate(mismatched_fields, headers=["Item #", "Field", "HKT Value", "ALL Value"], tablefmt="grid") + "\n")
    else:
        f.write("\n✅ No Mismatch Value\n")

    f.write("\n✅ Summary\n")
    if matched_field_count > 0:
        print(f"✅ {matched_field_count} shared fields between HKT and ALL match exactly in values.\n")
        f.write(f"✅ {matched_field_count} shared fields between HKT and ALL match exactly in values.\n")
    else:
        print("❌ No matching shared fields between HKT and ALL.\n")
        f.write("❌ No matching shared fields between HKT and ALL.\n")

    if fields_only_in_HKT:
        print(f"❌ {len(fields_only_in_HKT)} fields exist only in HKT: {', '.join(sorted(fields_only_in_HKT))}.\n")
        f.write(f"❌ {len(fields_only_in_HKT)} fields exist only in HKT: {', '.join(sorted(fields_only_in_HKT))}.\n")
    else:
        print("✅ NO Fields in HKT but NOT in ALL\n")
        f.write("✅ NO Fields in HKT but NOT in ALL\n")

    if fields_only_in_all:
        print(f"❌ {len(fields_only_in_all)} fields exist only in ALL: {', '.join(sorted(fields_only_in_all))}.\n")
        f.write(f"❌ {len(fields_only_in_all)} fields exist only in ALL: {', '.join(sorted(fields_only_in_all))}.\n")
    else:
        print("✅ NO Fields in ALL but NOT in HKT\n")
        f.write("✅ NO Fields in ALL but NOT in HKT\n")

    if mismatched_field_count > 0:
        print(f"❌ {mismatched_field_count} fields shared but with different values.\n")
        f.write(f"❌ {mismatched_field_count} fields shared but with different values.\n")
    else:
        print("✅ No Mismatch Value\n")
        f.write("✅ No Mismatch Value\n")

print(f"✅ Summary written to '{summary_file}'")
