
CREDIT_CARD = 'tarjeta'
TRANSFER = 'transferencia'
DEBIT = 'domiciliacion'

PAYMENT_METHODS = (
    (CREDIT_CARD, 'Pago con tarjeta'),
    (TRANSFER, 'Transferencia'),
    (DEBIT, 'Domiciliación bancaria'),
)

PENDING_PAYMENT = 'pago'
CURRENCY_BUY = 'compramoneda'

CARD_PAYMENT_TYPES = (
    (PENDING_PAYMENT, 'Pago pendiente'),
    (CURRENCY_BUY, 'Compra de Etics'),
)

RETURN_REASONS = (
    ('noexiste', 'Cuenta no existe'),
    ('cancelada','Cuenta cancelada'),
    ('devuelto','Devuelto por cliente'),
    ('sinfondos','Devuelto por el banco (falta de fondos)'),
    ('otros','Otros'),
)