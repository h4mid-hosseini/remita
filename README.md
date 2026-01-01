# Exchange Accounting (Internal)

Simple internal Django app to track one manual exchange order at a time. You enter all numbers; the app only calculates and shows results.

## Setup

1. Create a PostgreSQL database.
2. Set environment variables:

```
export POSTGRES_DB=exchange_accounting
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_HOST=127.0.0.1
export POSTGRES_PORT=5432
```

3. Install dependencies and run migrations:

```
pip install django psycopg2-binary
python manage.py migrate
```

4. Create a partner (via Django admin) or add a quick fixture.

```
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Docker (VPS)

Build and run:

```
docker compose up --build
```

Then run migrations inside the web container:

```
docker compose exec web python manage.py migrate
docker compose exec web python manage.py compilemessages
```

Open `http://YOUR_SERVER_IP:8000/`.

## Math (All conversions through USDT)

Inputs (per order):
- `requested_eur`
- `commission_percent` (multiplier, e.g. 0.05 for 5%)
- `partner_commission_eur`
- `eur_to_usdt`
- `usdt_to_irt`
- `customer_payment_currency` (EUR, USDT, IRT)
- `profit_currency` (USDT or IRT)

Calculations:
- `commission_eur = requested_eur * commission_percent`
- `customer_total_eur = requested_eur + commission_eur`
- `customer_should_pay_usdt = customer_total_eur * eur_to_usdt`
- `customer_should_pay`:
  - EUR: `customer_total_eur`
  - USDT: `customer_should_pay_usdt`
  - IRT: `customer_should_pay_usdt * usdt_to_irt`
- `partner_total_eur = requested_eur + partner_commission_eur`
- `partner_usdt_amount = partner_total_eur * eur_to_usdt`
- `profit_usdt = customer_should_pay_usdt - partner_usdt_amount`
- `profit_irt = profit_usdt * usdt_to_irt` (only if profit currency is IRT)

## Notes
- Decimal is used everywhere for money and rates.
- No background jobs, no ledgers, no auto-rate fetching.
- A default EUR → USDT suggestion is seeded from ExchangeRate-API (EUR/USD proxy).
