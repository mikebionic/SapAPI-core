
		order_invoices = Order_inv.query\
			.filter(and_(
        Order_inv.GCRecord=='' or Order_inv.GCRecord==None,\
				Order_inv.InvStatId==1)).all()

------------------------
# single_object returns one resource in "data" instead of list 
def apiResourceInfo(isInactive=False,
                    fullInfo=False,
                    user=None):

	inv_statuses = Inv_status.query\
    .filter_by(GCRecord == None).all()
    
	# return wishlist info for authenticated user
	if current_user.is_authenticated:
		user=current_user
	if user:
		RpAccId = user.RpAccId
		wishes = Wish.query\
			.filter(and_(
				Wish.GCRecord=='' or Wish.GCRecord==None),\
				Wish.RpAccId==RpAccId)\
			.all()
	





	
	startDate = request.args.get('startDate',None,type=str)
	endDate = request.args.get('endDate',datetime.now().date())
	if startDate == None:
		# !!! usage status is configurable, rp acc provided
		order_invoices = Order_inv.query\
			.filter(and_(
				Order_inv.GCRecord=='' or Order_inv.GCRecord==None,\
				Order_inv.RpAccId==RpAccId))\
			.order_by(Order_inv.OInvDate.desc()).all()
	else:
		if (type(startDate)!=datetime):
			startDate = dateutil.parser.parse(startDate)
			startDate = datetime.date(startDate)
		if (type(endDate)!=datetime):
			endDate = dateutil.parser.parse(endDate)
			endDate = datetime.date(endDate)
			
		order_invoices = Order_inv.query\
		.filter(and_(
      Order_inv.GCRecord=='' or Order_inv.GCRecord==None,\
			Order_inv.RpAccId==RpAccId,\
			extract('year',Order_inv.OInvDate).between(startDate.year,endDate.year),\
			extract('month',Order_inv.OInvDate).between(startDate.month,endDate.month),\
			extract('day',Order_inv.OInvDate).between(startDate.day,endDate.day)))\
		.order_by(Order_inv.OInvDate.desc()).all()

	data = []
	for order_invoice in order_invoices:
		oInvData = order_invoice.to_json_api()

		inv_status_list = [inv_status.to_json_api() for inv_status in inv_statuses if inv_status.InvStatId == order_invoice.InvStatId]
		inv_status = dataLangSelector(inv_status_list[0])
		oInvData['InvStatName'] = inv_status['InvStatName']
		
		order_inv_lines = Order_inv_line.query\
			.filter(and_(
				Order_inv_line.GCRecord == '' or Order_inv_line.GCRecord == None),\
				Order_inv_line.OInvId == order_invoice.OInvId).all()

		order_inv_lines_list = []
		for order_inv_line in order_inv_lines:
			order_inv_lines_list.append(order_inv_line.to_json_api())
		oInvData['Order_inv_lines'] = order_inv_lines_list

		data.append(oInvData)

#############################

	resource_filtering = {
			"GCRecord": None,
		}
		if isInactive==False:
			resource_filtering["UsageStatusId"] = 1




if not rp_acc:

  # rp acc not provided and it found by order_invoce.rpaccid
  #################33
  rp_acc = Rp_acc.query\
      .filter(and_(
        Rp_acc.GCRecord == '' or Rp_acc.GCRecord == None),\
        Rp_acc.RpAccId == order_invoice.RpAccId)\
      .first()
  if rp_acc:
    rpAccData = apiRpAccData(dbModel=rp_acc)
    oInvData['Rp_acc'] = rpAccData['data']
  ######3#########
  
# rp acc is provided as a current user model
###############
  model_type = user['model_type']
	current_user = user['current_user']

	if model_type=='Rp_acc':
		RpAccId = current_user.RpAccId
################






----------------------------------
	elif request.method == 'POST':
		if not request.json:
			res = {
				"status": 0,
				"message": "Error. Not a JSON data."
			}
			response = make_response(jsonify(res),400)

		else:
			req = request.get_json()
			order_invoices = []
			failed_order_invoices = [] 
			for data in req:
				order_invoice = addOrderInvDict(data)
				print(order_invoice)
				try:
					OInvRegNo = order_invoice['OInvRegNo']
					thisOrderInv = Order_inv.query\
						.filter(Order_inv.OInvRegNo == OInvRegNo).first()
					# getting correct rp_acc of a database
					try:
						RpAccRegNo = data['Rp_acc']['RpAccRegNo']
						RpAccName = data['Rp_acc']['RpAccName']
						rp_acc = Rp_acc.query\
							.filter(Rp_acc.RpAccRegNo == RpAccRegNo and Rp_acc.RpAccName == RpAccName)\
							.first()
						if rp_acc:
							order_invoice['RpAccId'] = rp_acc.RpAccId
					except Exception as ex:
						print(ex)
						print("Rp_acc not provided")
						abort(400)

					if thisOrderInv:
						thisOrderInv.update(**order_invoice)
						db_test.session.commit()
					else:
						thisOrderInv = Order_inv(**order_invoice)
						db_test.session.add(thisOrderInv)
						db_test.session.commit()

					order_inv_lines = []
					failed_order_inv_lines = []
					for order_inv_line in data['Order_inv_lines']:
						order_inv_line = addOrderInvLineDict(order_inv_line)
						order_inv_line['OInvId'] = thisOrderInv.OInvId
						try:
							OInvLineRegNo = order_invoice['OInvLineRegNo']
							thisOrderInvLine = Order_inv_line.query\
								.filter(Order_inv_line.OInvLineRegNo == OInvLineRegNo).first()
							if thisOrderInvLine:
								thisOrderInvLine.update(**order_inv_line)
								db_test.session.commit()
								order_inv_lines.append(order_inv_line)
								print('order inv line updated')
							else:
								newOrderInvLine = Order_inv_line(**order_inv_line)
								db_test.session.add(newOrderInvLine)
								db_test.session.commit()
								order_inv_lines.append(order_inv_line)
								print('order inv line created')
						except Exception as ex:
							failed_order_inv_lines.append(order_inv_line)

					order_invoice['Order_inv_lines'] = order_inv_lines
					order_invoices.append(order_invoice)

				except Exception as ex:
					failed_order_invoices.append(order_invoice)

			status = checkApiResponseStatus(order_invoices,failed_order_invoices)