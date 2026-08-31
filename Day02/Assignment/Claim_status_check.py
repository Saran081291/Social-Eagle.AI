claim_id = input("Enter Claim ID: ").strip()
patient_name = input("Enter Patient Name: ").strip()
billed_amount = float(input("Enter Billed Amount: ").strip())
claim_status = input("Enter Claim Status: ").strip()
normalized_status = claim_status.lower()

denial_reason = ""
paid_amount = None
patient_responsibility = None

if normalized_status == "submitted":
	result = "Claim has been submitted and is awaiting processing."
elif normalized_status == "pending":
	result = "Claim is currently under review."
elif normalized_status == "approved":
	result = "Claim has been approved for payment."
elif normalized_status == "denied":
	denial_reason = input("Enter Denial Reason: ").strip()
	result = "Claim has been denied. Review denial reason."
elif normalized_status == "paid":
	paid_amount = float(input("Enter Paid Amount: ").strip())
	patient_responsibility = billed_amount - paid_amount
	result = "Claim has been paid successfully."
else:
	result = "Invalid claim status."

print("\n========== CLAIM STATUS ==========")
print(f"Claim ID       : {claim_id}")
print(f"Patient Name   : {patient_name}")
print(f"Billed Amount  : ${billed_amount:.2f}")
print(f"Claim Status   : {claim_status}")

if denial_reason:
	print(f"Denial Reason  : {denial_reason}")

if paid_amount is not None:
	print(f"Paid Amount    : ${paid_amount:.2f}")
	print(f"Patient Responsibility : ${patient_responsibility:.2f}")

print(f"\nResult         : {result}")
print("==================================")
