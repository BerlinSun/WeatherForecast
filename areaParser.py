import xlrd

def getAreaDict():
	bk = xlrd.open_workbook("areaid_list.xlsx");
	try:
		sh = bk.sheet_by_name("Sheet1");
	except:
		print "No sheet is named 'Sheet1'";
		
	nrows = sh.nrows;
	ncols = sh.ncols;
	area_dict = {};

	for i in range(1, nrows):
		area_id = int(sh.cell_value(i, 0));
		name_cn = sh.cell_value(i, 1);
		area_dict[area_id] = name_cn;
	return area_dict;
