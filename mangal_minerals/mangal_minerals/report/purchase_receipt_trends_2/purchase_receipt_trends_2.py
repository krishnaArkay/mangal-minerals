# Copyright (c) 2025, Arkay Apps and contributors
# For license information, please see license.txt

from frappe import _

from erpnext.controllers.trends import get_columns, get_data


def execute(filters=None):
	if not filters:
		filters = {}
	data = []
	conditions = get_columns(filters, "Purchase Receipt")
	data = get_data(filters, conditions)

	chart_data = get_chart_data(data, filters)

	return conditions["columns"], data, None, chart_data


def get_chart_data(data, filters):
	if not data:
		return []

	labels, amount_values, qty_values = [], [], []

	if filters.get("group_by"):
		# consider only consolidated row
		data = [row for row in data if row[0]]

	data = sorted(data, key=lambda i: i[-1], reverse=True)

	if len(data) > 10:
		data = data[:10]

	for row in data:
		labels.append(row[0])
		qty_values.append(row[-2])    # Assuming second last column is qty
		amount_values.append(row[-1]) # Last column is amount

	return {
		"data": {
			"labels": labels,
			"datasets": [
				{"name": _("Total Received Amount"), "values": amount_values},
				{"name": _("Total Received Qty"), "values": qty_values},
			],
		},
		"type": "bar",  # You could use 'axis-mixed' if you want different types per dataset
		"colors": ["#4e79a7", "#f28e2b"],
		# "colors": ["#1F77B4", "#FF7F0E"],
		# "colors": ["#8ECAE6", "#FFB703"],
		"fieldtype": "Float",
	}

