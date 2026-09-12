from ..services.common import collection


def find_invoice(item_id):
    return collection("invoices").find_one({"_id": item_id}) or collection("invoices").find_one({"invoice_number": item_id})
