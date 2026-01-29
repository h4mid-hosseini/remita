from decimal import Decimal
from .models import Order


class OrderCalculator:
    @staticmethod
    def calculate(order: Order) -> dict:
        requested_eur = Decimal(order.requested_eur)
        commission_percent = Decimal(order.commission_percent)
        partner_commission_eur = Decimal(order.partner_commission_eur)
        eur_to_usdt = Decimal(order.eur_to_usdt)
        usdt_to_irt = Decimal(order.usdt_to_irt)

        commission_eur = requested_eur * commission_percent
        customer_total_eur = requested_eur + commission_eur
        customer_should_pay_usdt = customer_total_eur * eur_to_usdt
        customer_should_pay_irt = customer_should_pay_usdt * usdt_to_irt

        if order.customer_payment_currency == Order.CURRENCY_EUR:
            customer_should_pay = customer_total_eur
        elif order.customer_payment_currency == Order.CURRENCY_USDT:
            customer_should_pay = customer_should_pay_usdt
        else:
            customer_should_pay = customer_should_pay_usdt * usdt_to_irt

        partner_total_eur = requested_eur + partner_commission_eur
        partner_usdt_amount = partner_total_eur * eur_to_usdt
        partner_total_irt = partner_usdt_amount * usdt_to_irt

        profit_usdt = customer_should_pay_usdt - partner_usdt_amount
        profit_irt_value = profit_usdt * usdt_to_irt
        profit_eur_value = None
        if eur_to_usdt != 0:
            profit_eur_value = profit_usdt / eur_to_usdt

        profit_irt = None
        if order.profit_currency == Order.PROFIT_IRT:
            profit_irt = profit_irt_value

        customer_paid_usdt = None
        if order.customer_paid_amount is not None and order.customer_paid_currency:
            paid_amount = Decimal(order.customer_paid_amount)
            if order.customer_paid_currency == Order.CURRENCY_EUR:
                customer_paid_usdt = paid_amount * eur_to_usdt
            elif order.customer_paid_currency == Order.CURRENCY_IRT:
                if usdt_to_irt != 0:
                    customer_paid_usdt = paid_amount / usdt_to_irt

        return {
            "commission_eur": commission_eur,
            "customer_total_eur": customer_total_eur,
            "customer_should_pay": customer_should_pay,
            "customer_should_pay_usdt": customer_should_pay_usdt,
            "customer_should_pay_irt": customer_should_pay_irt,
            "partner_total_eur": partner_total_eur,
            "partner_usdt_amount": partner_usdt_amount,
            "partner_total_irt": partner_total_irt,
            "profit_usdt": profit_usdt,
            "profit_irt": profit_irt,
            "profit_irt_value": profit_irt_value,
            "profit_eur_value": profit_eur_value,
            "customer_paid_usdt": customer_paid_usdt,
        }
