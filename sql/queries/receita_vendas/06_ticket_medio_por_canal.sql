SELECT 
channel,
    ROUND(SUM(quantity * unit_price * (1 - COALESCE(discount_pct, 0))) / COUNT(DISTINCT order_id),2) AS ticket_medio

FROM vendas
WHERE order_status = 'paid'
GROUP BY channel
ORDER BY ticket_medio DESC; 