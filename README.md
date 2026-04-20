# Лабораторная работа №7: Observability

## Prometheus + Grafana + Tempo

---

<div align="center">
  <h3>☸️ Kubernetes + 📦 Helm + 📊 Prometheus/Grafana</h3>
  <br/>
</div>

---

## Цель работы

Научиться:
- экспортировать метрики в формате Prometheus
- настраивать скрейпинг метрик
- строить дашборды в Grafana с запросами PromQL
- настраивать распределённый трейсинг с OpenTelemetry и Grafana Tempo

---


---

## Запуск

### 1. Запустите приложение с метриками

```bash
cd lab7ipr
python bot.py

Приложение будет доступно на порту 8081:

Метрики: http://localhost:8081/metrics

Health: http://localhost:8081/health
```

### 2. Запустите стек наблюдаемости
```
cd telegram-support-observability
docker compose up -d
```

### Prometheus Targets
Откройте в браузере: http://localhost:19090/targets

<img width="1920" height="1080" alt="2026-04-20_05-47-02" src="https://github.com/user-attachments/assets/1925dd19-2b0e-4c87-8910-59724c089bd0" />


### Grafana
Откройте в браузере: http://localhost:13001
API: http://localhost:8081/api/stats
### Логин: admin
#### Пароль: admin

<img width="1920" height="1080" alt="2026-04-20_05-46-04" src="https://github.com/user-attachments/assets/ad17f1a5-e8de-4616-8f0c-9a098ee79ecd" />

## Генерация нагрузки
```
for i in {1..20}; do
  curl -s http://localhost:8081/api/stats
  curl -s -X POST http://localhost:8081/api/support
  echo "Request $i sent"
  sleep 0.5
done
```
